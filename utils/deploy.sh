#!/usr/bin/env bash

set +v
echo "==========================================================="
echo "STOP TOMCAT SERVER..."
echo "==========================================================="
set -v
service tomcat7 stop
sleep 3
service tomcat7 status
set +v
read -p "Check results above and press any key to continue... " -n1 -s
echo ""

echo "==========================================================="
echo "DEPLOY CORE..."
echo "==========================================================="
set -v
cd /var/lib/tomcat7/webapps
rm -rf mirebalais
rm -rf mirebalais.war
cp ~/build/openmrs-core/webapp/target/openmrs.war mirebalais.war
chown tomcat7 mirebalais.war 
chgrp tomcat7 mirebalais.war 
set +v
read -p "Check results above and press any key to continue... " -n1 -s
echo ""

echo "==========================================================="
echo "DEPLOY REST API MODULE..."
echo "==========================================================="
set -v
cd /home/tomcat7/.OpenMRS/modules
rm -rf webservices.rest-2.23.0-SNAPSHOT.*
cp ~/build/openmrs-module-webservices.rest/omod/target/webservices.rest-2.23.0-SNAPSHOT.*.omod .
chown tomcat7 webservices.rest-2.23.0-SNAPSHOT.*.omod 
chgrp tomcat7 webservices.rest-2.23.0-SNAPSHOT.*.omod
set +v
#read -p "Check results above and press any key to continue... " -n1 -s
echo ""

echo "Done."
