# Remove the directory if it exists
rm -r -f build/helloworld/android
# Execute the Briefcase commands
briefcase create android
briefcase build android
briefcase package android
briefcase run android -d "add your device id here"