# Cisco-Send-Commands
Send commands to a number of Cisco devices using Netmiko

Create a file in the same directory as this script called devices.txt with the IP/FQDN of your devices, on per line.

Update the commands in the config_commands that you want to run from global configuration mode.

When you run the script you will be prompted for your credentials.  Since this is a for loop for each device, it will take longer than Nornir to run.

Output will be created in out.txt in the same directory as the script.
