#!/usr/bin/python3

#*************************************************************************
#  WireGuard Configuration Updated
#  
#  This script updates a WireGuard interface's configuration with
#  when the endpoint's IP address changes (a useful feature for homelab
#  that do not have fixed addresses).
#
#**************************************************************************


import os
import argparse
import socket
from configparser import RawConfigParser

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', required=True, help='Configuration file to update')
parser.add_argument('-d', '--domain', required=True, help='DynDNS/Domain name to resolve')
parser.add_argument('-i', '--interface', required=True, help='The name of the interface/service to update')
args = parser.parse_args()
print(args.domain)

# resolve endpoint DynamicDNS IP address
dynamicdns = args.domain
dynamicdns_ip = socket.gethostbyname(dynamicdns)
print(dynamicdns_ip)


# read configuration file
config_file_name = args.filename
config = RawConfigParser()
config.optionxform = str
config.read(config_file_name)

# Get current endpoint address
endpoint = config.get("Peer", "Endpoint").split(":")
endpoint_ip = endpoint[0]
endpoint_port = endpoint[1]
print(endpoint[0])

# Check if address needs to be updated
if dynamicdns_ip != endpoint_ip:
    print("let's change")
    os.popen("sudo systemctl stop wg-quick@" + args.interface + ".service").read()
    config.set("Peer", "Endpoint", dynamicdns_ip + ":" + endpoint_port)
    config_file = open(config_file_name, "w")
    config.write(config_file)
    config_file.close()
    os.popen("sudo systemctl start wg-quick@" + args.interface + ".service").read()
               
else:
    print("nothing to do")