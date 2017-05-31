FROM edxops/edxapp:latest
# RUN mkdir /edx 
# RUN mkdir /edx/app 
# RUN mkdir /edx/app/edxapp
# RUN mkdir /edx/app/edxapp/edx-platform
WORKDIR /edx/app/edxapp/edx-platform
# ADD . /edx/app/edxapp/edx-platform
RUN git status
RUN bash ./scripts/travis-install.sh
RUN paver test_system -s lms -v