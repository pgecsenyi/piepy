#!/bin/sh
print_usage_then_exit()
{
    echo "Usage: ./run.sh <action> [<data path>]"
    echo "<action> can be one of the following: \"clean\", \"lint\", \"test\", \"start\"."
    exit 1
}

# Verify input parameters, decide what to do.
if [ $# -le 0 ] || [ $# -ge 3 ]; then
    print_usage_then_exit
fi

action=$1

# Run clean action.
if [ $action = "clean" ]; then
    find . -type d -name '__pycache__' -exec rm -r "{}" \; 2> /dev/null
    rm -r testdata 2> /dev/null
    exit 0
fi

# Run other actions, configure data path first.
data_path=../data
if [ $# -ge 2 ]; then
    data_path=$2
fi

config_path="${data_path}/config.cfg"
report_lint_path="${data_path}/report_code_quality.txt"
report_test_path="${data_path}/report_testing.txt"

if [ $action = "lint" ]; then
    pipenv run pylint --rcfile=.pylintrc app bll dal indexing multimedia test testing web > "${report_lint_path}"
elif [ $action = "test" ]; then
    pipenv run python test.py -p ../data/testdata 2> "${report_test_path}"
elif [ $action = "start" ]; then
    pipenv run python main.py -c "${config_path}" -d
else
    print_usage_then_exit
fi
