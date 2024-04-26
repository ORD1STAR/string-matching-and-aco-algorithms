# Algorithme de Boyer-Moore [BM] (recherche d’un seul motif M de longueur m)

def decalage(c):
        dec = {}
        for i in range(len(c)-1):
            dec[c[i]] = len(c) - i - 1
        return dec

def boyer_moore(T, M):
    # t1 = time.time()
    dec = decalage(M)
    motifI = M[::-1]
    i = len(M) - 1
    itt = 0
    occ = []
    while i < len(T):
        broke = False
        for j,l in enumerate(motifI):
            itt += 1
            if T[i-j] != l:
                broke = True
                break
        if not broke :
            occ.append(i-len(M)+1)
            i+=1
        else:
            if T[i] in dec:
                i += dec[T[i]]
            else:
                i += len(M)
    # t2 = time.time()
    return occ, itt