import numpy as np

def generate_moves(n, m): 
    results = [] # we start with an empty string
    def generate_moves(x, y, path): # recusive function
        if x == n - 1 and y == m - 1: # le cas de base if x and y sont arrivé a la derniere case .. on arrete re ajoute le chemin parcourut
            results.append(path)
            return

        if y + 1 < m: # si on peut aller a droite
            generate_moves(x, y + 1, path + ["r"]) # on y va w on ajoute le chemin r (right)
        
        if x + 1 < n:  # si on peut aller en bas
            generate_moves(x + 1, y, path + ["v"]) # on y va w on ajoute le chemin v (bas)
        
        if x + 1 < n and y + 1 < m: # si on peut aller en diagonale
            generate_moves(x + 1, y + 1, path + ["d"]) # on y va w on ajoute le chemin d (diagonale)
        # on refait tout cela dans tout les cas

    generate_moves(0, 0, [])
    # on commence par la case 0 0 avec aucun chemin
    return results


def dfs_algorithm(w1, w2):
    mat = np.zeros((len(w2), len(w1)))

    for i in range(len(w2)):
        for j in range(len(w1) ):
            if w2[i ] == w1[j]:
                mat[i, j] = 1
    best = 0
    best_commun = ""
    path = []

    moves = generate_moves(len(w2), len(w1))
    all_moves = moves.copy()
    while moves:
        move = moves.pop()
        lrc_counter = 0
        commun = ""
        
        i, j = 0, 0
        fi, fj = -1, -1
        if mat[i, j] == 1:
            lrc_counter += 1
            fi = i
            fj = j
            commun += w1[j]
        for m in move:
            if m == 'r': 
                j += 1
            elif m == 'v':
                i += 1
            else:
                i += 1
                j += 1
            if i < len(w2) and j < len(w1) and mat[i, j] == 1 and i != fi and j != fj:
                lrc_counter += 1
                commun += w1[j]
                fi = i
                fj = j
        if lrc_counter > best:
            best = lrc_counter
            best_commun = commun
            path = move
        
    return best,best_commun, path, all_moves

def recherche_dfs(all_strings, prints = True):
    if len(all_strings) < 2:
        return -1
    r = 0
    if prints:
        print( ["/","|","\\","—"][r%4]+ " "  + str(int((r/(len(all_strings)))*100)) + "%" , end="\r")
    best, commun, _, _ = dfs_algorithm(all_strings[0], all_strings[1])
    r += 1
    all_strings = all_strings[2:]
    
    for word in all_strings:
        if prints:
            print( ["/","|","\\","—"][r%4]+ " "  + str(int((r/(len(all_strings)))*100)) + "%" , end="\r")
        best, commun, path, _ = dfs_algorithm(commun, word)
    return best, commun