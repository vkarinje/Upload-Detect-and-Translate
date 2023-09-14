#use Google Cloud SDK's container as the base image
FROM google/cloud-sdk

# Specify your e-mail address as the maintainer of the container image
MAINTAINER "vkarinje@pdx.edu"

# Copy the contents  container directory /app
COPY . /app

# Set the working directory of the container to /app
WORKDIR /app

# Install the Python packages specified by requirements.txt into the container
RUN apt update -y && apt install -y python3-pip && pip3 install --upgrade google-cloud-datastore && pip3 install -r requirements.txt && export GOOGLE_APPLICATION_CREDENTIALS=$HOME/cloud-cs-530-vkarinje-lab5-bce141cc38e1.json
# Set the parameters to the program
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
