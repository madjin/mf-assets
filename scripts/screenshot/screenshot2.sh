#!/bin/bash

# Absolute path to the directory containing this script
SCRIPT_DIR="$(pwd)"

# Absolute path to the screenshot.js script
SCREENSHOT_SCRIPT="$SCRIPT_DIR/scripts/screenshot/screenshot.js"

# Iterate through all folders in sorted order
# Select folder via command line argument
for dir in $(ls -d "$1"/* | sort -V); do
  folder=${dir%*/}  # Remove trailing slash
  echo "Processing $folder"

  # Check if the folder is not node_modules and contains an index.html file
  if [ "$folder" != "node_modules" ] && [ -f "$folder/index.html" ]; then
    # Run the Puppeteer script for each folder
    node "$SCREENSHOT_SCRIPT" "$folder/index.html"

    # Get the base name of the directory
    base_name=$(basename "$folder")

    # Save the screenshot in the current directory with a specific name based on the folder
    mv "$SCRIPT_DIR/screenshot.png" "$base_name.png"
  fi
done
