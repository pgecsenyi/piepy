#!/bin/sh
python3 -m pylint --rcfile=.pylintrc app bll dal indexing multimedia testing web > report_code_quality.txt
