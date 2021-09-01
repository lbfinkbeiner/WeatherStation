"""
    File name: telnet_receiver.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/1/2021
    Python version: 3.7.3
"""

HOST_ws1 = 'weatherport-primary.hcro.org'
PORT_ws1 = 4001

HOST_ws2 = 'weatherport-secondary.hcro.org'
PORT_ws2 = 4001

from telnetlib import Telnet

def receive(feed, HOST, PORT):
    with Telnet(HOST, PORT) as tn:
        latest = ""
        while True:
            next_byte = tn.read_eager()
            try:
                next_char = next_byte.decode("ascii")
                if next_char.isspace():
                    feed["raw"] = latest
                    # publish the change
                    feed["updated"] = True
                    latest = ""
                else:
                    latest += next_char
            except UnicodeDecodeError:
                # I am not really sure what I should do
                # about this, if anything
                latest = ""

# This section is a bit dumb, but we only have
# two weather stations, so it's easy and readable
def receive_from_ws1(feed):
    receive(feed, HOST_ws1, PORT_ws1)

def receive_from_ws2(feed):
    receive(feed, HOST_ws2, PORT_ws2)
