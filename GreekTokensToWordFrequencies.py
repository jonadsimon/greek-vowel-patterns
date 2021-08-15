from collections import Counter

class GreekTokensToWordFrequencies:
    def __init__(self, raw_tokens_file):
        with open(raw_tokens_file) as infile:
            self.raw_tokens = [token for token in infile.read().split()]

        # Manually identified acronyms and other non-linguistic contructs (lowercased).
        self.token_blacklist = set(['βλ', 'κ', 'κα', 'εε', 'εοκ', 'αριθ', 'δνο'])
        self.english_chars = set('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ')
        self.punctuation_chars = set('!"#$%&\'()*+,-./:;<=>?@[\]^_`{¦}~«»ʼ·–')
        self.emphasis_mapping = {'ΐ': 'ϊ', 'ΰ': 'ϋ', 'ά': 'α', 'έ': 'ε', 'ή': 'η',
                                'ί': 'ι', 'ό': 'ο', 'ύ': 'υ', 'ώ': 'ω'}

    def TokenInBlacklist(self, token):
        return token in self.token_blacklist

    def TokenContainsNumber(self, token):
        return any([c.isdigit() for c in token])

    def TokenContainsEnglish(self, token):
        return any([c in self.english_chars for c in token])

    def TokenContainsPunctuation(self, token):
        return any([c in self.punctuation_chars for c in token])

    def DowncaseToken(self, token):
        return token.lower()

    def RemoveEmphases(self, token):
        return ''.join([self.emphasis_mapping[c] if c in self.emphasis_mapping else c for c in token])

    def FilterTokens(self):
        self.filtered_tokens = []
        for token in self.raw_tokens:
            if self.TokenInBlacklist(token) or self.TokenContainsNumber(token) or self.TokenContainsEnglish(token) or self.TokenContainsPunctuation(token):
                continue
            cleaned_token = self.DowncaseToken(token)
            cleaned_token = self.RemoveEmphases(cleaned_token)
            self.filtered_tokens.append(cleaned_token)

    def CountTokens(self):
        self.token_counts = Counter(self.filtered_tokens)

    def WriteTokenCountsToCSV(self, path):
        with open(path, 'w') as outfile:
            for token, cnt in self.token_counts.most_common():
                outfile.write(f'{token},{cnt}\n')
