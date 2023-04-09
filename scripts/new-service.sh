#!/usr/bin/env bash

# Change folder to the root of the project
cd "$(dirname "$0")/.."

# Get the service name from the first argument
SERVICE_NAME=$1

# If service name is empty, exit
if [ -z "$SERVICE_NAME" ]; then
  echo "Service name is required"
  exit 1
fi

# Validate the service name, must be alphanumeric, non empty, and no spaces. Dashes is allowed.
if [[ ! $SERVICE_NAME =~ ^[a-zA-Z0-9-]+$ ]]; then
  echo "Invalid service name: $SERVICE_NAME"
  echo "Service name must be alphanumeric, non empty, and no spaces. Dashes is allowed."
  exit 1
fi

# If service already exists, exit
if [ -d "services/$SERVICE_NAME" ]; then
  echo "Service already exists: $SERVICE_NAME"
  exit 1
fi

# Create a copy of the service name, while replacing dashes with underscores
SERVICE_NAME_UNDERSCORES=$(echo $SERVICE_NAME | sed 's/-/_/g')

# Set the service folder
SERVICE_FOLDER=services/$SERVICE_NAME_UNDERSCORES

# Copy the service template to the services directory
cp -r templates/service $SERVICE_FOLDER

# Rename the service template files to the service name
mv $SERVICE_FOLDER/src/service_name $SERVICE_FOLDER/src/$SERVICE_NAME_UNDERSCORES

export LC_ALL=C
# Replace all instances of "<SERVICE_NAME>" with the service name, in all files in the service directory
find $SERVICE_FOLDER -type f -exec sed -i '' "s/<SERVICE_NAME>/$SERVICE_NAME_UNDERSCORES/g" {} \;

# Replace all instances of "<SERVICE-NAME>" with the service name, in all files in the service directory
find $SERVICE_FOLDER -type f -exec sed -i '' "s/<SERVICE-NAME>/$SERVICE_NAME/g" {} \;

# Greet the user
echo "Service created in $SERVICE_FOLDER"
