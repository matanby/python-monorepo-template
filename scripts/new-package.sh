#!/usr/bin/env bash

# Change folder to the root of the project
cd "$(dirname "$0")/.."

# Get the package name from the first argument
PACKAGE_NAME=$1

# If package name is empty, exit
if [ -z "$PACKAGE_NAME" ]; then
  echo "Package name is required"
  exit 1
fi

# Validate the package name, must be alphanumeric, non empty, and no spaces. Dashes is allowed.
if [[ ! $PACKAGE_NAME =~ ^[a-zA-Z0-9-]+$ ]]; then
  echo "Invalid package name: $PACKAGE_NAME"
  echo "Package name must be alphanumeric, non empty, and no spaces. Dashes is allowed."
  exit 1
fi

# If package already exists, exit
if [ -d "packages/$PACKAGE_NAME" ]; then
  echo "Package already exists: $PACKAGE_NAME"
  exit 1
fi

# Create a copy of the package name, while replacing dashes with underscores
PACKAGE_NAME_UNDERSCORES=$(echo $PACKAGE_NAME | sed 's/-/_/g')

# Set the package folder
PACKAGE_FOLDER=packages/$PACKAGE_NAME_UNDERSCORES

# Copy the package template to the packages directory
cp -r templates/package $PACKAGE_FOLDER

# Rename the package template files to the package name
mv $PACKAGE_FOLDER/src/package_name $PACKAGE_FOLDER/src/$PACKAGE_NAME_UNDERSCORES

export LC_ALL=C
# Replace all instances of "<PACKAGE_NAME>" with the package name, in all files in the package directory
find $PACKAGE_FOLDER -type f -exec sed -i '' "s/<PACKAGE_NAME>/$PACKAGE_NAME_UNDERSCORES/g" {} \;

# Replace all instances of "<PACKAGE-NAME>" with the package name, in all files in the package directory
find $PACKAGE_FOLDER -type f -exec sed -i '' "s/<PACKAGE-NAME>/$PACKAGE_NAME/g" {} \;

# Greet the user
echo "Package created in $PACKAGE_FOLDER"
