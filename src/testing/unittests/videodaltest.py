"""
Video Data Access Layer unit tests
"""

# pylint: disable=too-many-public-methods

import unittest

from dal.context.dbcontext import DbContext
from dal.video.videodatacache import VideoDataCache
from dal.video.videodatahandler import VideoDataHandler
from testing.testhelper import TestHelper
from testing.videotestenvironment import VideoTestEnvironment

class VideoDalTest(unittest.TestCase):

    ####################################################################################################################
    # Initialization and cleanup.
    ####################################################################################################################

    @classmethod
    def setUpClass(cls):

        cls._helper = TestHelper()
        cls._video_data_handler = VideoDataHandler(DbContext(cls._helper.media_database_path))
        cls._helper.add_environment(VideoTestEnvironment(cls._video_data_handler))
        cls._helper.create_database()

    @classmethod
    def tearDownClass(cls):

        cls._helper.clean()

    ####################################################################################################################
    # Test methods.
    ####################################################################################################################

    def test_1_cache_languages(self):

        # Arrange.
        cache = VideoDataCache()

        # Act.
        self._insert_languages_into_cache(cache)

        id_lang_hun_1 = cache.get_language_id('Hungarian')
        id_lang_lit_1 = cache.get_language_id('Lithuanian')

        cache.clear()

        id_lang_hun_2 = cache.get_language_id('Hungarian')
        id_lang_lit_2 = cache.get_language_id('Lithuanian')

        # Assert.
        self.assertEqual(id_lang_hun_1, 3)
        self.assertEqual(id_lang_hun_2, None)
        self.assertEqual(id_lang_lit_1, None)
        self.assertEqual(id_lang_lit_2, None)

    def test_2_cache_qualities(self):

        # Arrange.
        cache = VideoDataCache()

        # Act.
        self._insert_qualities_into_cache(cache)

        id_quality_lq_1 = cache.get_quality_id('LQ')
        id_quality_hd_1 = cache.get_quality_id('HD (720p)')

        cache.clear()

        id_quality_lq_2 = cache.get_quality_id('LQ')
        id_quality_hd_2 = cache.get_quality_id('HD (720p)')

        # Assert.
        self.assertEqual(id_quality_lq_1, 1)
        self.assertEqual(id_quality_lq_2, None)
        self.assertEqual(id_quality_hd_1, 4)
        self.assertEqual(id_quality_hd_2, None)

    def test_3_cache_titles(self):

        # Arrange.
        cache = VideoDataCache()

        # Act.
        self._insert_titles_into_cache(cache)

        id_title_uncategorized_1 = cache.get_title_id('(Uncategorized)')
        id_title_fruits_apple_1 = cache.get_title_id('Fruits - Apple', 2)
        id_title_fruits_apple_2 = cache.get_title_id('Fruits - Apple', 3)

        cache.clear()

        id_title_uncategorized_2 = cache.get_title_id('(Uncategorized)')
        id_title_fruits_apple_1_2 = cache.get_title_id('Fruits - Apple', 2)
        id_title_fruits_apple_2_2 = cache.get_title_id('Fruits - Apple', 3)

        # Assert.
        self.assertEqual(id_title_uncategorized_1, 2)
        self.assertEqual(id_title_uncategorized_2, None)
        self.assertEqual(id_title_fruits_apple_1, None)
        self.assertEqual(id_title_fruits_apple_1_2, None)
        self.assertEqual(id_title_fruits_apple_2, 4)
        self.assertEqual(id_title_fruits_apple_2_2, None)

    def test_4_language_retrieval(self):

        # Act.
        self._video_data_handler.creator.insert_language('English')
        self._video_data_handler.creator.insert_language('German')
        self._video_data_handler.creator.insert_language('Hungarian')
        id_hun_1 = self._video_data_handler.retriever.retrieve_language_id('Hungarian')
        self._video_data_handler.creator.insert_language('Hungarian')
        id_hun_2 = self._video_data_handler.retriever.retrieve_language_id('Hungarian')
        id_lit_1 = self._video_data_handler.retriever.retrieve_language_id('Lithuanian')

        self._video_data_handler.clear_cache()

        id_hun_3 = self._video_data_handler.retriever.retrieve_language_id('Hungarian')
        id_lit_2 = self._video_data_handler.retriever.retrieve_language_id('Lithuanian')

        # Assert.
        self.assertEqual(id_hun_1, 4)
        self.assertEqual(id_hun_2, 4)
        self.assertEqual(id_hun_3, 4)
        self.assertEqual(id_lit_1, None)
        self.assertEqual(id_lit_2, None)

    def test_5_quality_retrieval(self):

        # Act.
        self._video_data_handler.creator.insert_quality('LQ')
        self._video_data_handler.creator.insert_quality('HQ')
        id_hq = self._video_data_handler.retriever.retrieve_quality_id('HQ')
        self._video_data_handler.creator.insert_quality('HQ')
        id_hq_2 = self._video_data_handler.retriever.retrieve_quality_id('HQ')
        self._video_data_handler.creator.insert_quality('DVD')
        id_dvd = self._video_data_handler.retriever.retrieve_quality_id('DVD')

        self._video_data_handler.clear_cache()

        id_hq_3 = self._video_data_handler.retriever.retrieve_quality_id('HQ')

        # Assert.
        self.assertEqual(id_hq, 3)
        self.assertEqual(id_hq_2, 3)
        self.assertEqual(id_hq_3, 3)
        self.assertEqual(id_dvd, 4)

    def test_6_title_retrieval(self):

        # Act.
        self._video_data_handler.creator.insert_title('Apple')
        id_apple = self._video_data_handler.retriever.retrieve_title_id('Apple')
        self._video_data_handler.creator.insert_title('Apple')
        id_apple_2 = self._video_data_handler.retriever.retrieve_title_id('Apple')
        self._video_data_handler.creator.insert_title('Apple', 1)
        id_apple_3 = self._video_data_handler.retriever.retrieve_title_id('Apple')
        id_apple_4 = self._video_data_handler.retriever.retrieve_title_id('Apple', 1)
        self._video_data_handler.creator.insert_title('Banana', 1)
        id_banana_1 = self._video_data_handler.retriever.retrieve_title_id('Banana')
        id_banana_2 = self._video_data_handler.retriever.retrieve_lower_title_id('Banana')

        self._video_data_handler.clear_cache()

        id_apple_4 = self._video_data_handler.retriever.retrieve_title_id('Apple', 1)
        id_banana_3 = self._video_data_handler.retriever.retrieve_title_id('Banana')
        id_banana_4 = self._video_data_handler.retriever.retrieve_lower_title_id('Banana')

        # Assert.
        self.assertEqual(id_apple, 2)
        self.assertEqual(id_apple_2, 2)
        self.assertEqual(id_apple_3, 2)
        self.assertEqual(id_apple_4, 3)
        self.assertEqual(id_banana_1, None)
        self.assertEqual(id_banana_2, 4)
        self.assertEqual(id_apple_4, 3)
        self.assertEqual(id_banana_3, None)
        self.assertEqual(id_banana_4, 4)

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _insert_languages_into_cache(self, cache):

        cache.set_language_id('English', 1)
        cache.set_language_id('German', 2)
        cache.set_language_id('Hungarian', 3)

    def _insert_qualities_into_cache(self, cache):

        cache.set_quality_id('LQ', 1)
        cache.set_quality_id('HD (1080p)', 2)
        cache.set_quality_id('HQ', 3)
        cache.set_quality_id('HD (720p)', 4)
        cache.set_quality_id('DVD', 5)

    def _insert_titles_into_cache(self, cache):

        cache.set_title_id('Maci laci', 1)
        cache.set_title_id('(Uncategorized)', 2)
        cache.set_title_id('Fruits', 3, 2)
        cache.set_title_id('Fruits - Apple', 4, 3)
        cache.set_title_id('Fruits - Banana', 5, 3)
        cache.set_title_id('Fruits - Cherry', 6, 3)

########################################################################################################################
# Main.
########################################################################################################################

if __name__ == '__main__':

    unittest.main()
