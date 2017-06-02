FROM edxops/edxapp:latest
WORKDIR /edx/app/edxapp/edx-platform
ADD scripts/travis-install.sh /edx/app/edxapp/edx-platform/scripts
ADD scripts/travis-tests.sh /edx/app/edxapp/edx-platform/scripts
RUN git status
RUN . /edx/app/edxapp/edxapp_env 
RUN /edx/app/edxapp/edx-platform/scripts/travis-install.sh
RUN mongo --version
RUN /bin/bash -c "source /edx/app/edxapp/edxapp_env && export EDXAPP_TEST_MONGO_HOST='mongo' && paver test_system -s lms -v --fail-fast"
