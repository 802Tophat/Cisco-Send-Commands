from __future__ import absolute_import, division, print_function

from netmiko import ConnectHandler
from getpass import getpass
import os
import signal
import sys
import time

signal.signal(signal.SIGINT, signal.SIG_DFL)

def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line

def get_credentials():
    """Prompt for and return a username and password."""
    USERNAME = get_input('Enter Username: ')
    PASSWORD = None
    while not PASSWORD:
        PASSWORD = getpass()
        password_verify = getpass('Retype your password: ')
        if PASSWORD != password_verify:
            print('Passwords do not match.  Try again.')
            PASSWORD = None
    return USERNAME, PASSWORD

USERNAME, PASSWORD = get_credentials()

devices = open('devices.txt','r').read()
devices = devices.strip()
devices = devices.splitlines()

success = 0
failure = 0
unreachable = 0

print("Starting Changes")

for device in devices:
    try:
        with open('out.txt', 'a') as DATAFILE:
                net_connect = ConnectHandler(device_type='cisco_ios_ssh', ip=device,
                                             username=USERNAME, password=PASSWORD,
                                             secret=PASSWORD, verbose=True)
                net_connect.enable()
                hostname = net_connect.find_prompt()
                print("Changing passwords on: " + str(hostname) + "\n")
                print(hostname, file=DATAFILE)
                net_connect.send_command('send log START - CHANGE')
                config_commands = ['COMMAND1',
                                   'COMMAND2'
                                  ]
                new_config = net_connect.send_config_set(config_commands)
                print(new_config, file=DATAFILE)
                saveconfig = net_connect.save_config()
                print(saveconfig, file=DATAFILE)
                net_connect.send_command('send log COMPLETE - CHANGE')
                net_connect.disconnect()
                print("Finished change on: " + str(hostname))
                print("\n", file=DATAFILE)
                print("\n")
                success += 1
                time.sleep(7)
    except:
        print ("Unable to reach device " + device)
        print ("FAILURE ON DEVICE: " + str(device) + "\n", file=open("out.txt", "a"))
        unreachable += 1

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
print("Results")
print("Successful: " + str(success))
print("Failures: " + str(failure))
print("Unable to Reach: " + str(unreachable))
DATAFILE.close()
