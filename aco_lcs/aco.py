import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def aco(w1, w2, ants=1, iterations=5, evaporation=0.5, show_animation = {"show": False, "interval": 200, "repeat": True, "FromEnd": True}):
    """
        w1: str > First word
        w2: str > Second word
        ants: int > Number of ants
        iterations: int > Number of iterations
        evaporation: float > Evaporation rate (0 < evaporation < 1)
        show_animation: dict > Show the animation of the pheromone matrix
            "show" > Bool: If the animation should be shown
            "interval" > int: Interval between frames
            "repeat" > Bool: If the animation should repeat
            "FromEnd" > Bool: If the last iteration only should be shown
        
        return: tuple > (best_path, best_score, best_length)
            best_path: list > List of moves
            best_score: int > Number of matches
            best_length: int > Length of the best path
    """
    
    
    mat = np.zeros((len(w2) + 1, len(w1) + 1))
    
    for i in range(1, len(w2) + 1):
        for j in range(1, len(w1) + 1):
            if w2[i - 1] == w1[j - 1]:
                mat[i, j] = 1
    pherm = [] # pour l'animation
    pheromone = np.ones((mat.shape[0] + 1, mat.shape[1] + 1))
    pheromone[0, :] = 0
    pheromone[:, 0] = 0
    pheromone[mat.shape[0], :] = 0
    pheromone[:, mat.shape[1]] = 0

    best = ([], 0)
    for _ in range(iterations):
        ant_tour = []
        for _ in range(ants):
            moves = []
            LSC = 0
            i, j = 0, 0
            added_i, added_j = -1, -1
            found = ""
            while i < len(w2) or j < len(w1) :  
                probs = sum([pheromone[i + 1, j], pheromone[i, j + 1], pheromone[i + 1, j + 1]])  
                if probs == 0:
                    break
                move = np.random.choice(['down', 'right', 'middle'], p=[pheromone[i + 1, j] / probs, pheromone[i, j + 1] / probs, pheromone[i + 1, j + 1] / probs])  # Swap i and j
                if move == 'down':
                    i += 1  
                elif move == 'right':
                    j += 1  
                elif move == 'middle':
                    i += 1  
                    j += 1 
                if (i < len(w2)+1 or j < len(w1)+1) and mat[i, j] == 1 and (added_j != j and added_i != i):
                    LSC += 1
                    found += w1[j-1]
                    added_i = i
                    added_j = j
                moves.append(move)
            ant_tour.append((moves, LSC))
            if LSC > best[1]:
                best = (moves, LSC, len(moves), found)

        # update pheromones matrix
        for ant in ant_tour:
            moves, LSC = ant
            if LSC == 0:
                continue
            i, j = 0, 0 
            for move in moves:
                if move == 'down':
                    i += 1 
                elif move == 'right':
                    j += 1 
                elif move == 'middle':
                    i += 1 
                    j += 1 
                pheromone[i, j] = pheromone[i, j] + (LSC / (max(len(w1), len(w2))) ) 

        # evaporation  
        for i in range(pheromone.shape[0] - 1):
            for j in range(pheromone.shape[1] - 1):
                pheromone[i,j] = pheromone[i,j]*(1 - evaporation) if pheromone[i,j]*(1 - evaporation) > 0.8 else 0.8 if pheromone[i,j] != 0 else 0
        
        pherm.append(pheromone.copy())
    if show_animation["show"]:
        def update(iteration):
            plt.clf()
            plt.title(f"Iteration: {iteration+1}")
            plt.imshow(pherm[iteration], cmap='coolwarm', interpolation='nearest')
            plt.colorbar()
        
        fig = plt.figure()
        if show_animation["FromEnd"]:
            plt.title(f"Iteration: {iterations}")
            plt.xticks(range(len(w1)+1), [''] + list(w1))
            plt.yticks(range(len(w2)+1), [''] + list(w2))
            plt.imshow(pherm[-1], cmap='coolwarm', interpolation='nearest')
            plt.colorbar()
        else:
            ani = animation.FuncAnimation(fig, update, frames=iterations, interval=show_animation["interval"], repeat=show_animation["repeat"])
        
        plt.show()
    return best

def recherche_aco(all_strings, ants=1, iterations=5, evaporation=0.5, prints = True, show_animation = {"show": False, "interval": 200, "repeat": True, "FromEnd": True}):
    if len(all_strings) < 2:
        return -1
    if prints:
        r = 0
        print( ["/","|","\\","—"][r%4]+ " "  + str(int((r/(len(all_strings)))*100)) + "%" , end="\r")
        r+= 1
    path, best, cost, found = aco(all_strings[0], all_strings[1], ants, iterations, evaporation, show_animation=show_animation)
    all_strings = all_strings[2:]
    for word in all_strings:
        if prints:
            print( ["/","|","\\","—"][r%4]+ " "  + str(int((r/(len(all_strings)))*100)) + "%" , end="\r")
            r += 1
        path, best, cost, found = aco(found, word, ants, iterations, evaporation, show_animation=show_animation)
    print("\r")
    return best, found