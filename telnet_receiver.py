"""
    File name: telnet_receiver.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 8/30/2021
    Python version: 3.7.3
"""

from telnetlib import Telnet
HOST = 'weatherport-primary.hcro.org'
PORT = 4001

def receive(feed):
    with Telnet(HOST, PORT) as tn:
        latest = ""
        while True: # gross
            next_byte = tn.read_eager()
            try:
                next_char = next_byte.decode("ascii")
                if next_char.isspace():
                    feed["value"] = latest
                    # publish the change
                    feed["changed"] = True
                    latest = ""
                else:
                    latest += next_char
            except UnicodeDecodeError:
                # I am not really sure what I should do
                # about this, if anything
                #print("error")
                #print(latest)
                latest = ""
