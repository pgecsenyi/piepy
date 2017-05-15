"""
Playlist Data Access Layer unit tests
"""

# pylint: disable=too-many-public-methods

import unittest

from dal.context.dbcontext import DbContext
from dal.playlist.entities import NewPlaylist
from dal.playlist.entities import NewPlaylistTrack
from dal.playlist.entities import PlaylistHeader
from dal.playlist.playlistdatahandler import PlaylistDataHandler
from multimedia.constants import AUDIO_OUTPUT_DIGITAL
from testing.playlisttestenvironment import PlaylistTestEnvironment
from testing.testhelper import TestHelper

class PlaylistDalTest(unittest.TestCase):

    ####################################################################################################################
    # Initialization and cleanup.
    ####################################################################################################################

    @classmethod
    def setUpClass(cls):

        # Set private static attributes.
        cls._playlist_id = 0

        # Create TestHelper.
        cls._helper = TestHelper()
        cls._playlist_data_handler = PlaylistDataHandler(DbContext(cls._helper.playlist_database_path))
        cls._helper.add_environment(PlaylistTestEnvironment(cls._playlist_data_handler))

        # Create test database.
        cls._helper.create_database()

    @classmethod
    def tearDownClass(cls):

        cls._helper.clean()

    ####################################################################################################################
    # Test methods.
    ####################################################################################################################

    def test_1_insert_playlist(self):

        # Arrange.
        new_tracks = [
            NewPlaylistTrack('audio', '01 Song one', '/test/Artist/Album/01 Song One.mp3', AUDIO_OUTPUT_DIGITAL),
            NewPlaylistTrack('audio', '02 Song Two', '/test/Artist/Album/02 Song Two.mp3', AUDIO_OUTPUT_DIGITAL),
            NewPlaylistTrack('video', 'Funny', '/test/Video/Funny.mp4', AUDIO_OUTPUT_DIGITAL)]
        new_playlist = NewPlaylist('The best playlist', new_tracks)

        # Act.
        playlist_id = PlaylistDalTest._playlist_data_handler.insert_playlist(new_playlist)

        # Assert.
        self.assertNotEqual(playlist_id, None, 'Playlist ID is not set correctly.')

        PlaylistDalTest._playlist_id = playlist_id

    def test_2_retrieve_playlist_headers(self):

        # Act.
        playlist_headers = PlaylistDalTest._playlist_data_handler.retrieve_playlist_headers()

        # Assert.
        self.assertEqual(
            playlist_headers[0].playlist_id,
            PlaylistDalTest._playlist_id,
            'Playlist ID is not set correctly.')
        self.assertEqual(playlist_headers[0].title, 'The best playlist', 'Playlist title is not set correctly.')

    def test_3_retrieve_playlist(self):

        # Act.
        playlist = PlaylistDalTest._playlist_data_handler.retrieve_playlist(PlaylistDalTest._playlist_id)

        # Assert.
        self.assertEqual(playlist.playlist_id, PlaylistDalTest._playlist_id, 'Playlist ID is not set correctly.')
        self.assertEqual(playlist.title, 'The best playlist', 'Playlist title is not set correctly.')
        self._check_tracks(playlist.tracks)

    def test_4_update_playlist(self):

        # Arrange.
        playlist_header = PlaylistHeader(PlaylistDalTest._playlist_id, 'The best playlist (updated)')

        # Act.
        PlaylistDalTest._playlist_data_handler.update_playlist(playlist_header)

        # Assert.
        playlist_headers = PlaylistDalTest._playlist_data_handler.retrieve_playlist_headers()

        self.assertEqual(
            playlist_headers[0].playlist_id,
            PlaylistDalTest._playlist_id,
            'Playlist ID has changed after update.')
        self.assertEqual(
            playlist_headers[0].title,
            'The best playlist (updated)',
            'The title of the updated playlist is incorrect.')

    def test_6_retrieve_updated_playlist(self):

        # Act.
        playlist = PlaylistDalTest._playlist_data_handler.retrieve_playlist(PlaylistDalTest._playlist_id)

        # Assert.
        self.assertEqual(playlist.playlist_id, PlaylistDalTest._playlist_id, 'Playlist ID is not set correctly.')
        self.assertEqual(playlist.title, 'The best playlist (updated)', 'Playlist title is not set correctly.')
        self._check_updated_tracks(playlist.tracks)

    def test_7_delete_retrieve_playlist(self):

        # Act.
        PlaylistDalTest._playlist_data_handler.delete_playlist(PlaylistDalTest._playlist_id)
        playlists = PlaylistDalTest._playlist_data_handler.retrieve_playlist_headers()

        # Assert.
        self.assertEqual(playlists, None, 'The list of playlists is not empty after delete.')

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _check_tracks(self, tracks):

        self.assertNotEqual(tracks, None, 'The list of tracks is empty.')
        self.assertTrue(len(tracks) == 3, 'The length of the result list is wrong.')

        self.assertEqual(tracks[0].category, 'audio', 'Wrong category for the first item.')
        self.assertEqual(tracks[0].path, '/test/Artist/Album/01 Song One.mp3', 'Wrong path for the first item.')
        self.assertEqual(tracks[0].title, '01 Song one', 'Wrong title for the first item.')

        self.assertEqual(tracks[1].category, 'audio', 'Wrong category for the second item.')
        self.assertEqual(
            tracks[1].path,
            '/test/Artist/Album/02 Song Two.mp3',
            'Wrong path for the second item.')
        self.assertEqual(tracks[1].title, '02 Song Two', 'Wrong path for the second item.')

        self.assertEqual(tracks[2].category, 'video', 'Wrong category for the third item.')
        self.assertEqual(tracks[2].path, '/test/Video/Funny.mp4', 'Wrong path for the third item.')
        self.assertEqual(tracks[2].title, 'Funny', 'Wrong title for the third item.')

    def _check_updated_tracks(self, tracks):

        self.assertNotEqual(tracks, None, 'The list of playlists is empty.')
        self.assertTrue(len(tracks) == 3, 'Wrong number of items in the playlist.')

        self.assertEqual(tracks[0].category, 'audio', 'Wrong category for the first item.')
        self.assertEqual(
            tracks[0].path,
            '/test/Artist/Album/01 Song One.mp3',
            'Wrong path for the first item.')
        self.assertEqual(tracks[0].title, '01 Song one', 'Wrong title for the first item.')
