from collections import Counter, defaultdict
from helper_utils import find_all, rec_dd

class GreekPhonemeFrequencies:
    '''
    Assume that a full list of words in the Greek language have already been parsed and stored in a list.
    This list is the 'vocab' input to the initializer.

    If no such list can be found a priori, a separate helper class can be used to construct it.

    (Question: Should emphases be stripped when constructing the dictionary? Leaning towards yes.)

    Desired result: Function providing P(letter|sound) for each occurrence of 'sound' across all words
    Note: A given word can contain multiple instances of a given sound, possibly with different spellings
    Therefore: Need to keep track of numerators and demoninators, i.e. for each word how many of each sounds does it contain, and how were each of them spelled
    '''
    def __init__(self, token_freq_csv):
        self.token_freq_counter = Counter()
        with open(token_freq_csv) as infile:
            for line in infile:
                token, cnt = line.split(',')
                self.token_freq_counter[token] = int(cnt)

        # Need to count two-letter vowels first, otherise will risk
        # misinterpreting parts of two-letter vowels as one-letter vowels.

        self.bigram_lexemes = ['ει', 'οι', 'υι', 'αι']
        self.unigram_lexemes = ['ι', 'η', 'υ', 'ε', 'ο', 'ω']
        self.other_diphthongs = ['αυ', 'ευ', 'ου']

        # For following/preceding logic to work, need to substitute a bigram with a unique
        # stand-in character that can be reverse-mapped back to it without the risk of unigram
        # collisions. Also need to keep track of the two other standard diphthongs because
        # they, like the two-letter vowels, are "their own kind of letter"

        self.bigram_to_placeholder_map = {'ει': '1', 'οι': '2', 'υι': '3', 'αι': '4', 'αυ': '5', 'ευ': '6', 'ου': '7'}
        self.placeholder_to_bigram_map = {'1': 'ει', '2': 'οι', '3': 'υι', '4': 'αι', '5': 'αυ', '6': 'ευ', '7': 'ου'}

        self.phonemes_to_lexemes = {'ee': ['ι', 'η', 'υ', 'ει', 'οι', 'υι'],
                                    'eh': ['ε', 'αι'], 'oh': ['ο', 'ω']}


    def CountUnconditionalLexemes(self):
        self.unweighted_lexeme_counter = Counter()
        self.weighted_lexeme_counter = Counter()
        for token, freq in self.token_freq_counter.items():
            mangled_token = token
            for lexeme in self.bigram_lexemes:
                num_found = mangled_token.count(lexeme)
                if num_found > 0: # not strictly necessary, if zero then logic is null-op
                    self.unweighted_lexeme_counter[lexeme] += num_found
                    self.weighted_lexeme_counter[lexeme] += num_found * freq
                    # need to replace the bigram lexems to avoid overcounting
                    mangled_token = mangled_token.replace(lexeme, '')
            for lexeme in self.unigram_lexemes:
                num_found = mangled_token.count(lexeme)
                if num_found > 0: # not strictly necessary, if zero then logic is null-op
                    self.unweighted_lexeme_counter[lexeme] += num_found
                    self.weighted_lexeme_counter[lexeme] += num_found * freq


    def CountConditionalPrecedingLexemes(self):
        self.unweighted_preceding_lexeme_counter = defaultdict(Counter)
        self.weighted_preceding_lexeme_counter = defaultdict(Counter)

        for token, freq in self.token_freq_counter.items():
            # Add a dedicated start character
            mangled_token = '^' + token
            # Need to replace 'other_diphthongs' FIRST so that the 'ου'
            # overrides the less-common 'υι' in the case of overlaps.
            for lexeme in self.other_diphthongs + self.bigram_lexemes:
                mangled_token = mangled_token.replace(lexeme, self.bigram_to_placeholder_map[lexeme])

            for lexeme in self.bigram_lexemes:
                for idx in find_all(mangled_token, self.bigram_to_placeholder_map[lexeme]):
                    if mangled_token[idx-1] in self.placeholder_to_bigram_map:
                        self.unweighted_preceding_lexeme_counter[self.placeholder_to_bigram_map[mangled_token[idx-1]]][lexeme] += 1
                        self.weighted_preceding_lexeme_counter[self.placeholder_to_bigram_map[mangled_token[idx-1]]][lexeme] += freq
                    else:
                        self.unweighted_preceding_lexeme_counter[mangled_token[idx-1]][lexeme] += 1
                        self.weighted_preceding_lexeme_counter[mangled_token[idx-1]][lexeme] += freq

            for lexeme in self.unigram_lexemes:
                for idx in find_all(mangled_token, lexeme):
                    if mangled_token[idx-1] in self.placeholder_to_bigram_map:
                        self.unweighted_preceding_lexeme_counter[self.placeholder_to_bigram_map[mangled_token[idx-1]]][lexeme] += 1
                        self.weighted_preceding_lexeme_counter[self.placeholder_to_bigram_map[mangled_token[idx-1]]][lexeme] += freq
                    else:
                        self.unweighted_preceding_lexeme_counter[mangled_token[idx-1]][lexeme] += 1
                        self.weighted_preceding_lexeme_counter[mangled_token[idx-1]][lexeme] += freq


    def WriteUnconditionalLexemeCountsToCSV(self, path):
        '''
        Need to first reprocess counters into a form where
        1) the weighted and unweighted counts can be merged & shown together
        2) the probabilities can be computed

        TODO: simplify the preceding logic to make this step trivial

        dict[phoneme][lexeme]['unweighted'/'weighted']['freq'/'prob'] = x
        defaultdict(defaultdict(defaultdict(defaultdict(int))))
        '''

        # lexeme_prob_dict = defaultdict(defaultdict(defaultdict(defaultdict(float))))
        lexeme_prob_dict = rec_dd()

        # Populate dicts with appropriately structured phonemes/lexemes/freqs
        for phoneme in self.phonemes_to_lexemes:
            for lexeme in self.phonemes_to_lexemes[phoneme]:
                lexeme_prob_dict[phoneme][lexeme]['unweighted']['freq'] = self.unweighted_lexeme_counter[lexeme]
                lexeme_prob_dict[phoneme][lexeme]['weighted']['freq'] = self.weighted_lexeme_counter[lexeme]

        # Compute freq totals and divide to get probabilities
        for phoneme in self.phonemes_to_lexemes:
            total_unweighted_freq = 0
            total_weighted_freq = 0
            for lexeme in self.phonemes_to_lexemes[phoneme]:
                total_unweighted_freq += lexeme_prob_dict[phoneme][lexeme]['unweighted']['freq']
                total_weighted_freq += lexeme_prob_dict[phoneme][lexeme]['weighted']['freq']
            for lexeme in self.phonemes_to_lexemes[phoneme]:
                lexeme_prob_dict[phoneme][lexeme]['unweighted']['prob'] = lexeme_prob_dict[phoneme][lexeme]['unweighted']['freq'] / total_unweighted_freq
                lexeme_prob_dict[phoneme][lexeme]['weighted']['prob'] = lexeme_prob_dict[phoneme][lexeme]['weighted']['freq'] / total_weighted_freq

        with open(path, 'w') as outfile:
            outfile.write(f'phoneme,lexeme,freq_unweighted,prob_unweighted,freq_weighted,prob_weighted\n')
            for phoneme in lexeme_prob_dict:
                for lexeme in lexeme_prob_dict[phoneme]:
                    sub_dict = lexeme_prob_dict[phoneme][lexeme]
                    outfile.write(f'{phoneme},{lexeme},{sub_dict["unweighted"]["freq"]},{sub_dict["unweighted"]["prob"]},{sub_dict["weighted"]["freq"]},{sub_dict["weighted"]["prob"]}\n')


    def WriteConditionalLexemeCountsToCSV(self, path):
        '''
        Need to first reprocess counters into a form where
        1) the weighted and unweighted counts can be merged & shown together
        2) the probabilities can be computed

        TODO: simplify the preceding logic to make this step trivial

        dict[phoneme][prev_lexeme][lexeme]['unweighted'/'weighted']['freq'/'prob'] = x
        defaultdict(defaultdict(defaultdict(defaultdict(int))))
        '''

        # lexeme_cond_prob_dict = defaultdict(defaultdict(defaultdict(defaultdict(defaultdict(float)))))
        lexeme_cond_prob_dict = rec_dd()

        # Populate dicts with appropriately structured phonemes/lexemes/freqs
        for phoneme in self.phonemes_to_lexemes:
            for prev_lexeme in self.unweighted_preceding_lexeme_counter:
                for lexeme in self.phonemes_to_lexemes[phoneme]:
                    lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['unweighted']['freq'] = self.unweighted_preceding_lexeme_counter[prev_lexeme][lexeme]
                    lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['weighted']['freq'] = self.weighted_preceding_lexeme_counter[prev_lexeme][lexeme]

        # Compute freq totals and divide to get probabilities
        for phoneme in self.phonemes_to_lexemes:
            for prev_lexeme in self.unweighted_preceding_lexeme_counter:
                total_unweighted_freq = 0
                total_weighted_freq = 0
                for lexeme in self.phonemes_to_lexemes[phoneme]:
                    # some of these may crash due to key not found errors
                    total_unweighted_freq += lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['unweighted']['freq']
                    total_weighted_freq += lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['weighted']['freq']
                for lexeme in self.phonemes_to_lexemes[phoneme]:
                    if total_unweighted_freq > 0:
                        lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['unweighted']['prob'] = lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['unweighted']['freq'] / total_unweighted_freq
                    else:
                        lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['unweighted']['prob'] = 'NaN'
                    if total_weighted_freq > 0:
                        lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['weighted']['prob'] = lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['weighted']['freq'] / total_weighted_freq
                    else:
                        lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]['weighted']['prob'] = 'NaN'

        with open(path, 'w') as outfile:
            outfile.write(f'phoneme,prev_lexeme,lexeme,freq_unweighted,prob_unweighted,freq_weighted,prob_weighted\n')
            for phoneme in lexeme_cond_prob_dict:
                for prev_lexeme in lexeme_cond_prob_dict[phoneme]:
                    for lexeme in lexeme_cond_prob_dict[phoneme][prev_lexeme]:
                        sub_dict = lexeme_cond_prob_dict[phoneme][prev_lexeme][lexeme]
                        outfile.write(f'{phoneme},{prev_lexeme},{lexeme},{sub_dict["unweighted"]["freq"]},{sub_dict["unweighted"]["prob"]},{sub_dict["weighted"]["freq"]},{sub_dict["weighted"]["prob"]}\n')
