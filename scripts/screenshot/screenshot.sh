#!/bin/bash

# Iterate through all folders in sorted order
# Select folder via command line argument
for dir in $(ls -d "$1"/* | sort -V); do
  dir=${dir%*/}  # Remove trailing slash

  # Check if the folder is not node_modules and contains an index.html file
  if [ "$dir" != "node_modules" ] && [ -f "$dir/index.html" ]; then
    # Run the Puppeteer script for each folder
    node screenshot.js "$dir/index.html"
    
    # Save the screenshot in the current directory with a specific name based on the folder
    mv screenshot.png "$dir.png"
  fi
done
