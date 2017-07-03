#!/usr/bin/env bash

docker exec -i devstack /bin/bash -s <<EOF
echo 'Fixing Mongo'
sudo -S rm /edx/var/mongo/mongodb/mongod.lock
sudo -S mongod -repair --config /etc/mongod.conf
sudo -S chown -R mongodb:mongodb /edx/var/mongo/.
sudo -S service mongod start
sudo su edxapp -s /bin/bash
source /edx/app/edxapp/edxapp_env
cd /edx/app/edxapp/edx-platform
echo 'Running Tests'
echo $TEST_SUITE 
echo $SHARD 
cat ./scripts/travis-tests.sh
EOF

docker exec -it devstack env TERM=$(TERM) /edx/app/edxapp/edx-platform/scripts/generic-ci-tests.sh
