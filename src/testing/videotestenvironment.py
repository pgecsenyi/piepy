from testing.testenvironment import TestEnvironment

class VideoTestEnvironment(TestEnvironment):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, video_data_handler=None):

        ### Attributes from outside.
        self._data_handler = video_data_handler

        ### Private attributes.
        self._fake_categorized_files = [
            'Movie/Triple Payback/Content/HD (720p)/Hindi/Triple Payback (1988).mp4',
            'Movie/Triple Payback/Content/HD (720p)/Hungarian/Triple Payback (1988).avi',
            'Movie/Triple Payback/Subtitle/HD (720p)/Hindi/English/Triple Payback (1988).srt',
            'Movie/Battle of Impact/Content/HD (1080p)/English/Battle of Impact (1990).avi',
            'Movie/Battle of Impact/Content/HD (1080p)/German/Battle of Impact (1990).avi',
            'Movie/Battle of Impact/Content/HD (1080p)/Greek/Battle of Impact (1990).avi',
            'Movie/Battle of Impact/Subtitle/HD (1080p)/Greek/English/Battle of Impact (1990).srt',
            'Movie/Battle of Impact/Subtitle/HD (1080p)/Greek/Finnish/Battle of Impact (1990).srt',
            'Movie/Battle of Impact/Subtitle/HD (1080p)/Greek/German/Battle of Impact (1990).srt',
            'Movie/Double Prejudice/Content/LQ/English/Double Prejudice (7) Nothing New (Part 1) (1982).avi',
            'Series/Screw driver/Screw driver 4 (1975)/Content/LQ/English/Screw driver 4 (1975).avi',
            'Series/Screw driver/Screw driver 4 (1975)/Subtitle/LQ/English/English/Screw driver 4 (1975).srt',
            'Series/Compressor Head/Compressor Head (2014)/Content/HD (720p)/Finnish/Season 1/' \
                'Compressor Head [1x01] Variable Length Codes.avi',
            'Series/Compressor Head/Compressor Head (2014)/Content/HD (720p)/Greek/Season 1/' \
                'Compressor Head [1x01] Variable Length Codes.avi',
            'Series/Compressor Head/Compressor Head (2014)/Content/LQ/Greek/Season 1/' \
                'Compressor Head [1x01] Variable Length Codes.avi',
            'Series/Compressor Head/Compressor Head (2014)/Subtitle/HD (720p)/Finnish/English/Season 1/' \
                'Compressor Head [1x01] Variable Length Codes.srt',
            'Series/Compressor Head/Compressor Head (2014)/Subtitle/HD (720p)/Finnish/Greek/Season 1/' \
                'Compressor Head [1x01] Variable Length Codes.srt',
            'Series/Compressor Head/Compressor Head (2014)/Subtitle/HD (720p)/Finnish/Hungarian/Season 1/' \
                'Compressor Head [1x01] Variable Length Codes.srt',
            'Series/Compressor Head/Compressor Head (2014)/Subtitle/HD (720p)/Greek/Greek/Season 1/' \
                'Compressor Head [1x01] Variable Length Codes.srt',
            'Series/Compressor Head/Compressor Head (2014)/Content/HQ/English/Season 1/' \
                'Compressor Head [1x03] Markov Chain Compression.mp4',
            'Series/Compressor Head/Compressor Head (2014)/Content/HQ/Hungarian/Season 1/' \
                'Compressor Head [1x03] Markov Chain Compression.mp4',
            'Series/Compressor Head/Compressor Head (2014)/Content/LQ/English/Season 1/' \
                'Compressor Head [1x00] Introducing Compressor Head.avi',
            'Series/Compressor Head/Compressor Head (2014)/Content/LQ/English/Season 1/' \
                'Compressor Head [1x03] Markov Chain Compression.avi',
            'Series/Family/Content/LQ/English/Season 1/Family [01] Intro.avi']
        self._fake_uncategorized_files = [
            'Fun/Parodies/Chasing the ball.mp4',
            'Effects/Fades/Fades Nr. 1/Fade Out.mp4']
        self._fake_unexpected_files = [
            'Movie/Triple Payback/Subtitle/HD (720p)/Hindi/English/20090605 134256/Triple Payback (1988).srt']

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def fake_categorized_files(self):
        return self._fake_categorized_files

    @property
    def fake_uncategorized_files(self):
        return self._fake_uncategorized_files

    @property
    def fake_unexpected_files(self):
        return self._fake_unexpected_files

    ####################################################################################################################
    # TestEnvironment implementation.
    ####################################################################################################################

    def create_database(self):

        if self._data_handler is None:
            raise Exception('No VideoDataHandler available.')

        self._data_handler.creator.create_db()

    def get_all_fake_files(self):

        return self._fake_categorized_files + self._fake_uncategorized_files + self._fake_unexpected_files
