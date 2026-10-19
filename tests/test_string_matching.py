import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from string_matching.aho_corasick import AhoCorasick
from string_matching.boyer_moore import boyer_moore
from string_matching.rabin_karp import rabin_karp_single_hash


def naive(text, pattern):
    """All (possibly overlapping) start positions of pattern in text."""
    return [i for i in range(len(text) - len(pattern) + 1) if text.startswith(pattern, i)]


class StringMatchingTests(unittest.TestCase):
    def setUp(self):
        random.seed(0)

    def random_case(self, n, m, alphabet="ACGT"):
        text = "".join(random.choice(alphabet) for _ in range(n))
        pattern = "".join(random.choice(alphabet) for _ in range(m))
        return text, pattern

    def test_boyer_moore_matches_naive(self):
        for _ in range(200):
            text, pattern = self.random_case(random.randint(1, 200), random.randint(1, 6))
            self.assertEqual(boyer_moore(text, pattern)[0], naive(text, pattern))

    def test_rabin_karp_matches_naive(self):
        for _ in range(200):
            text, pattern = self.random_case(random.randint(1, 200), random.randint(1, 6))
            (occ, _count), _fp = rabin_karp_single_hash(text, pattern)
            self.assertEqual(occ, naive(text, pattern))

    def test_aho_corasick_single_pattern(self):
        for _ in range(200):
            text, pattern = self.random_case(random.randint(1, 200), random.randint(1, 6))
            ac = AhoCorasick()
            ac.ajouter(pattern)
            ac.echecs()
            found, _ = ac.recherche(text)
            self.assertEqual([pos for pos, _ in found], naive(text, pattern))

    def test_aho_corasick_multiple_patterns_same_length(self):
        for _ in range(100):
            text = "".join(random.choice("ACGT") for _ in range(150))
            patterns = list({"".join(random.choice("ACGT") for _ in range(4)) for _ in range(5)})
            ac = AhoCorasick()
            for p in patterns:
                ac.ajouter(p)
            ac.echecs()
            found, _ = ac.recherche(text)
            expected = sorted((i, p) for p in patterns for i in naive(text, p))
            self.assertEqual(sorted(found), expected)


if __name__ == "__main__":
    unittest.main()
