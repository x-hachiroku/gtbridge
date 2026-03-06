class TrieNode:
    def __init__(self):
        self.children = {}
        self.match = None

class Replacer:
    def __init__(self, mappings: dict[str, str]):
        self.root = TrieNode()
        for src, dst in mappings.items():
            node = self.root
            for char in src:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.match = dst

    def replace(self, text: str) -> str:
        result = []
        i = 0
        n = len(text)

        while i < n:
            node = self.root
            longest_match_len = 0
            longest_match_dst = None

            # Look ahead to find the longest matching substring in the trie
            j = i
            while j < n and text[j] in node.children:
                node = node.children[text[j]]
                if node.match is not None:
                    longest_match_len = j - i + 1
                    longest_match_dst = node.match
                j += 1

            if longest_match_len > 0:
                result.append(longest_match_dst)
                i += longest_match_len
            else:
                result.append(text[i])
                i += 1

        return "".join(result)
