import sys
import json
import yaml
import requests
import urllib
import collections

from objdict import ObjDict

# TODO: remove this warning disabling statement!
requests.packages.urllib3.disable_warnings()

# start tool implementation
print "OPENMRS ORDERSET TOOL..."

# read orderSet (Regimen) template file (YAML schema)
INPUT_FILE = sys.argv[1]
print "[INFO] INPUT_FILE: " + INPUT_FILE
file = open(INPUT_FILE, "r")
regimen = yaml.load(file)

# define api host & endpoint info
#HOST = "https://ci.pih-emr.org"
HOST = "https://humci-azure.pih-emr.org"  # eventually make "sys.argv[2]"
API_ENDPOINT = HOST+"/mirebalais/ws/rest/v1"
USERID = "IBMHC1"
PASSWORD = "Ibmhc123"
HEADERS = {'Content-Type': 'application/json'}
print "[INFO] API_ENDPOINT: " + API_ENDPOINT


# build orderSetMember list in a loop...
for x in range(len(regimen["orderset"]["orders"])):

    print "[INFO] orderSetMember[",x,"]"

    # FETCH REQUIRED UUIDs...

    print regimen["orderset"]["orders"][x]

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

    print "[DEBUG] concept result\n" + r.text

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

    print "[jsonOrderTemplate]:\n"+jsonOrderTemplate.dumps()

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

 #   order.attributes = ObjDict()
 #   order.attributes.attributeType = "a5fb5770-409a-11e2-a25f-0800200c9a66"
 #   order.attributes.value = "test value"


print "[DEBUG] CREATE ORDERSET PAYLOAD:"
print order.dumps()

# create new orderSet (Regimen) template
r = requests.post(url = API_ENDPOINT + "/orderset",
                  auth = (USERID,PASSWORD),
                  headers = HEADERS,
                  data = order.dumps(),
                  verify = False)

print r;

exit()

body = {}
body["name"] = "Mario's Automated Regimen"
body["description"] = "OrderSet regimen provisioned using nifty automation python script + metadata"
body["operator"] = "ANY"

#body["orderSetMembers"] = {"orderType: { uuid: drugorder }"}

#body["orderSetMembers"]["orderType"]["uuid"] = "drugorder"
#body["orderSetMembers"]["orderTemplate"] = "{\"administrationInstructions\":\"In the evening\",\"dosingInstructions\":{\"doseUnits\":\"Tablet(s)\",\"frequency\":\"Once a day\",\"route\":\"Oral\",\"dose\":1},\"durationUnits\":\"Day(s)\",\"duration\":1,\"drug\":{\"name\":\"Aspirin 75mg\",\"uuid\":\"49f0c5c2-4738-4382-9928-69fd330d4624\",\"form\":\"Tablet\"},\"additionalInstructions\":\"This is good\"}"
#body["orderSetMembers"]["concept"]["display"] = "Aspirin"
#body["orderSetMembers"]["concept"]["uuid"] = "09291895-fb7d-4989-9e31-723ab44856d2"

#body["orderSetMembers"]["orderType"]["uuid"] = "drugorder"
#body["orderSetMembers"]["orderTemplate"] = "{\"drug\":{\"name\":\"Paracetamol 150mg\",\"uuid\":\"671ddb89-a30c-46e8-9f0c-5663714267d4\",\"form\":\"Injection\"},\"dosingInstructions\":{\"dose\":1,\"doseUnits\":\"Tablet(s)\",\"frequency\":\"Once a day\",\"route\":\"Oral\"},\"administrationInstructions\":\"In the evening\",\"duration\":1,\"durationUnits\":\"Day(s)\",\"additionalInstructions\":\"This is better\"}"
#body["orderSetMembers"]["concept"]["display"] = "Paracetamol"
#body["orderSetMembers"]["concept"]["uuid"] = "9881091b-1802-4c62-8b80-a8fcb170b59f"


print json.dumps(body);


#req.add_header('Content-Type', 'application/json; charset=utf-8')

#headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, auth = ('IBMHC1', 'Ibmhc123'), headers = headers, data = order.dumps(), verify = False)
#r = requests.post(url = API_ENDPOINT, auth = ('IBMHC1', 'Ibmhc123'), headers = headers, data = json.dumps(body), verify = False)
#r = requests.get(url = API_ENDPOINT, auth = ('IBMHC1', 'Ibmhc123'), headers = headers, verify = False)

print r

# extracting response text
#print r.json()

exit()

# fetch UUID for order "indication" or any other CIEL or PIH code concept value
#curl -X GET "https://humci-azure.pih-emr.org/mirebalais/ws/rest/v1/conceptreferenceterm?v=full&codeOrName=163073&source=CIEL" -H  "accept: application/json"

# fetch UUID for order type
#curl -X GET "https://humci-azure.pih-emr.org/mirebalais/ws/rest/v1/ordertype?v=full&q=drug%20order" -H  "accept: application/json"



o1 = osm.format( regimen["orderset"]["orders"][x]["type"],
                            regimen["orderset"]["orders"][x]["administrationInstructions"],
                            regimen["orderset"]["orders"][0]["dosingInstructions"]["doseUnits"],
                            regimen["orderset"]["orders"][0]["dosingInstructions"]["frequency"],
                            regimen["orderset"]["orders"][0]["dosingInstructions"]["route"],
                            regimen["orderset"]["orders"][0]["dosingInstructions"]["dose"],
                            regimen["orderset"]["orders"][0]["durationUnits"],
                            regimen["orderset"]["orders"][0]["duration"],
                            regimen["orderset"]["orders"][0]["relativeStartDay"],
                            regimen["orderset"]["orders"][0]["orderReason"],
                            regimen["orderset"]["orders"][0]["drug"]["name"],
                            regimen["orderset"]["orders"][0]["drug"]["form"],
                            regimen["orderset"]["orders"][0]["drug"]["additionalInstructions"],
                            regimen["orderset"]["orders"][0]["concept"],
                            "09291895-fb7d-4989-9e31-723ab44856d2"
                            )

#print o1

exit()


orderSetMember4 = {
    "orderType": {
        "uuid": "foo"
    },
    "orderTemplate": "{\"administrationInstructions\":\"foo\",\"dosingInstructions\":{\"doseUnits\":\"foo\",\"frequency\":\"foo\",\"route\":\"foo\",\"dose\":foo},\"durationUnits\":\"foo\",\"duration\":foo,\"drug\":{\"name\":\"foo\",\"uuid\":\"foo\",\"form\":\"foo\"},\"additionalInstructions\":\"foo\"}",
    "concept": {
        "display": "foo",
        "uuid": "foo"
    }
}


orderSetMember1 = {
    "orderType": {
        "uuid": "{}"
    },
    "orderTemplate": "{\"administrationInstructions\":\"{}\",\"dosingInstructions\":{\"doseUnits\":\"{}\",\"frequency\":\"{}\",\"route\":\"{}\",\"dose\":{}},\"durationUnits\":\"{}\",\"duration\":{},\"drug\":{\"name\":\"{}\",\"uuid\":\"{}\",\"form\":\"{}\"},\"additionalInstructions\":\"{}\"}",
    "concept": {
        "display": "{}",
        "uuid": "{}"
    }
}


orderSet = { "name": "foo",
             "description": "foo",
             "operator": "foo" }

orderType = { "orderType": {
        "uuid": "foo"
    } }

orderTemplateJSONString = {"administrationInstructions":"foo","dosingInstructions":{"doseUnits":"foo","frequency":"foo","route":"foo","dose":"foo"},"durationUnits":"foo","duration":"foo","drug":{"name":"foo","uuid":"foo","form":"foo"}, "additionalInstructions":"foo"}

orderTemplate = { "orderTemplate": json.dumps(orderTemplateJSONString) }

orderConcept = { "concept": {
        "display": "foo",
        "uuid": "foo"
    } }

orderSetMember = json.dumps(orderType) + "," + json.dumps(orderTemplate) + "," + json.dumps(orderConcept)

order = str(orderSet) + "," + "\"orderSetMembers\": [" + orderSetMember + "]"

print "dict:"
print str(orderSetMember)

orderType["orderType"]["uuid"] = "bar"

#orderSetMember = json.dumps(orderType) + "," + json.dumps(json.dumps(orderTemplate)) + "," + json.dumps(orderConcept)

#print "json.dumps:"
#print json.dumps(orderSetMember)

#print "dict:"
#print str(orderSetMember)

#print "dict:"
#print str(order)



#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)


#print regimen
#print regimen["orderset"]
#print regimen["orderset"]["name"]
#print regimen["orderset"]["cycleLength"]
#print regimen["orderset"]["orders"][0]["type"]
#print urllib.quote(regimen["orderset"]["orders"][0]["type"])


# define JSON body parts required for OrderSet creation:
# { OrderSet.name, OrderSet.description, OrderSet.operator,
#   OrderSetMember[*]
# }


#print json.dumps(regimen["orderset"]["orders"][0]["type"])

# lookup orderType UUID
#curl -X GET "https://humci-azure.pih-emr.org/mirebalais/ws/rest/v1/ordertype?v=full&q=drug%20order" -H  "accept: application/json"

print "RESPONSE:"
r2 = r.text  #json.loads(r.text).get("results")
r2json = json.loads(r2)

print json.loads(r.text)["results"][0]["uuid"]

exit()
