# coding: utf-8

import socket
import sys
import getpass

if len(sys.argv) != 2:
    sys.exit("Arguments erronés! Veuillez vérifier le nombre de paramètres")
elif sys.argv[1] == "UDP":
    protocole = "UDP"
    socketMachineCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
elif sys.argv[1] == "TCP":
    protocole = "TCP"
    socketMachineCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    sys.exit("Le protocole %s n'est pas supporté" % (str(sys.argv[1])))

hote = "localhost"
port = 17171

if protocole == "TCP":
    try:
        socketMachineCliente.connect((hote, port))
    except ConnectionRefusedError:
        sys.exit("Le service est temporairement indisponible! \nVeuillez réessayer plus tard")
    quitter = 0
    while quitter == 0:
        print("*********************** \nVous êtes un ?\nV: Vendeur \nC: Client \nQ: Quitter")
        choix = input("Choix: ")
        socketMachineCliente.send(choix.encode())
        if choix == "C":
            print((socketMachineCliente.recv(255)).decode('UTF-8'))
            try:
                choix = input("Veuillez indiquer votre choix SVP: ")
                socketMachineCliente.send(choix.encode())
                choix = int(choix)
            except ValueError:
                sys.exit("Vous devriez entrer un entier! Veuillez réessayer de nouveau")
            if choix == 1:
                print((socketMachineCliente.recv(255)).decode('UTF-8'), end="")
                socketMachineCliente.send(input().encode())
                refprod = input("La référence du produit: ")
                socketMachineCliente.send(refprod.encode())
                msg = (socketMachineCliente.recv(40)).decode('UTF-8')
                if msg[0] == "1":
                    print(msg[3:])
                elif msg[0] == "2":
                    qt = input(msg[3:])
                    socketMachineCliente.send(qt.encode())
                    msg = (socketMachineCliente.recv(300)).decode('UTF-8')
                    if msg[0] == "3":
                        print(msg[3:])
                    elif msg[0] == "4":
                        print(msg[3:])
            else:
                print("Choix incorrect!")
        elif choix == "V":
            print((socketMachineCliente.recv(255)).decode('UTF-8'))
            choix_ = input("Veuillez indiquer votre choix SVP: ")
            try:
                choix = int(choix_)
            except ValueError:
                sys.exit("Vous devriez entrer un entier! Veuillez réessayer de nouveau")
            socketMachineCliente.send(choix_.encode())

            if choix == 1:
                refprod = input("La référence du produit: ")
                try:
                    rp = int(refprod)
                except ValueError:
                    sys.exit("Vous devriez entrer un entier! Veuillez réessayer de nouveau")
                socketMachineCliente.send(refprod.encode())
                res = (socketMachineCliente.recv(4000)).decode('UTF-8')
                res = res.split('*')
                for i in range(0, len(res)):
                    print(res[i], end="")
            elif choix == 2:
                print("Vous devriez être un administrateur pour effectuez cette opération:")
                m2pass = getpass.getpass('Veuillez SVP entrer le mot de passe administrateur: ')
                socketMachineCliente.send(m2pass.encode())
                rep = (socketMachineCliente.recv(20)).decode('UTF-8')
                if rep == "ok":
                    idclt = input("L'identificateur client: ")
                    try:
                        idc = int(idclt)
                    except ValueError:
                        sys.exit("Vous devriez entrer un entier! Veuillez réessayer de nouveau")
                    socketMachineCliente.send(idclt.encode())
                    res = (socketMachineCliente.recv(4000)).decode('UTF-8')
                    res = res.split('*')
                    for i in range(0, len(res)):
                        print(res[i], end="")
                else:
                    print("Mot de passe incorrect!")
            elif choix == 3:
                res = (socketMachineCliente.recv(8000)).decode('UTF-8')
                res = res.split('*')
                for i in range(0, len(res)):
                    print(res[i], end="")
            else:
                print("Choix incorrect!")
        elif choix == "Q":
            quitter = 1
        else:
            print("Choix incorrect!")
else:
    adrServ = (hote, port)
    socketMachineCliente.sendto("je_commence".encode(), adrServ)
    quitter = 0
    while quitter == 0:
        print((socketMachineCliente.recv(255)).decode('UTF-8'))
        choix = input("Choix: ")
        socketMachineCliente.sendto(choix.encode(), adrServ)

        if choix == "C":
            print((socketMachineCliente.recv(255)).decode('UTF-8'))
            try:
                choix = input("Veuillez indiquer votre choix SVP: ")
                socketMachineCliente.sendto(choix.encode(), adrServ)
                choix = int(choix)
            except ValueError:
                socketMachineCliente.close()
                sys.exit("Vous devriez entrer un entier! Veuillez réessayer de nouveau")
            if choix == 1:
                print((socketMachineCliente.recv(255)).decode('UTF-8'), end="")
                socketMachineCliente.sendto(input().encode(), adrServ)
                refprod = input("La référence du produit: ")
                socketMachineCliente.sendto(refprod.encode(), adrServ)
                msg = (socketMachineCliente.recv(40)).decode('UTF-8')
                if msg[0] == "1":
                    print(msg[3:])
                elif msg[0] == "2":
                    qt = input(msg[3:])
                    socketMachineCliente.sendto(qt.encode(), adrServ)
                    msg = (socketMachineCliente.recv(300)).decode('UTF-8')
                    if msg[0] == "3":
                        print(msg[3:])
                    elif msg[0] == "4":
                        print(msg[3:])
            else:
                print("Choix incorrect!")
        elif choix == "V":
            print((socketMachineCliente.recv(255)).decode('UTF-8'))
            choix_ = input("Veuillez indiquer votre choix SVP: ")
            try:
                choix = int(choix_)
            except ValueError:
                sys.exit("Vous devriez entrer un entier! Veuillez réessayer de nouveau")
            socketMachineCliente.sendto(choix_.encode(), adrServ)

            if choix == 1:
                refprod = input("La référence du produit: ")
                socketMachineCliente.sendto(refprod.encode(), adrServ)
                res = (socketMachineCliente.recv(4000)).decode('UTF-8')
                res = res.split('*')
                for i in range(0, len(res)):
                    print(res[i], end="")
            elif choix == 2:
                idclt = input("L'identificateur client: ")
                socketMachineCliente.sendto(idclt.encode(), adrServ)
                res = (socketMachineCliente.recv(4000)).decode('UTF-8')
                res = res.split('*')
                for i in range(0, len(res)):
                    print(res[i], end="")
            elif choix == 3:
                res = (socketMachineCliente.recv(8000)).decode('UTF-8')
                res = res.split('*')
                for i in range(0, len(res)):
                    print(res[i], end="")
            else:
                print("Choix incorrect!")
        elif choix == "Q":
            quitter = 1
            print()
        else:
            print("Choix incorrect!")

print("Session terminée")
socketMachineCliente.close()
