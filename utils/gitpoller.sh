#!/usr/bin/env bash
python -u gitpoller.py idlewis-branches.gitpoller 2>&1 | tee -a gitpoller.log
