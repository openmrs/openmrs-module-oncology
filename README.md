# openmrs-module-oncology
Oncology module for OpenMRS

Collaborative work with IBM, Partners In Health, Hôpital Universitaire de Mirebalais (Haiti), Uganda Cancer Institute, University of North Carolina, and the OpenMRS Community.

July 15 - August 3, 2018, Boston MA

Deliverables:
-------------

- Design assets:
  - [Mockups](https://github.com/dearmasm/openmrs-module-oncology/blob/master/docs/Mockups.md)
  - Use Cases
  
  - [Back-end proposal](https://github.com/dearmasm/openmrs-module-oncology/blob/master/docs/BACKEND_PROPOSAL.md)
  - [Chemotherapy Ordering data design proposal and discussion](https://talk.openmrs.org/t/chemotherapy-ordering-data-design/19133)

- Oncology Solution OpenMRS components w/ contributions for chemotherapy treatment:
  - [OpenMRS Core](https://github.com/idlewis/openmrs-core)
    Iain's fork of core. The branch used on the oncology test server is 'integration'. Other branches contain the same commits but split by functional areas
  - [OpenMRS Web Services REST module](https://github.com/idlewis/openmrs-module-webservices.rest)
    Iain's fork of the webservices module. Same as above for branches
  - [OpenMRS PIH Mirebalais Metadata module](https://github.com/PIH/openmrs-module-mirebalaismetadata)
  - [OpenMRS Oncology Regimens Templates](https://github.com/dearmasm/openmrs-module-oncology/edit/master/regimens) 
  - dependencies:
    - [OpenMRS PIH Mirebalais module](https://github.com/PIH/openmrs-module-mirebalais)
    - [OpenMRS PIH Core module](https://github.com/PIH/openmrs-module-pihcore)

- Project Utilities
  - [YAAR - Regimen template tool](https://github.com/dearmasm/openmrs-module-oncology/blob/master/utils/YAAR_DOCS.md)
  - [GITPOLLER - GitHub commit watcher](https://github.com/dearmasm/openmrs-module-oncology/blob/master/utils/GITPOLLER_DOCS.md)

Notes:
------

