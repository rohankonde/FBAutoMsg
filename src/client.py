#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

from twisted.internet import task, reactor, protocol
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

import json
from packet import Packet

class EchoClient(protocol.Protocol):
    def __init__(self):
        self._buffer = ""
        with open('../data/settings.txt', 'r') as fp:
            self.__client = json.load(fp)["EMAIL"]

    def setClient(client):
        self._client = client

    def connectionMade(self):
        client = Packet("CLIENT", self.__client)
        self.transport.write(json.dumps(client.__dict__) + "%")

        with open('../data/friends.json', 'r') as fp:
            friends = json.load(fp)
        friendsLine = json.dumps(friends)
        packets = Packet.pack("JSON", friendsLine)

        for packet in packets:
            data = json.dumps(packet.__dict__)
            self.transport.write(data + "%")

    def dataReceived(self, data):
        packets = filter(None, data.split("%"))
        packets = [json.loads(packet) for packet in packets]
        for packet in packets:
            if packet["_header"] == "JSON":
                self._buffer = self._buffer + packet["_payload"].rstrip()
                if self._buffer.endswith('}'):
                    friends = json.loads(self._buffer)
                    with open('../data/friends.json', 'w') as fp:
                        json.dump(friends, fp)
                    
                    self._buffer = ""
                    self.transport.loseConnection()



class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)
        reactor.stop()



def main(reactor):
    factory = EchoClientFactory()
    reactor.connectTCP('72.182.103.88', 8000, factory)
    reactor.run(installSignalHandlers=0)
    return factory.done



if __name__ == '__main__':
    task.react(main)