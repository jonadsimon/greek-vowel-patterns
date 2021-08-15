from GreekPhonemeFrequencies import GreekPhonemeFrequencies
import time

if __name__ == '__main__':
    token_count_input_path = './data/token_counts.csv'
    unconditional_prob_output_path = './data/unconditional_lexeme_probs.csv'
    conditional_prob_output_path = './data/conditional_lexeme_probs.csv'

    start_time = time.time()
    phoneme_lexeme_probs = GreekPhonemeFrequencies(token_count_input_path)
    print('Finished loading token freqs ({:.1f}sec)'.format(time.time() - start_time))

    start_time = time.time()
    phoneme_lexeme_probs.CountUnconditionalLexemes()
    print('Finished computing unconditional freqs ({:.1f}sec)'.format(time.time() - start_time))

    start_time = time.time()
    phoneme_lexeme_probs.CountConditionalPrecedingLexemes()
    print('Finished computing conditional freqs ({:.1f}sec)'.format(time.time() - start_time))

    start_time = time.time()
    phoneme_lexeme_probs.WriteUnconditionalLexemeCountsToCSV(unconditional_prob_output_path)
    print('Finished writing unconditional probs ({:.1f}sec)'.format(time.time() - start_time))

    start_time = time.time()
    phoneme_lexeme_probs.WriteConditionalLexemeCountsToCSV(conditional_prob_output_path)
    print('Finished writing conditional probs ({:.1f}sec)'.format(time.time() - start_time))
