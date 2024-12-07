# Remove the directory if it exists
rm -r -f build/app/android
# Execute the Briefcase commands
briefcase create android
briefcase build android
briefcase package android
briefcase run android -d @cloud_phone