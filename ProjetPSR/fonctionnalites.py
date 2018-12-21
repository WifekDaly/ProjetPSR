# -*- coding: utf-8 -*-

# fonction pour consulter le stock d'un produit
def conStoProd(refprod, verrou):
    res = []
    with verrou:
        with open('stock.txt', 'r') as fichierStock:
            listeStock = fichierStock.readlines()
    for i in range(0, 3):
        res.append(listeStock[i])
    for i in range(3, len(listeStock), 2):
        listeMots = listeStock[i]
        listeMotsModif = listeMots.replace(' ', '')
        listeInfo = listeMotsModif.split('|')
        for j in range(0, len(listeInfo) - 1):
            if (not listeInfo[j]) or ("\n" in listeInfo[j]):
                listeInfo.pop(j)
        if (int(listeInfo[0]) == refprod):
            res.append(listeMots)
            res.append(listeStock[0])
    return res

# fonction pour la consultation de facture d'un client
def conFacClient(idClient, verrou):
    res = []
    with verrou:
        with open('facture.txt', 'r') as fichierFac:
            listeFac = fichierFac.readlines()
    for i in range(0, 3):
        res.append(listeFac[i])
    for i in range(3, len(listeFac), 2):
        listeMots = listeFac[i]
        listeMotsModif = listeMots.replace(' ', '')
        listeInfo = listeMotsModif.split('|')
        for j in range(0, len(listeInfo) - 1):
            if (not listeInfo[j]) or ("\n" in listeInfo[j]):
                listeInfo.pop(j)
        if (int(listeInfo[0]) == idClient):
            res.append(listeMots)
            res.append(listeFac[0])
    return res

# fonction pour consulter l'historique de commandes
def conHistoCom(verrou):
    with verrou:
        with open('histo.txt', 'r') as fichierHisto:
            res = fichierHisto.readlines()
    return res

# fonction qui effectue l'achat d'un produit spécifique
def acheterProduit(idClient, machineCliente, verrou,q,adrClient):
    with verrou:
        with open('stock.txt', 'r') as fichierStock:
            listeProd = fichierStock.readlines()
    if (q is None):
        refprod = int((machineCliente.recv(10)).decode('UTF-8'))
    else :
        refprod = int(q.get())
    existe = False
    listeEntete = []
    for i in range(0, 3):
        listeEntete.append(listeProd[i])
    for i in range(3, len(listeProd), 2):
        listeMots = listeProd[i]
        listeMotsModif = listeMots.replace(' ', '')
        listeInfo = listeMotsModif.split('|')
        for j in range(0, len(listeInfo) - 1):
            if (not listeInfo[j]) or ("\n" in listeInfo[j]):
                listeInfo.pop(j)
        if int(listeInfo[0]) == refprod:
            existe = True
            indiceProd = i
            break
    # si le code du produit démandé est inexistant
    if existe == False:
        if (q is None):
            machineCliente.send("1. Produit non disponible!".encode())
        else:
            machineCliente.sendto("1. Produit non disponible!".encode(),adrClient)
            return
    else:
        if (q is None):
            machineCliente.send("2. La quantité demandée :".encode())
            quantite = int(machineCliente.recv(20).decode('UTF-8'))
        else:
            machineCliente.sendto("2. La quantité demandée :".encode(),adrClient)
            quantite = int(q.get())

        listeInfoProd = ((listeProd[indiceProd]).replace(' ', '')).split('|')
        for j in range(0, len(listeInfoProd) - 1):
            if (not listeInfoProd[j]) or ("\n" in listeInfoProd[j]):
                listeInfoProd.pop(j)

        # si la quantité demandée est supérieure à la quantité du stock
        if (int(listeInfoProd[2]) < quantite):
            if (q is None) :
                machineCliente.send(("3. La quantité demandée n'est pas disponible!").encode())
            else :
                machineCliente.sendto("3. La quantité demandée n'est pas disponible!".ecoode(),adrClient)
            # enregistrement dans l'historique de commandes
            with verrou:
                with open('histo.txt', 'a') as fichierHisto:
                    com = "| "
                    com = com + str(idClient)
                    com = com + ' ' * (22 - (len(str(idClient))))
                    com = com + "| "
                    com = com + str(refprod)
                    com = com + ' ' * (19 - len(str(refprod)))
                    com = com + "| "
                    com = com + str(quantite)
                    com = com + ' ' * (17 - len(str(quantite)))
                    com = com + "| echec"
                    com = com + ' ' * 5
                    com = com + '|\n'
                    fichierHisto.write(com)
                    fichierHisto.write('-' * 77 + '\n')
            return
        else:
            listeInfoProd[2] = int(listeInfoProd[2]) - quantite
            paye = int(listeInfoProd[1]) * quantite
            AvantRef = "| "
            MAJProd = AvantRef + listeInfoProd[0]
            MAJProd = MAJProd + ' ' * (18 - len(str(listeInfoProd[0])))
            MAJProd = MAJProd + "| "
            MAJProd = MAJProd + listeInfoProd[1]
            MAJProd = MAJProd + ' ' * (16 - len(str(listeInfoProd[1])))
            MAJProd = MAJProd + "| "
            MAJProd = MAJProd + str(listeInfoProd[2])
            MAJProd = MAJProd + ' ' * (6 - len(str(listeInfoProd[2])))
            MAJProd = MAJProd + '|\n'
            listeProd[indiceProd] = MAJProd;

            with verrou:
                with open('stock.txt', 'w+') as fichierStock:
                    for k in range(0, len(listeEntete)):
                        fichierStock.write("%s" % listeEntete[k])
                    for k in range(3, len(listeProd)):
                        fichierStock.write("%s" % listeProd[k])

            with verrou:
                with open('histo.txt', 'a') as fichierHisto:
                    com = "| "
                    com = com + str(idClient)
                    com = com + ' ' * (22 - (len(str(idClient))))
                    com = com + "| "
                    com = com + str(refprod)
                    com = com + ' ' * (19 - len(str(refprod)))
                    com = com + "| "
                    com = com + str(quantite)
                    com = com + ' ' * (17 - len(str(quantite)))
                    com = com + "| succes"
                    com = com + ' ' * 4
                    com = com + '|\n'
                    fichierHisto.write(com)
                    fichierHisto.write('-' * 77 + '\n')
            # ajout d'une nouvelle facture
            with verrou:
                with open('facture.txt', 'a') as fichierFact:
                    fac = "| " + str(idClient)
                    fac = fac + ' ' * (22 - len(str(idClient))) + "| " + str(paye) + ' ' * (16 - len(str(paye))) + "|\n"
                    fichierFact.write(fac)
                    fichierFact.write('-' * 43 + '\n')
            if (q is None):
                machineCliente.send(
                ("4. Votre commande a été effectué avec succés\nVous devriez payer " + str(paye)).encode())
            else :
                machineCliente.sendto(
                    ("4. Votre commande a été effectué avec succés\nVous devriez payer " + str(paye)).encode(),adrClient)
