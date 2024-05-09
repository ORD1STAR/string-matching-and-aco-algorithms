import time
import random

from aco import recherche_aco
from dfs import recherche_dfs

def dynamic_LCS(words):
    def lcs_f(word1, word2):
        if len(word1) == 0 or len(word2) == 0:
            return ""
        if word1[-1] == word2[-1]:
            return lcs_f(word1[:-1], word2[:-1]) + word1[-1]
        else:
            lcs1 = lcs_f(word1[:-1], word2)
            lcs2 = lcs_f(word1, word2[:-1])
            return lcs1 if len(lcs1) > len(lcs2) else lcs2

    lcs = words[0]
    for word in words[1:]:
        lcs = lcs_f(lcs, word)
    return lcs



running = True

words = []

while running:
    print("========== MENU ==========")
    print(f"1. Enter {"new " if len(words) > 1 else ""}sequences")
    print(f"2. Generate {"new " if len(words) > 1 else ""}random sequences")
    if len(words) > 1:
        print("3. Run ACO")
        print("4. Run DFS")
        print("5. Print the sequences")
    print("6. Exit")
    print("==========================")
    choice = input("Enter your choice> ")
    try:
        choice = int(choice)
        assert choice in range(1, 7)
        
        if choice == 1:
            n = input("Enter number of sequences> ")
            try:
                n = int(n)
                assert n > 1
                sequences = []
                for i in range(n):
                    sequences.append(input(f"Enter sequence {i + 1}> "))
                words = sequences
                print()
                continue
            except:
                print("Invalid number of sequences")
                print()
                continue
        elif choice == 2:
            n = input("Enter number of sequences> ")
            try:
                n = int(n)
                assert n > 1
                base = ''.join(random.choice(["A", "T", "C", "G"]) for _ in range(random.randint(3, 7)))
                sequences = []
                for i in range(n):
                    new = base
                    for j in range(random.randint(int(len(base)/3), int(len(base)))):
                        if len(new) >= 11:
                            break
                        s = random.randint(0, len(new))
                        new = new[:s] + random.choice(["A", "T", "C", "G"]) + new[s:]
                    sequences.append(new)
                words = sequences
                print()
                continue
            except:
                print("Invalid number of sequences")
                print()
                continue
        elif choice == 3:
            if len(words) < 2:
                print("Not enough sequences")
                print()
                continue
            ants = input("Enter number of ants> ")
            itt = input("Enter number of iterations> ")
            evap = input("Enter evaporation rate> ")
            try:
                ants = int(ants)
                itt = int(itt)
                evap = float(evap)
                assert ants > 0 and itt > 0 and 0 <= evap < 1
                start = time.time()
                best, found = recherche_aco(words, ants, itt, evap)
                end = time.time() - start

                real_best = dynamic_LCS(words)

                print(f"LCS: {found}")
                print(f"Best length for the LCS: {best}/{len(real_best)}    (found with dynamic programmation)")
                print(f"Time: {end}")
                print()
                continue
            except:
                print("Invalid parameters")
                print()
                continue

        elif choice == 4:
            if len(words) < 2:
                print("Not enough sequences")
                print()
                continue
            start = time.time()
            best, found = recherche_dfs(words)
            end = time.time() - start

            real_best = dynamic_LCS(words)

            print(f"LCS: {found}")
            print(f"Best length for the LCS: {best}/{len(real_best)}    (found with dynamic programmation)")
            print(f"Time: {end}")
            print()
            continue
        
        elif choice == 5:
            print("The sequences are:")
            print("\n".join(words))
            print()
            continue
        elif choice == 6:
            running = False
            continue

    except:
        print("Invalid choice")
        continue

print("Goodbye!")