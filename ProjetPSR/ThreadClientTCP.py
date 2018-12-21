import sys
from threading import Thread
from threading import Lock
from fonctionnalites import acheterProduit
from fonctionnalites import conFacClient
from fonctionnalites import conHistoCom
from fonctionnalites import conStoProd

class clientTCP(Thread):

    def __init__(self, adr, port, serveur):
        Thread.__init__(self)
        self.adr = adr
        self.port = port
        self.machineCliente = serveur


    def run(self):

        print("Connecté à l'adresse: %s sur le port %s " % (str(self.adr), str(self.port)))
        quitter = 0
        # tant que le client n'a pas choisi Quitter
        while quitter == 0:
            choix = (self.machineCliente.recv(22)).decode('UTF-8')
            # si "Client" est choisie
            if choix == "C":
                self.machineCliente.send("(1) .Acheter un produit".encode())
                try:
                    choix = int((self.machineCliente.recv(40)).decode('UTF-8'))
                except ValueError:
                    self.machineCliente.close()
                    sys.exit()
                if choix == 1:
                    self.machineCliente.send("Votre identificateur: ".encode())
                    acheterProduit(int((self.machineCliente.recv(255)).decode('UTF-8')), self.machineCliente,
                                       self.verrou,None,None)
                else:
                    self.machineCliente.send("Choix incorrect!".encode())
            elif choix == "V":
                self.machineCliente.send(
                    "(1) .Consulter le stock d'un produit\n(2) .Consulter les factures d'un client\n(3) .Consulter l'historique des commandes".encode())
                try:

                    choix = int((self.machineCliente.recv(40)).decode('UTF-8'))
                except ValueError:
                    sys.exit()

                if choix == 1:
                    try:
                        refprod = int(((self.machineCliente.recv(40)).decode('UTF-8')))
                    except ValueError:
                        sys.exit()
                    res = conStoProd(refprod, self.verrou)
                    res = "*".join(res)
                    self.machineCliente.send(res.encode())
                elif choix == 2:
                    m2p = (self.machineCliente.recv(40)).decode('UTF-8')
                    #with open('mot_de_passe', 'r') as fichierM2P:
                        #listeInfo = fichierM2P.readlines()
                    #algorithmeCipher = Fernet(listeInfo[1].encode())
                    #m2pVrai = algorithmeCipher.decrypt(listeInfo[0].encode())
                    if "pass" == m2p:
                        self.machineCliente.send("ok".encode())
                        try:
                            idclt = int((self.machineCliente.recv(40)).decode('UTF-8'))
                        except ValueError:
                            sys.exit()
                        res = conFacClient(idclt, self.verrou)
                        res = "*".join(res)
                        self.machineCliente.send(res.encode())
                    else:
                        self.machineCliente.send("...".encode())
                elif choix == 3:
                    res = "*".join(conHistoCom(self.verrou))
                    self.machineCliente.send(res.encode())
                else:
                    print()
            elif choix == "Q":
                quitter = 1
            else:
                print()
