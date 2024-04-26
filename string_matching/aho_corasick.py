class noeud:
    def __init__(self):
        self.enfants = {}               # dictionnaire des enfants {char : noeud}     
        self.terminal = (False, None) # (est terminal ? , motif si oui)
        self.echec = None   # pointer vers le noeud echec


class AhoCorasick:
    def __init__(self):
        self.racine = noeud()        
        self.racine.echec = self.racine  # par defaut la racine pointe son echec vers elle meme
    
    def ajouter(self, motif):     
        node = self.racine
        for char in motif:                      # pour chaque caractere du motif
            if char not in node.enfants:        # si le caractere n'est pas dans les enfants du noeud
                node.enfants[char] = noeud()    # on l'ajoute
            node = node.enfants[char]           # on descend d'un niveau
        node.terminal = (True, motif)           # on marque le noeud comme terminal et on stocke le motif
    
    def echecs(self):
        file = []
        racine = self.racine
        for enfant in racine.enfants.values():  # on ajoute les enfants de la racine dans la file
            file.append(enfant)                 
            enfant.echec = racine                # par defaut, tous les noeuds pointent leur echec vers la racine

        while file:                                     # tant que la file n'est pas vide
            node = file.pop(0)                          # on prend le premier noeud de la file
            for char, enfant in node.enfants.items():   # pour chaque enfant du noeud
                file.append(enfant)                     # on l'ajoute dans la file
                echec = node.echec                      # on initialise l'echec du noeud
                while echec != self.racine and char not in echec.enfants:   # on cherche le noeud echec
                    echec = echec.echec                 # en remontant dans l'arbre
                enfant.echec = echec.enfants[char] if char in echec.enfants else self.racine    # on le stocke dans l'enfant


    def recherche(self, texte):                         
        found = []
        node = self.racine
        itt = 0
        for i, char in enumerate(texte):                            # pour chaque caractere du texte
            while node != self.racine and char not in node.enfants: # on cherche le noeud correspondant au caractere dans l'arbre
                node = node.echec                                   
            itt += 1
            if char in node.enfants:
                node = node.enfants[char]                        # on descend d'un niveau
            itt += 1
            if node.terminal[0]:                                # si le noeud est terminal on stocke le motif et sa position
                found.append((i-len(node.terminal[1])+1, node.terminal[1]))
        return (found, itt)

