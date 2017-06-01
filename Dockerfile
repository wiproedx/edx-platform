FROM edxops/edxapp:latest
WORKDIR /edx/app/edxapp/edx-platform
ADD scripts/travis-install.sh /edx/app/edxapp/edx-platform/scripts
ADD scripts/travis-tests.sh /edx/app/edxapp/edx-platform/scripts
RUN git status
RUN source /edx/app/edxapp/edxapp_env 
RUN /edx/app/edxapp/edx-platform/scripts/travis-install.sh
RUN paver test_system -s lms -v