**`Git Commit Poller / Watcher`**
=======================================================================

- Background:  
  As part of the [OpenMRS 2.1.3 Mirebalais: Oncology Regimen Ordering & Dashboard Support](https://github.com/openmrs/openmrs-module-oncology) project, we wanted to
  quickly setup a no-frills CI build/test server that monitored several Git repo branches
  for changes (i.e. "commits") and triggered the build pipeline. With more time and in a
  larger project, teams would use tools like Jenkins/Travis and take advantage of web hooks
  feature to fullfil similar need. We did not need (or want) that level of devops tooling
  investment so I wrote this `gitpoller` utility to basically perform that function for us.

- Setup:
  To start using GITPOLLER tool, download contents of the following directories onto your development environment:
  - ["\utils"](https://github.com/dearmasm/openmrs-module-oncology/tree/master/utils): collection of different handy utils, including GITPOLLER tool

- Usage information:
  - First, you must create an GITPOLLER tool *git input file* which provides tool with the required GitHub server api endpoint and connectivity parameters, as well as GitHub `repos` and `branches` to be monitored by tool.
  You can use the `*.gitpoller` example available in this project's [/util](https://github.com/dearmasm/openmrs-module-oncology/edit/master/utils) directory as a starting template.
     ```yaml
     $ cat idlewis-branches.gitpoller
     # git account and repo being watched
     hostURL: "https://api.github.com"
     apiEndpoint: ""
     userID: <github userid>
     password: <github apikey>
     account: "idlewis"
     repoBranches:
         - # repo/branch 1
           repo: "openmrs-core"
           branch: "integration"
         - # repo/branch 2
           repo: "openmrs-module-webservices.rest"
           branch: "integration"

     # execute this action when change is detected
     executeOnChange: "/home/dearmasm/build/build.sh"
     ```
     ```bash
     $cp idlewis-branches.gitpoller mygitrepo-branches.gitpoller

     $vi mygitrepo-branches.gitpoller
     ```
     Edit the new file and add your specific GitHub connectivity and repo/branches details. Notice an entry for what
     action to take (execute) on detecting a change in any of the repo/branches.

- Example:
```bash
$ cat gitpoller-idlewis.sh
#!/usr/bin/env bash
python -u gitpoller.py idlewis-branches.gitpoller 2>&1 | tee -a gitpoller.log
```

```bash
$ ./gitpoller-idlewis.sh
SIMPLE GIT POLLER UTILITY v1.0 (20180803)...
[INFO] CONFIG_FILE: idlewis-branches.gitpoller
[INFO] API_ENDPOINT: https://api.github.com
[INFO] GIT INFO {account}: "idlewis"
[INFO] GIT INFO {repo/branches}: [{"repo": "openmrs-core", "branch": "integration"}, {"repo": "openmrs-module-webservices.rest", "branch": "integration"}]
------------------------------------------------------------------------------
[INFO] Poll git branch: {"repo": "openmrs-core", "branch": "integration"}
[INFO]   gitReportedLastCommitSHA: 3190bfc5b05dce62e6521dd37660bb299ac49e34
[INFO]   lastKnownCommitSHA      : f25014e8a34e4f82a589738fe9ed98b016f73f2c
[INFO] changeDetected: True  [ 2018-08-02 01:16:02.604649 ]
------------------------------------------------------------------------------
[INFO] Poll git branch: {"repo": "openmrs-module-webservices.rest", "branch": "integration"}
[INFO]   gitReportedLastCommitSHA: ba3c6b80a7e4d93bfaf4a5528e659850c48ae427
[INFO]   lastKnownCommitSHA      : 096fbc61a6028c65163afbbfb4715b6417463dfc
[INFO] changeDetected: True  [ 2018-08-02 01:16:02.752477 ]
[INFO] executing change process: /home/dearmasm/build/build.sh

===========================================================
BUILD CORE...
===========================================================
Already up-to-date.
OpenJDK 64-Bit Server VM warning: ignoring option PermSize=512m; support was removed in 8.0
OpenJDK 64-Bit Server VM warning: ignoring option MaxPermSize=1024m; support was removed in 8.0
. . .
```
>>>Note: in the above example, the gitpoller detects that there are new commits on each of the branches being watched (note that the SHA values are different) and then triggers the `executeOnChange` command as a subprocess (it stops any further polling to GitHub until subprocess completes). When subprocess completes (in this case it is a Maven build task that will take approx 15min), the poller script will then sleep for 30min and then attempt to poll GitHub resources again (loop), thus repeating this cycle every 30min or so (depending if a build was kicked off or not during the cycle).

- Implementation Notes:  
    - The tool is written in `Python 3` language. The key implementation file is [gitpoller.py](https://github.com/dearmasm/openmrs-module-oncology/edit/master/utils/gitpoller.py). There is a bash-friendly convenience wrapper included [gitpoller-idlewis.sh](https://github.com/dearmasm/openmrs-module-oncology/edit/master/utils/gitpoller-idlewis.sh) that can be used to launch GITPOLLER tool which redirects the stderr/stdout to a log file and console.  

    - The tool cycle sleep time is preset to 30min inside Python code. You can modify the value by just editing code line:
    ```python
    # wait a little bit before checking with git again (polling)
    time.sleep(1800) # in seconds (i.e. check for change every 30mins)
    ```

    - The tool uses several specialized Python package libraries which will usually require installing manually (see next section on tool requisites).  

- Python Prerequisites:
  - MacOS (Mavericks or higher) instructions:
    1. install python 2.7 or higher, test that you can run it from command-line (type ```exit()``` to quit python prompt)
       ```
          ibmmacbookmario:utils dearmasm$ python
          Python 2.7.10 (default, Oct  6 2017, 22:29:07)
          [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)] on darwin
          Type "help", "copyright", "credits" or "license" for more information.
          >>>
    2. install python yaml and requests libraries
       ```
          sudo easy_install pip
          brew install libyaml
          sudo python -m easy_install pyyaml
          sudo pip install requests
          sudo pip install objdict
          sudo pip install enum

    3. test python+yaml lib is working
       ```
          ibmmacbookmario:utils dearmasm$ ls -l test.*
          -rw-r--r--  1 dearmasm  staff  96 Jul 23 09:52 test.py
          -rw-r--r--  1 dearmasm  staff  45 Jul 23 09:13 test.yaml
          ibmmacbookmario:utils dearmasm$ python test.py
          Hello World!
          {'hello': {'go': True, 'world': 123, 'here': 'we'}}

- Linux (Ubuntu or similar) instructions:
    1. install python 2.7 or higher, test that you can run it from command-line (type ```exit()``` to quit python prompt)

    2. install python yaml and requests libraries
       ```
          sudo apt install python-setuptools
          sudo easy_install pip
          sudo python -m easy_install pyyaml
          sudo pip install requests
          sudo pip install objdict
          sudo pip install enum

    3. test python+yaml lib is working
       ```
          $ ls -l test.*
          -rw-r--r--  1 dearmasm  staff  96 Jul 23 09:52 test.py
          -rw-r--r--  1 dearmasm  staff  45 Jul 23 09:13 test.yaml
          $ python test.py
          Hello World!
          {'hello': {'go': True, 'world': 123, 'here': 'we'}}
       ```
