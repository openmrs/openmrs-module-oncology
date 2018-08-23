<img src="https://cloud.githubusercontent.com/assets/668093/12567089/0ac42774-c372-11e5-97eb-00baf0fccc37.jpg" alt="OpenMRS"/>

# openmrs-module-oncology
Oncology module for OpenMRS

Collaborative work with IBM, Partners In Health, Hôpital Universitaire de Mirebalais (Haiti), Uganda Cancer Institute, University of North Carolina, and the OpenMRS Community.

Project dates: July 15 - August 3, 2018, Boston MA

Purpose:
--------
The goal of this project is to add **chemotherapy regimen support** to OpenMRS EMR system so that doctors can order and track a patient's chemo treatment from EMR system. Nurse's adminstration detail is also included in this new support in order to **improve quality of care for cancer patients** and tracking the chemo treatment effectiveness.

Implementation Demonstration:
-----------------------------
[![Little red ridning hood](http://i.imgur.com/7YTMFQp.png)](https://vimeo.com/3514904 "Little red riding hood - Click to Watch!")

Deliverables:
-------------

- Design assets:
  - [Mockups](https://github.com/openmrs/openmrs-module-oncology/blob/master/docs/Mockups.md)
  - Use Cases
  - [Back-end proposal](https://github.com/openmrs/openmrs-module-oncology/blob/master/docs/BACKEND_PROPOSAL.md)
  - [Chemotherapy Ordering data design proposal and discussion](https://talk.openmrs.org/t/chemotherapy-ordering-data-design/19133)
  - [Haiti's Mirebalais Hospital chemotherapy paper forms](https://github.com/openmrs/openmrs-module-oncology/tree/master/haiti-chemo-forms)

- Oncology Solution OpenMRS components w/ contributions for chemotherapy treatment:
  - [OpenMRS Oncology OWA module](https://github.com/openmrs/openmrs-owa-oncology) : **Front-end (UI)** implementation for Chemotherapy Ordering user experience (implements Doctor & Nurse use cases).
  - [OpenMRS Core](https://github.com/idlewis/openmrs-core) : **Back-end (Core)** implementation. Iain's fork of core. The branch used on the oncology test server is 'integration'. Other branches contain the same commits but split by functional areas.
  - [OpenMRS Web Services REST module](https://github.com/idlewis/openmrs-module-webservices.rest) : **API (REST)** implementation. Iain's fork of the webservices module. Same as above for branches.
  - [OpenMRS PIH Mirebalais Metadata module](https://github.com/PIH/openmrs-module-mirebalaismetadata) : Updated **metadata concepts** for supporting chemotherapy regimens for Haiti use cases.
  - [OpenMRS Oncology Regimens Templates](https://github.com/openmrs/openmrs-module-oncology/tree/master/regimens) : Haiti **chemotherapy regimens** codified into YAML schema for ease of provisioning/updating using [YAAR tool](https://github.com/dearmasm/openmrs-module-oncology/blob/master/utils/YAAR_DOCS.md).
  - dependencies:
    - [OpenMRS PIH Mirebalais module](https://github.com/PIH/openmrs-module-mirebalais)
    - [OpenMRS PIH Core module](https://github.com/PIH/openmrs-module-pihcore)

- Project Utilities
  - [YAAR - Regimen template tool](https://github.com/openmrs/openmrs-module-oncology/blob/master/utils/YAAR_DOCS.md)
  - [GITPOLLER - GitHub commit watcher](https://github.com/openmrs/openmrs-module-oncology/blob/master/utils/GITPOLLER_DOCS.md)


Backlog/Dashboard:
------------------

- [Chemo Order Issues](https://issues.openmrs.org/browse/TRUNK-5414?jql=labels%20%3D%20chemo-order)
- [Chemotherapy Orders Dashboard](https://issues.openmrs.org/secure/RapidBoard.jspa?rapidView=171&view=planning&selectedIssue=TRUNK-5413&projectKey=TRUNK)
  
  
Notes:
------

