"""
Indexing unit tests.
"""

# pylint: disable=too-many-public-methods

import unittest

from indexing.collectible import Collectible
from indexing.collector import Collector
from indexing.filters.directoryfilter import DirectoryFilter
from indexing.filters.pathfilterfactory import PathFilterFactory
from indexing.indexer import Indexer
from indexing.indexerpolicy import IndexerPolicy
from indexing.nodes import CategorizedNode, UncategorizedNode
from indexing.pathanalyzer import PathAnalyzer
from indexing.pathpattern import PathPattern
from indexing.pathpatternanalyzer import PathPatternAnalyzer
from indexing.tagconfig import TagConfig
from testing.testhelper import TestHelper
from testing.videotestenvironment import VideoTestEnvironment

class IndexingTest(unittest.TestCase):

    ####################################################################################################################
    # Initialization and cleanup.
    ####################################################################################################################

    @classmethod
    def setUpClass(cls):

        # Create test environment.
        cls._environment = VideoTestEnvironment()

        # Create TestHelper.
        cls._helper = TestHelper()
        cls._helper.add_environment(cls._environment)

        # Create test files.
        cls._helper.create_files()

    @classmethod
    def tearDownClass(cls):

        cls._helper.clean()

    ####################################################################################################################
    # Test methods.
    ####################################################################################################################

    def test_01_path_pattern(self):

        # Arrange and act.
        path_pattern = PathPattern('a/b/([^/]*)/[0-9]+', ['?a', 'b', '?c', '?d'], 4)

        # Assert.
        self.assertEqual('a/b/([^/]*)/[0-9]+', path_pattern.path_pattern_regexp.pattern, 'Invalid regular expression.')
        self._compare_lists(['?a', 'b', '?c', '?d'], path_pattern.group_tag_mapping)
        self.assertEqual(4, path_pattern.length_without_any_tags, 'Invalid value for length without don\'t cares.')

    def test_02_tag_config(self):

        # Arrange and act.
        tag_config = TagConfig('!', ':', 'something', {'tag1' : '.*', 'tag2' : '[0-9]+'})

        # Assert.
        self.assertEqual('!', tag_config.start, 'The start separator is incorrect.')
        self.assertEqual(':', tag_config.end, 'The end separator is incorrect.')
        self.assertEqual('something', tag_config.tag_any, 'The ANY tag is incorrect.')
        self._compare_dictionaries(tag_config.tag_patterns, {'tag1' : '.*', 'tag2' : '[0-9]+'})

    def test_03_pathpatternanalyzer_validate(self):

        # Arrange.
        tag_patterns_1 = {
            'languages' : '([^/]+)',
            'quality' : '([^/]+)',
            'title' : '([^/]+)'}
        tag_config_1 = TagConfig('%', '%', None, tag_patterns_1)
        tag_patterns_2 = {
            'languages' : '([^/]+)',
            'quality' : '([^/]+)',
            'title' : '([^/]+)'}
        tag_config_2 = TagConfig('%', '%', ('any', '[^/]+'), tag_patterns_2)

        path_pattern_analyzer = PathPatternAnalyzer()

        # Act and assert.
        self._assert_raises_with_message(
            Exception,
            'Exception should be raised indicating unallowed tag.',
            path_pattern_analyzer.parse,
            tag_config_1,
            '%title%/Content/%quality%/%languages%/%any%')
        self._assert_raises_with_message(
            Exception,
            'Exception should be raised indicating missing fixpoint.',
            path_pattern_analyzer.parse,
            tag_config_2,
            '%title%/%quality%/%languages%/%any%')

    def test_04_pathpatternanalyzer_anal_1(self):

        # Arrange.
        tag_patterns = {
            'languages' : '([^/]+)',
            'quality' : '([^/]+)',
            'title' : '([^/]+)'}
        tag_config = TagConfig('%', '%', ('dontcare', '[^/]+'), tag_patterns)
        path_pattern_analyzer = PathPatternAnalyzer()

        # Act.
        path_pattern = path_pattern_analyzer.parse(tag_config, '%title%/Content/%quality%/%languages%/%dontcare%')

        # Assert.
        self.assertEqual(
            '([^/]+)/Content/([^/]+)/([^/]+)/([^/]+|)$',
            path_pattern.path_pattern_regexp.pattern,
            'The built pattern not equals with the expected one.')
        self._compare_lists(
            ['title', 'quality', 'languages', 'dontcare'],
            path_pattern.group_tag_mapping)
        self.assertEqual(4, path_pattern.length_without_any_tags, 'Invalid group length.')

    def test_05_pathpatternanalyzer_anal_2(self):

        # Arrange.
        tag_patterns = {
            'episode_title' : '([^/]+)',
            'languages' : '([^/]+)',
            'quality' : '([^/]+)',
            'title' : '([^/]+)'}
        tag_config = TagConfig('%', '%', ('dontcare', '[^/]+'), tag_patterns)
        path_pattern_analyzer = PathPatternAnalyzer()

        # Act.
        path_pattern = path_pattern_analyzer.parse(
            tag_config,
            '%title%/Content/%quality%/%languages%/%dontcare%/%episode_title%')

        # Assert.
        self.assertEqual(
            '([^/]+)/Content/([^/]+)/([^/]+)/([^/]+/|)([^/]+)$',
            path_pattern.path_pattern_regexp.pattern,
            'The built pattern not equals with the expected one.')

    def test_06_collectible(self):

        # Arrange.
        path_pattern = PathPattern('([^/]*)', ['a'], 1)

        # Arrange and act.
        collectible_1 = Collectible(['.md', '.txt'], path_pattern)
        collectible_2 = Collectible(['.gif', '.jpg'], path_pattern, 'apple')

        # Assert.
        self._compare_lists(['.md', '.txt'], collectible_1.extensions)
        self.assertEqual(path_pattern, collectible_1.path_pattern, 'PathPattern object has been tampered.')
        self.assertEqual(None, collectible_1.token, 'Token should be None.')
        self._compare_lists(['.gif', '.jpg'], collectible_2.extensions)
        self.assertEqual(path_pattern, collectible_2.path_pattern, 'PathPattern object has been tampered.')
        self.assertEqual('apple', collectible_2.token, 'Invalid token.')

    def test_07_nodes(self):

        # Act.
        node = CategorizedNode('/foo/bar.txt')
        node.meta['a1'] = 'foo'
        node.meta['c3'] = 'bar'

        uncategorized_node_1 = UncategorizedNode('/foo/bar')
        uncategorized_node_2 = UncategorizedNode('/foo/bar', uncategorized_node_1)
        uncategorized_node_3 = UncategorizedNode('/foo/bar', uncategorized_node_1)

        # Assert.
        self.assertEqual(node.path, '/foo/bar.txt')
        self.assertEqual(node.meta['a1'], 'foo')
        self.assertEqual(node.meta['c3'], 'bar')

        self.assertEqual(uncategorized_node_1.parent, None, 'Wrong parent for Node 1.')
        self.assertEqual(uncategorized_node_2.parent, uncategorized_node_1, 'Wrong parent for Node 2.')
        self.assertEqual(uncategorized_node_3.parent, uncategorized_node_1, 'Wrong parent for Node 3.')

    def test_08_revision_filter(self):

        # Arrange.
        revision_filter = DirectoryFilter('^[0-9]{8} [0-9]{6}$')

        # Act and assert.
        result = revision_filter.apply_filter('Apple/Banana/20110408 123452/Cherry')
        self.assertEqual(True, result, 'This path is a revision.')
        result = revision_filter.apply_filter('Apple/Banana/Cherry/Date')
        self.assertEqual(True, result, 'Result is not cached correctly.')
        result = revision_filter.leave_scope()
        result = revision_filter.apply_filter('Apple/Banana/Cherry/Date')
        self.assertEqual(False, result, 'This path is not a revision.')

    def test_09_indexer_policy(self):

        # Arrange.
        collectible_1 = Collectible(['.avi', '.mp4'], 'Some/%video%/path', 'video')
        collectible_2 = Collectible(['.srt', '.sub'], '%Some%/%subtitle%/%path%', 'subtitle')
        collectibles = [collectible_1, collectible_2]

        collector = TestCollector()

        # Act.
        policy = IndexerPolicy(collector, collectibles, None)

        # Assert.
        self.assertEqual(collector, policy.collector, 'Wrong Collector.')
        self._compare_unordered_lists(['.avi', '.mp4', '.srt', '.sub'], policy.extensions)
        self._compare_unordered_lists([], policy.filters)
        self.assertEqual(collectible_1, policy.get_collectible('.avi'), 'Wrong Collectible.')
        self.assertEqual(collectible_1, policy.get_collectible('.mp4'), 'Wrong Collectible.')
        self.assertEqual(collectible_2, policy.get_collectible('.srt'), 'Wrong Collectible.')
        self.assertEqual(collectible_2, policy.get_collectible('.sub'), 'Wrong Collectible.')

    def test_10_path_analyzer(self):

        # Arrange.
        tag_config = TagConfig('%', '%', None, {'a' : '([^/]+)', 'b' : '([^/]+)'})
        path_pattern = PathPatternAnalyzer().parse(tag_config, '%a%/Fix/%b%')
        collectible = Collectible(['.hey'], path_pattern)
        collector = TestCollector()
        policy = IndexerPolicy(collector, [collectible])

        # Act.
        path_analyzer = PathAnalyzer(policy)
        path_analyzer.enter('Test')
        path_analyzer.enter('Foo')
        path_analyzer.enter('Fix')
        path_analyzer.enter('Bar')
        path_analyzer.analyze('Test/Foo/Fix/Bar', '.hey')
        path_analyzer.analyze('Test/Foo/Fix/Bar2', '.ho')
        path_analyzer.leave()
        path_analyzer.leave()
        path_analyzer.enter('Fix2')
        path_analyzer.analyze('Test/Foo/Fix2/Test2/Bar3', '.hey')
        path_analyzer.leave()
        path_analyzer.leave()
        path_analyzer.leave()
        path_analyzer.leave()

        # Assert.
        self._compare_path_lists(['Test/Foo/Fix/Bar.hey'], collector.collected_categorized_paths, 0, 'categorized')
        self._compare_path_lists(
            ['Test/Foo/Fix2/Test2/Bar3.hey'],
            collector.collected_uncategorized_paths,
            0,
            'uncategorized')

    def test_11_indexer(self):

        # Arrange.
        tag_patterns = {
            'episode_title' : '([^/]+)',
            'language' : '([^/]+)',
            'languages' : '([^/]+)',
            'quality' : '([^/]+)',
            'title' : '([^/]+)'}
        tag_config = TagConfig('%', '%', ('any', '[^/]+'), tag_patterns)
        path_pattern_analyzer = PathPatternAnalyzer()
        video_pattern = path_pattern_analyzer.parse(
            tag_config,
            '%title%/Content/%quality%/%languages%/%any%/%episode_title%')
        subtitle_pattern = path_pattern_analyzer.parse(
            tag_config,
            '%title%/Subtitle/%quality%/%languages%/%language%/%any%/%episode_title%')

        collector = TestCollector()
        collectibles = [
            Collectible(['.avi', '.mp4'], video_pattern, 'video'),
            Collectible(['.srt'], subtitle_pattern, 'subtitle')]
        test_filter_factory = TestFilterFactory()

        indexer_policy = IndexerPolicy(collector, collectibles, test_filter_factory)
        indexer_policy.tag_any = 'any'

        indexer = Indexer()
        indexer.add_directory(self._helper.root_path)
        indexer.add_policy(indexer_policy)

        # Act.
        indexer.index()

        # Assert.
        self._compare_path_lists(
            self._environment.fake_categorized_files,
            collector.collected_categorized_paths,
            len(self._helper.files_path) + 1,
            'categorized')
        self._compare_path_lists(
            self._environment.fake_uncategorized_files,
            collector.collected_uncategorized_paths,
            len(self._helper.files_path) + 1,
            'uncategorized')

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _assert_raises_with_message(self, exception_type, msg, func, *args, **kwargs):

        does_exception_type_match = False

        try:
            func(*args, **kwargs)
        except Exception as exception:
            if isinstance(exception, exception_type):
                does_exception_type_match = True

        self.assertTrue(does_exception_type_match, msg)

    def _compare_dictionaries(self, expected_dict, actual_dict):

        if expected_dict is None:
            self.assertEqual(None, actual_dict, 'There are no expected items, but the actual dictionary is not None.')
        else:
            self.assertNotEqual(None, actual_dict, 'There are no items in the actual dictionary.')

        self.assertEqual(
            len(expected_dict),
            len(actual_dict),
            'The length of the expected and the actual lists differ.')

        for item in expected_dict.items():
            expected_key = item[0]
            if expected_key not in actual_dict:
                self.fail('The key {} is not present in the actual dictionary.'.format(expected_key))
            self.assertEqual(
                item[1],
                actual_dict[expected_key],
                'The value for the following key differ in expected and in actual lists: {}.'.format(expected_key))

    def _compare_lists(self, expected_list, actual_list):

        if expected_list is None:
            self.assertEqual(None, actual_list, 'There are no expected items, but the actual list is not None.')
        else:
            self.assertNotEqual(None, actual_list, 'There are no items in the actual list.')

        self.assertEqual(
            len(expected_list),
            len(actual_list),
            'The length of the expected and the actual lists differ.')

        for i in range(0, len(expected_list)):
            self.assertEqual(
                expected_list[i],
                actual_list[i],
                'The following items differ in expected and in actual lists: {}, {}.'.format(
                    expected_list[i],
                    actual_list[i]))

    def _compare_path_lists(self, expected_paths, actual_paths, offset, name):

        name = name.upper()
        processed_indices = []

        for actual_path in actual_paths:

            match = False
            for i in range(0, len(expected_paths)):
                if actual_path[offset:] == expected_paths[i]:
                    self.assertNotIn(
                        i,
                        processed_indices,
                        expected_paths[i] + ' is in the ' + name + ' list more than once.')
                    processed_indices.append(i)
                    match = True
                    break

            self.assertTrue(match, actual_path[offset:] + ' is not expected in ' + name + ' list.')

        self.assertEqual(len(processed_indices), len(expected_paths), name + ' list is not complete.')

    def _compare_unordered_lists(self, expected_list, actual_list):

        if expected_list is None:
            self.assertEqual(None, actual_list, 'There are no expected items, but the actual list is not None.')
        else:
            self.assertNotEqual(None, actual_list, 'There are no items in the actual list.')

        self.assertEqual(
            len(expected_list),
            len(actual_list),
            'The length of the expected and the actual lists differ.')

        for i in range(0, len(expected_list)):
            if expected_list[i] not in actual_list:
                self.fail('Actual list does not contain the expected item: ' + expected_list[i] + '.')
        for i in range(0, len(actual_list)):
            if actual_list[i] not in expected_list:
                self.fail('Actual list contains an unexpected item: ' + actual_list[i] + '.')

########################################################################################################################
# Mocked classes.
########################################################################################################################

class TestCollector(Collector):

    def __init__(self):

        self.collected_categorized_paths = []
        self.collected_uncategorized_paths = []

    def collect_categorized(self, categorized_nodes):

        for item in categorized_nodes:
            self.collected_categorized_paths.append(item.path)

    def collect_uncategorized(self, uncategorized_nodes):

        for item in uncategorized_nodes:
            self.collected_uncategorized_paths.append(item.path)

class TestFilterFactory(PathFilterFactory):

    def create_filters(self):

        return [DirectoryFilter('^[0-9]{8} [0-9]{6}$')]

########################################################################################################################
# Main.
########################################################################################################################

if __name__ == '__main__':

    unittest.main()
