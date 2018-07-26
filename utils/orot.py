import sys
import json
import yaml
import requests
import urllib
import collections

from objdict import ObjDict

# TODO: remove this warning disabling statement!
requests.packages.urllib3.disable_warnings()


def displayArgsHelp():
    print "[INFO] usage: orot -add <config-file> <input-file>"
    print "              orot -get <config-file> [<uuid>]"
    print "              orot -update <config-file> <input-file> <uuid>"
    print "              orot -retire <config-file> <uuid>"
    print "              orot -purge <config-file> <uuid>"

# start tool implementation
print "OPENMRS REGIMEN ORDERSET TOOL v1.0 (20180803)..."

# check if enough params were passed in...
if len(sys.argv) < 3:
    displayArgsHelp()
    exit()

# parse base tool parameters
ACTION = sys.argv[1]
CONFIG_FILE = sys.argv[2]
print "[INFO] ACTION: " + ACTION
print "[INFO] CONFIG_FILE: " + CONFIG_FILE
file = open(CONFIG_FILE, "r")
config = yaml.load(file)


# define api host & endpoint info
HOST = config["hostURL"]
API_ENDPOINT = HOST + config["apiEndpoint"]
USERID = config["userID"]
PASSWORD = config["password"]
HEADERS = {'Content-Type': 'application/json'}
print "[INFO] API_ENDPOINT: " + API_ENDPOINT


# if tool action is to fetch orderSet...
if ACTION == "-get":
    # if params include <uuid>, then use it
    if len(sys.argv) > 3:
        uuidOrderSetParam = "/" + sys.argv[3]   # uuid url path
    else:
        uuidOrderSetParam = ""  # fetch ALL orderSets

    # fetch orderSet(s) metadata
    r = requests.get(url = API_ENDPOINT + "/orderset" + uuidOrderSetParam + "?v=full",
                    auth = (USERID,PASSWORD),
                    headers = HEADERS,
                    verify = False)

    # display fetched orderSet metadata
    print json.dumps(json.loads(r.text), indent=4)
    exit()

# if tool action is to retire or purge an orderSet...
if (ACTION == "-retire") or (ACTION == "-purge"):
    # if params include <uuid>, then use it
    if len(sys.argv) > 3:
        uuidOrderSetParam = "/" + sys.argv[3]   # uuid url path
    else:
        # bad params list, exit
        displayArgsHelp()
        exit()

# if tool action is to purge an orderSet...
if (ACTION == "-purge"):
    # add an additional "purge=true" param to end of url
    uuidOrderSetParam.append("?purge=true")

    # retire orderSet
    r = requests.delete(url = API_ENDPOINT + "/orderset" + uuidOrderSetParam,
                    auth = (USERID,PASSWORD),
                    headers = HEADERS,
                    verify = False)

    print r
    exit()


# if tool action is to add or update a regimen orderSet...
if (ACTION == "-add") or (ACTION == "-update"):
    # if params include <input-file>, then use it
    if len(sys.argv) > 3:
        INPUT_FILE = sys.argv[3] # use <input-file>
    else:
        # bad params list, exit
        displayArgsHelp()
        exit()
else:
    # bad params list, exit
    displayArgsHelp()
    exit()

# read orderSet Regimen template file (uses a YAML schema)
print "[INFO] INPUT_FILE: " + INPUT_FILE
file = open(INPUT_FILE, "r")
regimen = yaml.load(file)

# build new orderSet's orderSetMember list in a loop...
for x in range(len(regimen["orderset"]["orders"])):

    print "[INFO] processing orderSetMember[",x,"]"

    # build orderSetMember number [x]...

    # DEBUG
    #print regimen["orderset"]["orders"][x]

    # prepare to query UUIDs that will be required during OrderSet creation phase
    # fetch UUIDs using metadata coded into OrderSet Regimen definition YAML source

    # use orderType encoded value
    order_type = urllib.quote(regimen["orderset"]["orders"][x]["type"])

    # fetch orderType UUID value
    r = requests.get(url = API_ENDPOINT + "/ordertype?v=full&q=" + order_type,
                     auth = (USERID,PASSWORD),
                     headers = HEADERS,
                     verify = False)

    # store fetched UUID
    uuidOrderType = json.loads(r.text)["results"][0]["uuid"]

    # use orderType concept encoded value
    #conceptCodeValue = regimen["orderset"]["orders"][x]["concept"].split(":")
    conceptCodeValue = regimen["orderset"]["orders"][x]["concept"]

    # fetch orderType Concept UUID value
    r = requests.get(url = API_ENDPOINT + "/concept?locale='en'&q=" + conceptCodeValue,
                     auth = (USERID,PASSWORD),
                     headers = HEADERS,
                     verify = False)

    #rest/v1/concept?v=full&q="Aspirine"&locale="en"
    # TODO: not needed after all??!
    # fetch orderType Concept UUID value
    #r = requests.get(url = API_ENDPOINT + "/conceptreferenceterm?v=full&codeOrName=" + conceptCodeValue[1] + "&source=" + conceptCodeValue[x] + "?lang=en",
    #                 auth = (USERID,PASSWORD),
    #                 headers = HEADERS,
    #                 verify = False)

    #print "[DEBUG] concept result\n" + r.text

    # TODO: change to capture retrieved concept display name
    nameOrderTypeConcept = conceptCodeValue #json.loads(r.text)["results"][0]["display"]
    uuidOrderTypeConcept = json.loads(r.text)["results"][0]["uuid"]

    print "[INFO] uuidOrderType: " + uuidOrderType + "   [" + order_type + "]"
    print "[INFO] uuidOrderTypeConcept: " + uuidOrderTypeConcept + "   [" + nameOrderTypeConcept + "]"

    jsonOrderTemplate = ObjDict();
    jsonOrderTemplate.administrationInstructions = regimen["orderset"]["orders"][x]["administrationInstructions"]
    jsonOrderTemplate.dosingInstructions = ObjDict()
    jsonOrderTemplate.dosingInstructions.doseUnits = regimen["orderset"]["orders"][x]["dosingInstructions"]["doseUnits"]
    jsonOrderTemplate.dosingInstructions.frequency = regimen["orderset"]["orders"][x]["dosingInstructions"]["frequency"]
    jsonOrderTemplate.dosingInstructions.route = regimen["orderset"]["orders"][x]["dosingInstructions"]["route"]
    jsonOrderTemplate.dosingInstructions.dose = regimen["orderset"]["orders"][x]["dosingInstructions"]["dose"]
    jsonOrderTemplate.durationUnits = regimen["orderset"]["orders"][x]["durationUnits"]
    jsonOrderTemplate.duration = regimen["orderset"]["orders"][x]["duration"]
    # TODO: add this later when attributes are available
    #jsonOrderTemplate.relativeStartDay = regimen["orderset"]["orders"][x]["relativeStartDay"]
    jsonOrderTemplate.orderReason = regimen["orderset"]["orders"][x]["orderReason"]
    jsonOrderTemplate.drug = ObjDict()
    jsonOrderTemplate.drug.name = regimen["orderset"]["orders"][x]["drug"]["name"]
    jsonOrderTemplate.drug.uuid = uuidOrderTypeConcept
    jsonOrderTemplate.drug.form = regimen["orderset"]["orders"][x]["drug"]["form"]
    jsonOrderTemplate.drug.additionalInstructions = regimen["orderset"]["orders"][x]["drug"]["additionalInstructions"]
    jsonOrderTemplate.orderTemplateType = None

    # DEBUG
    #print "[jsonOrderTemplate]:\n"+jsonOrderTemplate.dumps()

    # build orderSetMember JSON payload data set...
    orderSetMember = ObjDict()
    orderSetMember.orderType = ObjDict()
    orderSetMember.orderType.uuid = uuidOrderType # usually UUID of "Drug Order" type
    orderSetMember.orderTemplate = jsonOrderTemplate.dumps()
    orderSetMember.concept = ObjDict()
    orderSetMember.concept.display = nameOrderTypeConcept
    orderSetMember.concept.uuid = uuidOrderTypeConcept

    # if this is the fist item in list of medications, create base orderSet object
    if x == 0:
        # build orderSet JSON payload data set...
        order = ObjDict()
        order.name = regimen["orderset"]["name"]
        order.description = regimen["orderset"]["description"]
        order.operator = "ANY"
        # TODO: add "indication", "cycle" info when data model ready
        order.orderSetMembers = []

    # append new orderSetMember into array
    order.orderSetMembers.append(orderSetMember)

# TODO: add orderSet attribute values
#   order.attributes = ObjDict()
#   order.attributes.attributeType = "a5fb5770-409a-11e2-a25f-0800200c9a66"
#   order.attributes.value = "test value"


#print "[DEBUG] CREATE ORDERSET PAYLOAD:"
#print order.dumps()

# reset extra url parameter (only used in "-update" use case)
uuidOrderSetParam = ""

# if tool action is to add or update a regimen orderSet...
if ACTION == "-update":
    # if params include <uuid> param...
    if len(sys.argv) > 4:
        uuidOrderSetParam = "/" + sys.argv[4] # use <uuid> in url
    else:
        # bad params list, exit
        displayArgsHelp()
        exit()

# create or update an orderSet (Regimen) template
r = requests.post(url = API_ENDPOINT + "/orderset" + uuidOrderSetParam,
                  auth = (USERID,PASSWORD),
                  headers = HEADERS,
                  data = order.dumps(),
                  verify = False)

# display results
print r;
