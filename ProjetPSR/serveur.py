# -*- coding: utf-8 -*-

import sys
import queue
import socket
import time
from ThreadClientUdp import clientUdp
from ThreadClientTCP  import clientTCP
from threading import Lock

liste = dict()

if len(sys.argv) != 2:
    sys.exit("Arguments erronés! Veuillez vérifier le nombre de paramètres")
elif sys.argv[1] == "UDP":
    protocole = "UDP"
    socketServeur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
elif sys.argv[1] == "TCP":
    protocole = "TCP"
    socketServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    sys.exit("Le protocole %s n'est pas supporté" % (str(sys.argv[1])))

socketServeur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketServeur.bind(('', 17171))


verrou = Lock()
if protocole == "TCP":
    print("Serveur en écoute ...")
    while True:
        socketServeur.listen(5)
        (machineCliente, (addr, port)) = socketServeur.accept()
        thCliente = clientTCP(addr, port, machineCliente, verrou)
        thCliente.start()
else:
    print("Serveur en attente ...")
    while True :
        (donnee, (adr, port)) = socketServeur.recvfrom(50)
        if donnee.decode() == "je_commence":
            q = queue.Queue()
            liste[str(adr),port] = clientUdp(adr,port,socketServeur,verrou,q)
            liste[str(adr),port].start()
            print("En communication avec le client ayant l'adresse %s sur le port %s" % (str(adr), str(port)), end='')
        else :
            time.sleep(0.1)
            liste[str(adr), port].q.put(donnee.decode())

socketServeur.close()
