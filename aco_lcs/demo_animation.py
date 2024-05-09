from aco import aco, recherche_aco

texts = ["AAAArtzAAAAAAAAAArpvAAA6AAAzyuAAAAALSRAAA", 
         "AAAAAAAAAAAAAyxhnAAAAAAAAAAAAAAAAAutrxAAA", 
         "AAAjgfrqAAAAAAAAAAAAAAAAAAAAAAAAAAetyjAAA",
         "AAAAAAAGE SDAAAAAAAAAluyjhàAAAAAAAAAAAAJAA"
         ] # real LCS 30

best = aco(texts[0], texts[1], ants=10, iterations=50, evaporation=0.4, show_animation={"show": True, "interval": 300, "repeat": True, "FromEnd": False})
print(best[1])
print(best[3])

# best, found = recherche_aco(texts, 20, 100, 0.8)
# print(best)
# print(found)