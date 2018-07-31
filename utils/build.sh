#!/usr/bin/env bash
echo ""
echo "==========================================================="
echo "BUILD CORE..."
echo "==========================================================="
cd ~/build/openmrs-core
git pull
mvn clean install -DskipTests
#read -p "Check results above and press any key to continue... " -n1 -s

echo ""
echo "==========================================================="
echo "BUILD REST API MODULE..."
echo "==========================================================="
cd ~/build/openmrs-module-webservices.rest
git pull
mvn clean install -DskipTests
#read -p "Check results above and press any key to continue... " -n1 -s
echo ""
