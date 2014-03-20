from twisted.internet import task

from p2pserver import P2PServer

import sys
import time
import uuid

PING_INTERVAL = 1.0

class Client:
    
    def __init__(self, optimalNumPeers, startPort, endPort, sendPings, pingsInterval ):

        self.optNumPeers    = optimalNumPeers
        self.startPort      = startPort
        self.endPort        = endPort
        self.sendPings      = sendPings
        self.pingsInterval  = pingsInterval

        self.lastPingTime = 0.0
        self.publicKey = uuid.uuid1().get_hex()
        self.p2pserver = None

        self.doWorkTask = task.LoopingCall(self.__doWork)
        self.doWorkTask.start(0.1, False)
        self.lastPingTime = time.time()

    def startNetwork(self, seedHost, seedHostPort):
        print "Starting network ..."
        self.p2pserver = P2PServer(1, self.startPort, self.endPort, self.publicKey, seedHost, seedHostPort)

    def stopNetwork(self):
        #FIXME: Pewnie cos tu trzeba jeszcze dodac. Zamykanie serwera i wysylanie DisconnectPackege
        self.p2pserver = None

    def connect(self, address, port):
        if self.p2pserver:
            self.p2pserver.connect(address, port)
        else:
            print "Trying to connect when server is not started yet"

    def __doWork(self):
        if self.sendPings:
            self.p2pserver.pingPeers( self.pingsInterval )
            
