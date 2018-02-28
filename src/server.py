#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

import json
from db import update_db
from packet import Packet

### Protocol Implementation

# This is just about the simplest possible protocol
class Echo(Protocol):

    def __init__(self):
        self._buffer = ""
        self._client = ""

    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        packets = filter(None, data.split("%"))
        packets = [json.loads(packet) for packet in packets]
        for packet in packets:
            if packet["_header"] == "CLIENT":
                self._client = packet["_payload"]
            elif packet["_header"] == "JSON":
                self._buffer = self._buffer + packet["_payload"].rstrip()
                if self._buffer.endswith('}'):
                    friends = json.loads(self._buffer)
                    friends_u = update_db(friends, self._client)
                    friendsLine = json.dumps(friends_u)
                    packets = Packet.pack("JSON", friendsLine)

                    for packet in packets:
                        data = json.dumps(packet.__dict__)
                        self.transport.write(data + "%")
                    
                    self._buffer = ""
        #self._buffer = self._buffer + data.rstrip()
        



def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    main()