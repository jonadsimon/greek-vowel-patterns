class GreekTokensToWordFrequencies:
    def __init__(self, raw_tokens_file):
        with open(raw_tokens_file) as infile:
            self.raw_tokens = [token for token in infile.read().split()]

        # Manually identified acronyms and other non-linguistic contructs (lowercased).
        self.token_blacklist = ['βλ', 'κ', 'κα', 'εε', 'εοκ', 'αριθ', 'δνο']

    def TokenContainsNumber(self, token):
        return any([c.isdigit() for c in token])

    def TokenContainsEnglish(self, token):
        english_chars = set('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ')
        return any([c in english_chars for c in token])

    def TokenContainsPunctuation(self, token):
        punctuation_chars = set('!"#$%&\'()*+,-./:;<=>?@[\]^_`{¦}~«»')
        return any([c in punctuation_chars for c in token])

    def DowncaseToken(self, token):
        return token.downcase()

    def RemoveEmphases(self, token):
        emphasis_mapping = {'ΐ': 'ϊ', 'ΰ': 'ϋ', 'ά': 'α', 'έ': 'ε', 'ή': 'η',
                            'ί': 'ι', 'ό': 'ο', 'ύ': 'υ', 'ώ': 'ω'}
        return ''.join([emphasis_mapping[c] if c in emphasis_mapping else c for c in token])
