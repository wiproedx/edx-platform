FROM edxops/edxapp:latest
# RUN mkdir /edx 
# RUN mkdir /edx/app 
# RUN mkdir /edx/app/edxapp
# RUN mkdir /edx/app/edxapp/edx-platform
WORKDIR /edx/app/edxapp/edx-platform
ADD scripts/travis-install.sh /edx/app/edxapp/edx-platform/scripts
ADD scripts/travis-tests.sh /edx/app/edxapp/edx-platform/scripts
RUN git status
RUN /edx/app/edxapp/edx-platform/scripts/travis-install.sh
RUN paver test_system -s lms -v