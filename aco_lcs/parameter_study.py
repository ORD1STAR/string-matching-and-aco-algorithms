import numpy as np
import matplotlib.pyplot as plt
import time

from aco import recherche_aco
from dfs import recherche_dfs

aco_data = {}
dfs_data = {}
texts = ["ATCGATCGATCG", "ATGCGTACGCTA", "AGCTAGCTAGCT", "CTAGCTAGCTAG", "CGATCGATCGAT"]
LCS = 5

####            =====================================    ACO   =====================================
_id = 0
ants_n = range(1,21)
itt_n = range(1,21)
evap_n = np.arange(0.1, 1, 0.1)
for ant in ants_n:
    for itt in itt_n:
        for evap in evap_n:
            start = time.time()
            best1, _ = recherche_aco(texts, ant, itt, evap, prints=False)
            end1 = time.time() - start
            start = time.time()
            best2, _ = recherche_aco(texts, ant, itt, evap, prints=False)
            end2 = time.time() - start
            start = time.time()
            best3, _ = recherche_aco(texts, ant, itt, evap, prints=False)
            end3 = time.time() - start
            best = max([best1, best2, best3])
            aco_data[_id] = [ant, itt, evap, (end1 + end2 + end3) / 3, best]
            _id += 1
            print(f"\r{str(round(round((_id / (len(ants_n) * len(itt_n) * len(evap_n))), 4) * 100, 2))}%", end="")

ants = [aco_data[i][0] for i in aco_data]
itts = [aco_data[i][1] for i in aco_data]
evaps = [aco_data[i][2] for i in aco_data]
times = [aco_data[i][3] for i in aco_data]
acc = [aco_data[i][4]/LCS for i in aco_data]

plt.figure("ACO Time Comparaison")

plt.scatter(itts, times, c=ants, cmap='coolwarm', edgecolors='black', linewidths=0.5)
plt.colorbar(values = ants, label='Ants Population Density')
plt.xlabel("Iterations")
plt.ylabel("Time")
plt.title("Iterations vs Time")

plt.figure("ACO Accuracy Comparaison (Ant Population Parameter)")
plt.scatter(acc, times, c=ants, cmap='coolwarm', edgecolors='black', linewidths=0.5)
plt.colorbar(values = ants, label='Ants Population Density')
plt.xlabel("Accuracy")
plt.ylabel("Time")
plt.title("Accuracy vs Time (Ant Population Parameter)")

plt.figure("ACO Accuracy Comparaison (Itterations Parameter)")
plt.scatter(acc, times, c=itts, cmap='coolwarm', edgecolors='black', linewidths=0.5)
plt.colorbar(values = itts, label='Itterations')
plt.xlabel("Accuracy")
plt.ylabel("Time")
plt.title("Accuracy vs Time (Itterations Parameter)")


####            =====================================    DFS   =====================================
start = time.time()
best1, _ = recherche_dfs(texts, prints=False)
end1 = time.time() - start
start = time.time()
best2, _ = recherche_dfs(texts, prints=False)
end2 = time.time() - start
start = time.time()
best3, _ = recherche_dfs(texts, prints=False)
end3 = time.time() - start
best = max([best1, best2, best3])
print("DFS:")
print("FINAL time:", (end1 + end2 + end3) / 3)
print("accuracy:", best/LCS)



plt.show()