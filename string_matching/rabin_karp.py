def rabin_karp_single_hash(text, pattern):
    n = len(text)
    m = len(pattern)
    p = 31  # prime number for hash function
    d = 256  # number of possible characters
    apparition = []
    faux_positif = 0
    count = 0
    if m > n:
        return (apparition, count), 0
    # Calculate the hash values of the pattern
    pattern_hashes = [0, 0, 0]
    for i in range(m):
        for j in range(3):
            pattern_hashes[j] = (pattern_hashes[j] * d + ord(pattern[i])) % p

    # Calculate the hash values of the first window in the text
    text_hashes = [0, 0, 0]
    for i in range(m):
        for j in range(3):
            text_hashes[j] = (text_hashes[j] * d + ord(text[i])) % p

    # Slide the window over the text and compare the hash values
    for i in range(n - m + 1):
        match = True
        for j in range(3):
            count += 1
            if text_hashes[j] != pattern_hashes[j]:
                match = False
                break
        if match:
            for index, c in enumerate(pattern):
                count += 1
                if c != text[i+index]:
                    faux_positif += 1
                    break
            else:
                apparition.append(i)
        if i < n - m:
            for j in range(3):
                text_hashes[j] = (d * (text_hashes[j] - ord(text[i]) * pow(d, m - 1, p)) + ord(text[i + m])) % p

    return (apparition, count), faux_positif


def rabin_karp_multiple_hashes(text, patterns):
    """
    Implementation of the Rabin-Karp algorithm using three hash functions.
    """
    n = len(text)
    p = 31  # prime number for hash function
    d = 256  # number of possible characters
    count = 0
    apparition = []
    faux_positif = 0

    for pattern in patterns:
        m = len(pattern)
        if m > n:
            break

        # Calculate the hash values of the pattern
        pattern_hashes = [0, 0, 0]
        for i in range(m):
            for j in range(3):
                pattern_hashes[j] = (pattern_hashes[j] * d + ord(pattern[i])) % p

        # Calculate the hash values of the first window in the text
        text_hashes = [0, 0, 0]
        for i in range(m):
            for j in range(3):
                text_hashes[j] = (text_hashes[j] * d + ord(text[i])) % p

        # Slide the window over the text and compare the hash values
        for i in range(n - m + 1):
            match = True
            for j in range(3):
                count += 1
                if text_hashes[j] != pattern_hashes[j]:
                    match = False
                    break
            if match:
                for index, c in enumerate(pattern):
                    count += 1
                    if c != text[i+index]:
                        faux_positif += 1
                        break
                else:
                    apparition.append(i)
            if i < n - m:
                for j in range(3):
                    text_hashes[j] = (d * (text_hashes[j] - ord(text[i]) * pow(d, m - 1, p)) + ord(text[i + m])) % p

    return (apparition, count), faux_positif
