# Remove the directory if it exists
rm -r -f build/helloworld/macOS
rm -r -f build/helloworld/ubuntu
rm -r -f build/helloworld/linux
rm -r -f build/helloworld/windows
# Execute the Briefcase commands
briefcase create
briefcase build
briefcase package --adhoc-sign
briefcase run