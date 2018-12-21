import sys
from threading import Thread
from fonctionnalites import acheterProduit
from fonctionnalites import conFacClient
from fonctionnalites import conHistoCom
from fonctionnalites import conStoProd


class clientUdp(Thread):

    def __init__(self, ip, port, socket,v,q):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.q = q
        self.verrou = v

    def run(self):
        print("Connecté à l'adresse: %s sur le port %s " % (str(self.ip), str(self.port)))
        quitter = 0
        while quitter == 0:
            machineCliente = (self.ip, self.port)
            self.socket.sendto ("*********************** \nVous êtes un ?\nV: Vendeur \nC: Client \nQ: Quitter".encode (),
                              machineCliente)
            choix = (self.q.get())
            if choix == "C":
                self.socket.sendto ("(1) Acheter un produit".encode (), machineCliente)
                try:
                    choix = int (self.q.get())
                except ValueError:
                    return
                if choix == 1:
                    self.socket.sendto ("Votre identificateur: ".encode (), machineCliente)
                    try:
                        acheterProduit (int (self.q.get()), self.socket, self.verrou,self.q,machineCliente)
                    except ValueError:
                        return
                else:
                    self.socket.sendto ("Choix incorrect!".encode (), machineCliente)
                    return
            elif choix == "V":
                self.socket.sendto (
                "(1) Consulter le stock d'un produit\n(2) Consulter les factures d'un client\n(3) Consulter l'historique des commandes".encode (),
                machineCliente)
                try:
                    choix = int (self.q.get())
                except ValueError:
                    sys.exit ()
                if choix == 1:
                    refprod = (self.q.get())
                    res = conStoProd (int (refprod),self.verrou)
                    res = "*".join (res)
                    self.socket.sendto (res.encode (), machineCliente)
                elif choix == 2:
                    idclt = int (self.q.get())
                    res = conFacClient (idclt,self.verrou)
                    res = "*".join (res)
                    self.socket.sendto (res.encode (), machineCliente)
                elif choix == 3:
                    res = "*".join (conHistoCom (self.verrou))
                    self.socket.sendto (res.encode (), machineCliente)
                else:
                    print ()
            elif choix == "Q":
                quitter = 1
            else:
                print ()


