# #This line specifies the base image for the container. In this case, it's using an Alpine Linux image with Python 3.9.
# #Not so important but it helps in documentation and knowing who maintains this docker image
# #it tells that no need to buffer the output and get logs in realtime
# #copy from the local to the docker image
# #only one run to avoid creating the image layers to keep our file light weight
# #create virtual environment to bypass any conflict due to dependencies on the actual base image
# # "&& \" is used to concatenate multiple command in single line and if any line fail it fails.
# # we remove tmp directory, to remove the extra folder
# # add user to restrict the full access and do not work on root user because if file get compromised then user can get full access
# #sets the environment variable inside the image and it defines all the data where the executables can be run.
# # once all the above commands are being run as a root user, now after this every command will be run as a django user with limited access.
# FROM python:3.10-alpine3.14
# LABEL maintainer="londonappdeveloper.com"

# ENV PYTHONUNBUFFERED 1

# COPY ./requirements.txt /tmp/requirements.txt
# COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# COPY ./app /app
# WORKDIR /app
# EXPOSE 8000

# ARG DEV=false

# # Create virtual environment in /py
# RUN python -m venv /py

# # # Upgrade pip and install requirements
# # RUN /py/bin/pip install --upgrade pip && \
# #     /py/bin/pip install -r /tmp/requirements.txt && \
# #     if [ "$DEV" = "true" ]; then /py/bin/pip install -r requirements.dev.txt; fi

# # Upgrade pip and install requirements
# RUN /py/bin/pip install --upgrade pip && \
#     # installing the postgresql client.
#     # we are going to need this package inside our alpine image in order for our psycopgy2 package to connect with postgresql
#     apk add --update --no--cache postgresql--client && \
#     apk add --update --no--cache --virtual .tmp-build-deps \
#         build-base postgresql-dev musl-dev && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     if [ "$DEV" = "True" ]; then \
#         /py/bin/pip install -r /tmp/requirements.dev.txt && \
#         /py/bin/pip install flake8; \
#     fi

# # Clean up temporary files
# RUN rm -rf /tmp && \
#     apk del .tmp-build-deps &&

# # Create non-root user
# RUN adduser \
#     --disabled-password \
#     --no-create-home \
#     django-user

# # Set PATH for the virtual environment
# ENV PATH="/py/bin:$PATH"

# # Switch to the non-root user
# USER django-user

FROM python:3.10-alpine3.14
LABEL maintainer="londonappdeveloper.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

# Create virtual environment in /py
RUN python -m venv /py

# Upgrade pip and install requirements
RUN /py/bin/pip install --upgrade pip && \
    # installing the postgresql client.
    # we are going to need this package inside our alpine image in order for our psycopgy2 package to connect with postgresql
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "True" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt && \
        /py/bin/pip install flake8; \
    fi

# Clean up temporary files
RUN rm -rf /tmp && \
    apk del .tmp-build-deps

# Create non-root user
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

# Set PATH for the virtual environment
ENV PATH="/py/bin:$PATH"

# Switch to the non-root user
USER django-user
