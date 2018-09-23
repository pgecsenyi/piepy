import os
import shutil
import sys

from dal.configuration.config import Config
from dal.configuration.configmanager import ConfigManager

class TestHelper(object):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.test_service_base_url = 'http://localhost:8096/'

        # The path of the test files, database and so on.
        self._environments = []
        self._test_root_directory = self._determine_root_directory()
        self._test_paths = {
            'config' : os.path.join(self._test_root_directory, 'test.json'),
            'database_media' : os.path.join(self._test_root_directory, 'media.db'),
            'database_playlist' : os.path.join(self._test_root_directory, 'playlist.db'),
            'files' : os.path.join(self._test_root_directory, 'fakefiles')}

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def config_path(self):
        return self._test_paths['config']

    @property
    def files_path(self):
        return self._test_paths['files']

    @property
    def media_database_path(self):
        return self._test_paths['database_media']

    @property
    def playlist_database_path(self):
        return self._test_paths['database_playlist']

    @property
    def root_path(self):
        return self._test_root_directory

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def add_environment(self, environment):

        # Validate parameters.
        if environment is None:
            raise Exception('environment cannot be None.')

        # Store new environment.
        self._environments.append(environment)

    def build_url(self, url=''):

        return self.test_service_base_url + url

    def clean(self):

        try:
            if os.path.exists(self._test_root_directory):
                shutil.rmtree(self._test_root_directory)
        except OSError as exception:
            print('Error: {0} - {1}.'.format(exception.filename, exception.strerror))

    def create_configuration(self):

        # Create root path.
        self.create_root_path()

        # Generate and amend config.
        test_config = Config()
        test_config.create_default()
        test_config.database.lifetime = 3600
        test_config.database.path_media = self._test_paths['database_media']
        test_config.database.path_playlist = self._test_paths['database_playlist']
        test_config.indexing.video.subtitle_rules[0].directory = self._test_paths['files']
        test_config.indexing.video.video_rules[0].directory = self._test_paths['files']
        test_config.logging.enabled = False
        test_config.web.port = 8096

        # Save config.
        ConfigManager.save(self._test_paths['config'], test_config)

    def create_database(self):

        # Check if have test data.
        if self._environments is None or len(self._environments) <= 0:
            raise Exception('No test environments are defined.')

        # Create root path.
        self.create_root_path()

        # Create database.
        for environment in self._environments:
            environment.create_database()

    def create_files(self):

        # Check if have test data.
        if self._environments is None or len(self._environments) <= 0:
            raise Exception('No test environments are defined.')

        # Collect all the paths we need to create.
        all_fake_files = []
        for environment in self._environments:
            all_fake_files = all_fake_files + environment.get_all_fake_files()

        # Create root path.
        self.create_root_path()

        # Create empty files.
        for fake_path in all_fake_files:
            full_path = os.path.join(self._test_paths['files'], fake_path)
            directory = os.path.dirname(full_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(full_path):
                with open(full_path, 'w') as output:
                    output.write('')

    def create_root_path(self):

        if not os.path.exists(self._test_root_directory):
            os.makedirs(self._test_root_directory)

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _determine_root_directory(self):

        params = sys.argv
        param_count = len(params)

        for i in range(param_count):
            if params[i] == '-p' and param_count >= i + 1:
                return params[i + 1]

        return 'testdata'
