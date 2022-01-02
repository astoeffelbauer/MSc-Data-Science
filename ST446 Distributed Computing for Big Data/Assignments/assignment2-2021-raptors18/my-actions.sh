#!/bin/bash
python -m pip install nltk
python -m pip install --upgrade pip
python -m nltk.downloader -d /usr/local/share/nltk_data all # check whether it is there.