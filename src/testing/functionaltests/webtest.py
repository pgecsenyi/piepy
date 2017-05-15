"""
Web unit tests
"""

# pylint: disable=too-many-public-methods

import time
import unittest

import requests

from testing.communicationhelper import get_json, put_json
from testing.functions import are_expected_items_in_list, are_expected_kv_pairs_in_list, \
                              get_item_from_embedded_dictionary
from testing.servermanager import ServerManager
from testing.testhelper import TestHelper
from testing.videotestenvironment import VideoTestEnvironment

class WebTest(unittest.TestCase):

    ####################################################################################################################
    # Initialization and cleanup.
    ####################################################################################################################

    @classmethod
    def setUpClass(cls):

        # Set private static attributes.
        cls._episode_title_id = 0
        cls._file_id = 0
        cls._language_id = 0
        cls._main_executable = 'main.py'
        cls._parent_id = 0
        cls._playlist_id = 0
        cls._quality_id = 0

        # Create TestHelper.
        cls._helper = TestHelper()
        cls._helper.add_environment(VideoTestEnvironment())

        # Create test configuration and files.
        cls._helper.create_configuration()
        cls._helper.create_files()

        # Create Server Manager and start the server.
        cls._server_manager = ServerManager(cls._main_executable, cls._helper.config_path)
        cls._server_manager.start()
        if not cls._server_manager.wait_for_initialization(cls._helper.test_service_base_url):
            print('The service is unavailable.')
            cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):

        cls._server_manager.stop()
        cls._helper.clean()

    ####################################################################################################################
    # Real test methods.
    ####################################################################################################################

    def test_1_rebuild(self):

        # Arrange.
        rebuild_url = WebTest._helper.build_url('rebuild')
        status_url = WebTest._helper.build_url('status')

        # Act.
        requests.get(rebuild_url)

        # Wait until database is building. Poll status in every 2 seconds.
        number_of_retries = 0
        result = ''
        while number_of_retries < 10:
            data = get_json(status_url)
            result = data['status']['synchronization']
            if result == 'not running':
                break
            number_of_retries += 1
            time.sleep(2)

        # Assert.
        self.assertEqual(result, 'not running', 'Rebuild failed.')

    def test_2_categories(self):

        # Arrange.
        url = WebTest._helper.build_url('categories')

        # Act.
        data = get_json(url)

        # Assert.
        are_expected_items_in_list(self, data, 'categories')
        are_expected_items_in_list(self, data['categories'], 'audio', 'image', 'video')

    def test_3_video_languages(self):

        # Arrange.
        url = WebTest._helper.build_url('video/languages')

        # Act.
        data = get_json(url)

        # Assert.
        expected_languages = ['(Uncategorized)', 'English', 'Finnish', 'German', 'Greek', 'Hindi', 'Hungarian']
        are_expected_items_in_list(self, data, 'languages')
        are_expected_kv_pairs_in_list(self, data['languages'], 'language', expected_languages)

        WebTest._language_id = get_item_from_embedded_dictionary(
            data['languages'],
            'language',
            'Greek',
            'id')

    def test_4_video_qualities(self):

        # Arrange.
        url = WebTest._helper.build_url('video/qualities')

        # Act.
        data = get_json(url)

        # Assert.
        expected_qualities = ['(Uncategorized)', 'LQ', 'HQ', 'HD (720p)', 'HD (1080p)']
        are_expected_items_in_list(self, data, 'qualities')
        are_expected_kv_pairs_in_list(self, data['qualities'], 'quality', expected_qualities)

        WebTest._quality_id = get_item_from_embedded_dictionary(
            data['qualities'],
            'quality',
            'HD (720p)',
            'id')

    def test_5_01_video_titles(self):

        # Arrange.
        url = WebTest._helper.build_url('video/titles')

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['(Uncategorized)', 'Triple Payback', 'Battle of Impact', 'Double Prejudice',
                           'Screw driver 4 (1975)', 'Compressor Head (2014)', 'Family']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

        WebTest._parent_id = get_item_from_embedded_dictionary(
            data['titles'],
            'title',
            'Compressor Head (2014)',
            'id')

    def test_5_02_video_titles_by_l(self):
        """
        Query video titles by language.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?language={}'.format(WebTest._language_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Battle of Impact', 'Compressor Head (2014)']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_03_video_titles_by_p(self):
        """
        Query video titles by parent.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?parent={}'.format(WebTest._parent_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = [
            'Compressor Head [1x01] Variable Length Codes',
            'Compressor Head [1x03] Markov Chain Compression',
            'Compressor Head [1x01] Variable Length Codes']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_04_video_titles_by_q(self):
        """
        Query video titles by quality.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?quality={}'.format(WebTest._quality_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Triple Payback', 'Compressor Head (2014)']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_05_video_titles_by_l_p(self):
        """
        Query video titles by language and parent.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?language={}&parent={}'.format(
            WebTest._language_id,
            WebTest._parent_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head [1x01] Variable Length Codes']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_06_video_titles_by_l_q(self):
        """
        Query video titles by language and quality.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?language={}&quality={}'.format(
            WebTest._language_id,
            WebTest._quality_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head (2014)']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_07_video_titles_by_p_q(self):
        """
        Query video titles by parent and quality.
        """

        # Arrange.
        url = WebTest._helper.build_url(
            'video/titles?parent={}&quality={}'.format(WebTest._parent_id, WebTest._quality_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head [1x01] Variable Length Codes']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

        WebTest._episode_title_id = get_item_from_embedded_dictionary(
            data['titles'],
            'title',
            'Compressor Head [1x01] Variable Length Codes',
            'id')

    def test_5_08_video_titles_by_sl(self):
        """
        Query video titles by subtitle language.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?subtitle={}'.format(WebTest._language_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head (2014)']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_09_video_titles_by_l_sl(self):
        """
        Query video titles by language and subtitle language.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?language={}&subtitle={}'.format(
            WebTest._language_id,
            WebTest._language_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head (2014)']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_10_video_titles_by_p_sl(self):
        """
        Query video titles by parent and subtitle language.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?parent={}&subtitle={}'.format(
            WebTest._parent_id,
            WebTest._language_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head [1x01] Variable Length Codes']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_11_video_titles_by_q_sl(self):
        """
        Query video titles by quality and subtitle language.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?quality={}&subtitle={}'.format(
            WebTest._quality_id,
            WebTest._language_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head (2014)']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_12_video_titles_by_l_p_sl(self):
        """
        Query video titles by language, parent and subtitle language.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?language={}&parent={}&subtitle={}'.format(
            WebTest._language_id,
            WebTest._parent_id,
            WebTest._language_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head [1x01] Variable Length Codes']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_13_video_titles_by_l_q_sl(self):
        """
        Query video titles by language, quality and subtitle language.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?language={}&quality={}&subtitle={}'.format(
            WebTest._language_id,
            WebTest._quality_id,
            WebTest._language_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head (2014)']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_5_14_video_titles_by_l_p_q_sl(self):
        """
        Query video titles by language, parent, quality and subtitle language.
        """

        # Arrange.
        url = WebTest._helper.build_url('video/titles?language={}&parent={}&quality={}&subtitle={}'.format(
            WebTest._language_id,
            WebTest._parent_id,
            WebTest._quality_id,
            WebTest._language_id))

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Compressor Head [1x01] Variable Length Codes']
        are_expected_items_in_list(self, data, 'titles')
        are_expected_kv_pairs_in_list(self, data['titles'], 'title', expected_titles)

    def test_6_search(self):

        # Arrange.
        url = WebTest._helper.build_url('search/family')

        # Act.
        data = get_json(url)

        # Assert.
        expected_titles = ['Family', 'Family [01] Intro']
        are_expected_items_in_list(self, data, 'videos')
        are_expected_kv_pairs_in_list(self, data['videos'], 'title', expected_titles)

    def test_7_details(self):

        # Arrange.
        url = WebTest._helper.build_url('video/details/{}'.format(WebTest._episode_title_id))

        # Act.
        data = get_json(url)

        # Assert.
        are_expected_items_in_list(self, data['details'], 'id', 'files', 'subtitles', 'title')
        self.assertEqual('Compressor Head [1x01] Variable Length Codes', data['details']['title'], 'Wrong title.')
        are_expected_kv_pairs_in_list(
            self,
            data['details']['files'],
            'language',
            ['Finnish', 'Greek', 'Greek'])
        are_expected_kv_pairs_in_list(
            self,
            data['details']['files'],
            'quality',
            ['HD (720p)', 'HD (720p)', 'LQ'])
        are_expected_kv_pairs_in_list(
            self,
            data['details']['subtitles'],
            'language',
            ['English', 'Greek', 'Greek', 'Hungarian'])
        WebTest._file_id = data['details']['files'][0]['id']

    def test_8_01_playlist_add(self):

        # Arrange.
        url = WebTest._helper.build_url('playlist/add')
        payload = {
            'title' : 'Test playlist',
            'tracks': [
                {'category' : 'video', 'file' : WebTest._file_id}]}

        # Act.
        data = put_json(url, payload)

        # Assert.
        self.assertEqual('Test playlist', data['playlist']['title'], 'Wrong title for the playlist.')

        WebTest._playlist_id = data['playlist']['id']

    def test_8_02_playlist_add_track(self):

        # Arrange.
        url = WebTest._helper.build_url('playlist/add-track')
        payload = {'playlist' : WebTest._playlist_id, 'category' : 'video', 'file' : WebTest._file_id}

        # Act.
        data = put_json(url, payload)

        # Assert.
        self.assertEqual('video', data['track']['category'], 'Wrong category.')
        self.assertEqual('Compressor Head [1x01] Variable Length Codes', data['track']['title'], 'Wrong title.')

    def test_8_03_playlists(self):

        # Arrange.
        url = WebTest._helper.build_url('playlist/all')

        # Act.
        data = get_json(url)

        # Assert.
        self.assertNotEqual(None, data['playlists'], 'There are no playlists in the response.')
        self.assertEqual(1, len(data['playlists']), 'Incorrect number of playlists.')
        self.assertEqual('Test playlist', data['playlists'][0]['title'], 'Incorrect playlist title.')
