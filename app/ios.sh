# Remove the directory if it exists
rm -r -f build/helloworld/iOS
# Execute the Briefcase commands
briefcase create iOS
briefcase build iOS
briefcase package iOS
briefcase run iOS -d "add your device id here"