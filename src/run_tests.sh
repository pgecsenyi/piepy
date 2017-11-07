#!/bin/sh
echo 'TEST RESULTS\n============' > report_testing.txt
echo '\n\nPlaylist Data Access Layer\n---------------------\n' >> report_testing.txt
pipenv run python -m unittest -v testing.unittests.playlistdaltest 2>> report_testing.txt
echo '\n\nVideo Data Access Layer\n-----------------------\n' >> report_testing.txt
pipenv run python -m unittest -v testing.unittests.videodaltest 2>> report_testing.txt
echo '\n\nIndexing\n--------\n' >> report_testing.txt
pipenv run python -m unittest -v testing.unittests.indexingtest 2>> report_testing.txt
echo '\n\nWeb\n---\n' >> report_testing.txt
pipenv run python -m unittest -v testing.functionaltests.webtest 2>> report_testing.txt
