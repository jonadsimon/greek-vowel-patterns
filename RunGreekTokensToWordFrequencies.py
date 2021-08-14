from GreekTokensToWordFrequencies import GreekTokensToWordFrequencies
import time

if __name__ == '__main__':
    raw_token_input_path = './data/el.tok'
    token_count_output_path = './data/token_counts.csv'

    start_time = time.time()
    token_to_word_freqs = GreekTokensToWordFrequencies(raw_token_input_path)
    print('Finished loading tokens ({:.1f}sec)'.format(time.time() - start_time))

    start_time = time.time()
    token_to_word_freqs.FilterTokens()
    print('Finished filtering tokens ({:.1f}sec)'.format(time.time() - start_time))

    start_time = time.time()
    token_to_word_freqs.CountTokens()
    print('Finished counting tokens ({:.1f}sec)'.format(time.time() - start_time))

    start_time = time.time()
    token_to_word_freqs.WriteTokenCountsToCSV(token_count_output_path)
    print('Finished writing tokens ({:.1f}sec)'.format(time.time() - start_time))
