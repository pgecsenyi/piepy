#!/bin/sh
if [ $# -le 0 ]; then
  echo "Usage: ./run.sh <lint|test|start> <data file path>"
fi

action=$1
data_path=../data
if [ $# -ge 2 ]; then
  data_path=$2
fi

config_path="${data_path}/config.cfg"
report_lint_path="${data_path}/report_code_quality.txt"
report_test_path="${data_path}/report_testing.txt"

if [ $action = "clean" ]; then
  find . -type d -name '__pycache__' -exec rm -r "{}" \; 2> /dev/null
  rm -r testdata
elif [ $action = "lint" ]; then
  pipenv run pylint --rcfile=.pylintrc app bll dal indexing multimedia testing web > "${report_lint_path}"
elif [ $action = "test" ]; then
  echo 'TEST RESULTS\n============' > "${report_test_path}"
  echo '\n\nPlaylist Data Access Layer\n---------------------\n' >> "${report_test_path}"
  pipenv run python -m unittest -v testing.unittests.playlistdaltest 2>> "${report_test_path}"
  echo '\n\nVideo Data Access Layer\n-----------------------\n' >> "${report_test_path}"
  pipenv run python -m unittest -v testing.unittests.videodaltest 2>> "${report_test_path}"
  echo '\n\nIndexing\n--------\n' >> "${report_test_path}"
  pipenv run python -m unittest -v testing.unittests.indexingtest 2>> "${report_test_path}"
  echo '\n\nWeb\n---\n' >> "${report_test_path}"
  pipenv run python -m unittest -v testing.functionaltests.webtest 2>> "${report_test_path}"
elif [ $action = "start" ]; then
  pipenv run python main.py -c "${config_path}" -d
fi
