# Yet Another Automated Regimen (YAAR) management tool
# OpenMRS OrderSet (Regimen) lifecycle automated tooling
#   - query, create, update, retire OrderSets (Regimens)
# author: Mario De Armas
# date: 2018.08.03
# version: 1.0

import sys
import json
import yaml
import requests
import urllib
import collections

from objdict import ObjDict

# TODO: remove this warning disabling statement!
requests.packages.urllib3.disable_warnings()


def buildDict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

def displayArgsHelp():
    print "[INFO] usage: yaar -add <config-file> <input-file>"
    print "              yaar -get <config-file> [<uuid>]"
    print "              yaar -update <config-file> <input-file> <uuid>"
    print "              yaar -retire <config-file> <uuid>"
    #print "              yaar -purge <config-file> <uuid>"  # <<< action currently not supported by OpenMRS

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


# lookup regimen category UUID
categoryCodedValue = regimen["orderset"]["category"].split(":")
# fetch category concept UUID value
r = requests.get(url = API_ENDPOINT + "/conceptreferenceterm?v=full&codeOrName=" + categoryCodedValue[1] + "&source=" + categoryCodedValue[0] + "?lang=en",
                 auth = (USERID,PASSWORD),
                 headers = HEADERS,
                 verify = False)

# store fetched UUID
uuidRegimenCategory = json.loads(r.text)["results"][0]["uuid"]

#print json.dumps(regimen)
#exit()

# build new orderSet's orderSetMember list in a loop...
for x in range(len(regimen["orderset"]["orders"])):

    print "[INFO] processing orderSetMember[",x,"]"

    # build orderSetMember number [x]...

    # DEBUG
    #print regimen["orderset"]["orders"][x]

    # prepare to query UUIDs that will be required during OrderSet creation phase
    # fetch UUIDs using metadata coded into OrderSet Regimen definition YAML source

    #--------------------------------------------------------------------------
    # use orderType encoded value
    order_type = urllib.quote(regimen["orderset"]["orders"][x]["type"])

    # fetch orderType UUID value
    r = requests.get(url = API_ENDPOINT + "/ordertype?v=full&q=" + order_type,
                     auth = (USERID,PASSWORD),
                     headers = HEADERS,
                     verify = False)

    # store fetched UUID
    uuidOrderType = json.loads(r.text)["results"][0]["uuid"]

    #--------------------------------------------------------------------------
    # use orderType concept encoded value
    conceptCodeValue = regimen["orderset"]["orders"][x]["drugConcept"]

    # fetch orderType Concept UUID value
    r = requests.get(url = API_ENDPOINT + "/concept?locale='en'&q=" + conceptCodeValue,
                     auth = (USERID,PASSWORD),
                     headers = HEADERS,
                     verify = False)

    # TODO: change to capture retrieved concept display name
    nameOrderTypeConcept = conceptCodeValue #json.loads(r.text)["results"][0]["display"]
    uuidOrderTypeConcept = json.loads(r.text)["results"][0]["uuid"]

    print "[INFO] uuidOrderType: " + uuidOrderType + "   [" + order_type + "]"
    print "[INFO] uuidOrderTypeConcept: " + uuidOrderTypeConcept + "   [" + nameOrderTypeConcept + "]"

    #--------------------------------------------------------------------------
    # fetch OrderSetAttributeType UUID values
    r = requests.get(url = API_ENDPOINT + "/ordersetattributetype",
                     auth = (USERID,PASSWORD),
                     headers = HEADERS,
                     verify = False)

    orderSetAttributeTypes = json.loads(r.text)["results"]

    attribsByName = buildDict(orderSetAttributeTypes, key="display")
    attribsByName.get("cycleLength")["uuid"]
    #print "[DEBUG] uuidOrderSetAttributes: " + json.dumps(attribsByName)

    #--------------------------------------------------------------------------
    # fetch Time Units UUID value for cycleLengthUnits
    #r = requests.get(url = API_ENDPOINT + "/concept/f1904502-319d-4681-9030-e642111e7ce2?v=full",
    #                 auth = (USERID,PASSWORD),
    #                 headers = HEADERS,
    #                 verify = False)

    #print r.text

    #orderSetAttributeTypes = json.loads(r.text)["results"]

    #attribsByName = buildDict(orderSetAttributeTypes, key="display")
    #attribsByName.get("cycleLength")["uuid"]
    #print "[DEBUG] uuidOrderSetAttributes: " + json.dumps(attribsByName)

    # can't seem to find API that can cleanly fetch info needed, so hard-coding for now
    if (regimen["orderset"]["cycleLengthUnits"] == "Months"):
        uuidCycleLengthUnits = "3cd70b68-26fe-102b-80cb-0017a47871b2"
    if (regimen["orderset"]["cycleLengthUnits"] == "Weeks"):
        uuidCycleLengthUnits = "3cd7091a-26fe-102b-80cb-0017a47871b2"
    if (regimen["orderset"]["cycleLengthUnits"] == "Days"):
        uuidCycleLengthUnits = "3cd706b8-26fe-102b-80cb-0017a47871b2"


    #--------------------------------------------------------------------------
    jsonOrderTemplate = ObjDict();
    jsonOrderTemplate.category = regimen["orderset"]["orders"][x]["category"]
    jsonOrderTemplate.drugConcept = regimen["orderset"]["orders"][x]["drugConcept"]
    jsonOrderTemplate.drugName = regimen["orderset"]["orders"][x]["drugName"]
    jsonOrderTemplate.route = regimen["orderset"]["orders"][x]["route"]
    jsonOrderTemplate.dose = regimen["orderset"]["orders"][x].get("dose")
    jsonOrderTemplate.doseUnits = regimen["orderset"]["orders"][x].get("doseUnits")
    jsonOrderTemplate.relativeStartDay = regimen["orderset"]["orders"][x]["relativeStartDay"]
    jsonOrderTemplate.dosingInstructions = ObjDict()
    jsonOrderTemplate.dosingInstructions.dosingTiming = regimen["orderset"]["orders"][x]["dosingInstructions"]["timing"]
    jsonOrderTemplate.dosingInstructions.dosingDilution = regimen["orderset"]["orders"][x]["dosingInstructions"].get("dilution")
    jsonOrderTemplate.dosingInstructions.dosingAdjustment = regimen["orderset"]["orders"][x]["dosingInstructions"]["dosingAdjustment"]
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
        order.description = regimen["orderset"]["name"]
        order.operator = "ANY"
        order.category = uuidRegimenCategory
        order.orderSetMembers = []  # create empty orderSetMemberList array
        order.attributes = []       # create empty orderSet attributes array
        orderSetAttribute = ObjDict()     # cycleLength
        orderSetAttribute.attributeType = attribsByName.get("cycleLength")["uuid"]
        orderSetAttribute.value = str(regimen["orderset"]["cycleLength"])
        order.attributes.append(orderSetAttribute)
        orderSetAttribute = ObjDict()     # cycleLengthUnits
        orderSetAttribute.attributeType = attribsByName.get("cycleLengthUnits")["uuid"]
        orderSetAttribute.value = uuidCycleLengthUnits
        order.attributes.append(orderSetAttribute)
        orderSetAttribute = ObjDict()     # cycleCount
        orderSetAttribute.attributeType = attribsByName.get("numCycles")["uuid"]
        orderSetAttribute.value = str(regimen["orderset"]["cycleCount"])
        order.attributes.append(orderSetAttribute)

    # append new orderSetMember into array
    order.orderSetMembers.append(orderSetMember)

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

print order.dumps()

# create or update an orderSet (Regimen) template
r = requests.post(url = API_ENDPOINT + "/orderset" + uuidOrderSetParam,
                  auth = (USERID,PASSWORD),
                  headers = HEADERS,
                  data = order.dumps(),
                  verify = False)

# display results
print r;
