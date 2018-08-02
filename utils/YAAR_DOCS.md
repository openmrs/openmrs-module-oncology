**`Yet Another Automated Regimen (YAAR)`** management tool
=======================================================================

- Background:  
  As part of the [OpenMRS 2.1.3 Mirebalais: Oncology Regimen Ordering & Dashboard Support](https://github.com/openmrs/openmrs-module-oncology) project, we had a need to
  constantly create/update/retire `OrderSet` objects in many OpenMRS platform instances.  
  The repetitive demands and laborious task to structure HTTP requests with attributes and many UUIDs.  
  Therefore, we created a small and easy to use utility that can process chemotherapy regimen treatments
  as YAML metadata files and manage the OpenMRS REST API "back-end" processing to implement the desired lifecycle operations of add, get, update, retire of `OrderSet`'s.
  We giveback to the OpenMRS community this handy utility so that it can benefit others as they
  work to adopt support to their platforms for `OrderSet` templates.

- Setup:
  To start using YAAR tool, download contents of the following directories onto your development environment:
  - ["\utils"](https://github.com/dearmasm/openmrs-module-oncology/tree/master/utils): collection of different handy utils, including YAAR tool
  - ["\regimens"](https://github.com/dearmasm/openmrs-module-oncology/tree/master/regimens): reference examples of chemotherapy regimens created as part of our project  


- Usage information:
  - First, you must create an YAAR tool *server configuration file* to provide the YAAR tool with the required OpenMRS server api endpoint connectivity parameters.
  You can use the `*.conf` examples available in this project's [/util](https://github.com/dearmasm/openmrs-module-oncology/tree/master/utils) directory as starting templates.
     ```yaml
     $ cat localhost-server.conf
     # YAAR tool configuration file (YAML format)
     # author: Mario De Armas
     # date: 2018.08.03
     #
     # This file contains target OpenMRS server for use with YAAR utility:
     hostURL: "http://localhost:8080/openmrs"
     apiEndpoint: "/ws/rest/v1"
     userID: "admin"
     password: "Admin123"
     ```
     ```bash
     $cp localhost-server.conf myhost-server.conf

     $vi myhost-server.conf
     ```
     Edit new file and add your specific OpenMRS host connectivity details - which will be used later as a YAAR tool parameter file.


  - USAGE INFO
     ```bash
     $ ./yaar.sh
     OPENMRS REGIMEN ORDERSET TOOL v1.0 (20180803)...
     [INFO] usage: yaar -add <config-file> <input-file>
                   yaar -get <config-file> [<uuid>]
                   yaar -update <config-file> <input-file> <uuid>
                   yaar -retire <config-file> <uuid>
     ```  

      HTTP CODE | Notes |
     --- | --- |
      *`200`* | Regimen instance (`OrderSet`) was udpated or returned (depending on YAAR action command executed)
      *`201`* | New regimen instance (`OrderSet`) was created (it will have a unique UUID)      
      *`400`* | Problem with the new regimen metadata or POST request structure is invalid, enable YAAR debugging and review error detail
      *`500`* | Problem with OpenMRS server processing request, check server instance logs for insight

  - Enabling Debugging  
     The tool allows for debugging mode to be enabled by appending `+d` to tool action name. So, for example, `-add` becomes `-add+d` to enable debugging for that command execution instance.  
     Here is table with quick look up for enabling debug mode for the different action parameters tool supports:

     No Debug | Debug Mode |
     --- | --- |
      `-add` | `-add+d`
      `-get` | `-get+d`
      `-update` | `-update+d`
      `-retire` | `-retire+d`  




  - **`ADD`** (create new instance) a new regimen `OrderSet` on a target OpenMRS solution instance
     ```bash
     $ ./yaar.sh -add <openmrs-server.conf> <regimen-input-file>
     ```

  - **`GET all`** (existing) regimen `OrderSet` instances metadata from a target OpenMRS solution instance
     ```bash
     $ ./yaar.sh -get <openmrs-server.conf>
     ```

  - **`GET`** a specific (existing) regimen `OrderSet` instance metadata from a target OpenMRS solution instance
     ```bash
     $ ./yaar.sh -get <openmrs-server.conf> <regimen-uuid>
     ```

  - **`UPDATE`** an existing regimen `OrderSet` instance on a target OpenMRS solution instance
     ```bash session
     $ ./yaar.sh -update <openmrs-server.conf> <regimen-input-file> <regimen-uuid>
     ```

  - **`RETIRE`** an existing regimen `OrderSet` instance from a target OpenMRS solution instance
     ```bash session
     $ ./yaar.sh -retire <openmrs-server.conf> <regimen-uuid>
     ```


- Implementation Notes:  
    - The tool is written in `Python 3` language. The key implementation file is [yaar.py](https://github.com/dearmasm/openmrs-module-oncology/blob/master/utils/yaar.py). There is a bash-friendly convenience wrapper included [yaar.sh](https://github.com/dearmasm/openmrs-module-oncology/blob/master/utils/yaar.sh) that can be used to launch YAAR tool without having to type `python yaar.py` every time.  

    - The tool supports drug concepts UUID look ups and building the `OrderSet` HTTP body requests dynamically to match API/object structure (specifically it will encode order set list members properly and append new chemo order set attribute extensions added by IBM+PIH chemo treatment project).  

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
