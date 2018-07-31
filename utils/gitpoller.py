# Simple Git Poller utility - notices new commits and starts a subprocess on change
# author: Mario De Armas
# date: 2018.08.03
# version: 1.0

import sys
import json
import yaml
import requests
import urllib
import collections
import os
import subprocess
import time
import datetime

# TODO: remove this warning disabling statement!
requests.packages.urllib3.disable_warnings()

# open tool configuration file and load contents
CONFIG_FILE = sys.argv[1]
print "[INFO] CONFIG_FILE: " + CONFIG_FILE
file = open(CONFIG_FILE, "r")
config = yaml.load(file)
file.close()

# parse file contents and define git api endpoint and account/repo/branch info
HOST = config["hostURL"]
API_ENDPOINT = HOST + config["apiEndpoint"]
USERID = config["userID"]  # not used by this tool (TODO: add if GitHub needs it in the future)
PASSWORD = config["password"]  # not used by this tool (TODO: add if GitHub needs it in the future)
HEADERS = {'Content-Type': 'application/json'}
# define git information for use by loop
GIT_ACCOUNT = config["account"]
GIT_REPOBRANCHES = config["repoBranches"]
CHANGE_ACTION = config["executeOnChange"]
print "[INFO] API_ENDPOINT: " + API_ENDPOINT
print "[INFO] GIT INFO {account}: " + json.dumps(GIT_ACCOUNT)
print "[INFO] GIT INFO {repo/branches}: " + json.dumps(GIT_REPOBRANCHES)


# "watch for changes" (i.e. loop forever)... until Ctrl+C stops program execution
while True:
    # reset git information back to neutral
    changeDetected = False;

    # check change through all known repo branches...
    for branch in GIT_REPOBRANCHES:
        print "------------------------------------------------------------------------------"
        print "[INFO] Poll git branch: " + json.dumps(branch)

        try:
            fileGitTracker = open(branch["repo"] + "_" + branch["branch"] + ".gitwatch","r")
            lastKnownCommitSHA = fileGitTracker.readline()
            fileGitTracker.close()
        except IOError as e:
            lastKnownCommitSHA = ""

        # fetch git repo branch metadata
        r = requests.get(url = API_ENDPOINT + "/repos/" + GIT_ACCOUNT + "/" + branch["repo"] + "/branches/" + branch["branch"],
                        auth = (USERID,PASSWORD),
                        headers = HEADERS,
                        verify = False)

        # DEBUG: display fetched repo/branch metadata
        #print json.dumps(json.loads(r.text))

        # decode last known commit value provide by API call results
        gitReportedLastCommitSHA = json.loads(r.text)["commit"]["sha"]
        print "[INFO]   gitReportedLastCommitSHA: " + gitReportedLastCommitSHA
        print "[INFO]   lastKnownCommitSHA      : " + lastKnownCommitSHA

        if (gitReportedLastCommitSHA != lastKnownCommitSHA):
            # change was detected in at least one of the watched branches...
            changeDetected = True
            # store new discovered commit SHA value (for reference later)
            fileGitTracker = open(branch["repo"] + "_" + branch["branch"] + ".gitwatch","w+")
            fileGitTracker.write(gitReportedLastCommitSHA)
            fileGitTracker.close()

        print "[INFO] changeDetected: " + str(changeDetected) + "  [ " + str(datetime.datetime.now()) + " ]"

    # check if we need to trigger a rebuild of repos...
    if (changeDetected == True):
        # invoke subprocess (and wait -- block -- until it has completed)
        #subprocess.call(CHANGE_ACTION)
        hello = "world"

    # wait a little bit before checking with git again (polling)
    time.sleep(10) # seconds


# you will never reach here b/c of infinite while loop
exit()

# GitHub api used in above loop (for reference of future changes by GitHub):
#HTTP GET https://api.github.com/repos/<account>/<repo-name>/branches/<branch-name>
