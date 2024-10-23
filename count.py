import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure that necessary NLTK data is downloaded
nltk.download('punkt')

# Paths to the folders
sw_removed_folder = 'SW_Removed'
master_dictionary_folder = 'MasterDictionary'
output_folder = 'counts'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load positive and negative words
positive_words = set()
negative_words = set()

# Load positive words
with open(os.path.join(master_dictionary_folder, 'positive-words.txt'), 'r', encoding='ISO-8859-1') as file:
    positive_words.update(file.read().splitlines())

# Load negative words
with open(os.path.join(master_dictionary_folder, 'negative-words.txt'), 'r', encoding='ISO-8859-1') as file:
    negative_words.update(file.read().splitlines())

# Function to count syllables in a word
def count_syllables(word):
    word = word.lower()
    vowels = "aeiouy"
    syllable_count = 0
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith("e"):
        syllable_count -= 1
    if syllable_count == 0:
        syllable_count += 1
    return syllable_count

# Function to count complex words (more than two syllables)
def count_complex_words(word_list):
    return sum(1 for word in word_list if count_syllables(word) > 2)


# Function to count personal pronouns
def count_personal_pronouns(word_list):
    pronouns = ["i", "we", "my", "ours", "us"]
    sum = 0
    for word in word_list:
        if word == "US":
            continue
        elif word.lower() in pronouns:
            sum += 1
    return sum

# Function to calculate average word length
def average_word_length(word_list):
    total_length = sum(len(word) for word in word_list)
    return total_length / len(word_list) if len(word_list) > 0 else 0

# Function to calculate average sentence length
def average_sentence_length(sentences, total_word_count):
    return total_word_count / len(sentences) if len(sentences) > 0 else 0

# Function to calculate FOG Index
def fog_index(avg_sentence_length, percentage_complex_words):
    return 0.4 * (avg_sentence_length + percentage_complex_words)

# Function to calculate average number of words per sentence
def avg_words_per_sentence(sentences, total_word_count):
    return total_word_count / len(sentences) if len(sentences) > 0 else 0

# Function to calculate syllables per word
def calculate_syllables_per_word(word_list):
    total_syllables = sum(count_syllables(word) for word in word_list)
    return total_syllables / len(word_list) if len(word_list) > 0 else 0

# Function to calculate scores and additional metrics
def calculate_scores(text, positive_words, negative_words):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    total_word_count = len(words)
    total_sentence_count = len(sentences)
    
    positive_count = sum(1 for word in words if word.lower() in positive_words)
    negative_count = sum(-1 for word in words if word.lower() in negative_words)  # Negative count is negative

    complex_word_count = count_complex_words(words)
    percentage_complex_words = (complex_word_count / total_word_count) * 100 if total_word_count > 0 else 0

    personal_pronouns_count = count_personal_pronouns(words)
    avg_word_length = average_word_length(words)
    avg_sentence_length = average_sentence_length(sentences, total_word_count)
    avg_words_per_sentence_value = avg_words_per_sentence(sentences, total_word_count)
    syllables_per_word_value = calculate_syllables_per_word(words)
    fog_index_value = fog_index(avg_sentence_length, percentage_complex_words)

    # Calculate scores
    positive_score = positive_count
    negative_score = -negative_count
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (total_word_count + 0.000001)

    return (positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length, 
            percentage_complex_words, fog_index_value, avg_words_per_sentence_value, complex_word_count, 
            total_word_count, syllables_per_word_value, personal_pronouns_count, avg_word_length)

# Loop through each file in the SW_Removed folder
for filename in os.listdir(sw_removed_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(sw_removed_folder, filename)

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Calculate scores and additional metrics
        (positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length, 
         percentage_complex_words, fog_index_value, avg_words_per_sentence_value, complex_word_count, 
         total_word_count, syllables_per_word_value, personal_pronouns_count, avg_word_length) = calculate_scores(content, positive_words, negative_words)

        # Save the results to the count folder
        output_file_path = os.path.join(output_folder, f'{filename}')
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(f'Positive Score: {positive_score}\n')
            file.write(f'Negative Score: {negative_score}\n')
            file.write(f'Polarity Score: {polarity_score:.6f}\n')
            file.write(f'Subjectivity Score: {subjectivity_score:.6f}\n')
            file.write(f'Average Sentence Length: {avg_sentence_length:.2f}\n')
            file.write(f'Percentage of Complex Words: {percentage_complex_words:.2f}%\n')
            file.write(f'FOG Index: {fog_index_value:.2f}\n')
            file.write(f'Average Number of Words Per Sentence: {avg_words_per_sentence_value:.2f}\n')
            file.write(f'Complex Word Count: {complex_word_count}\n')
            file.write(f'Word Count: {total_word_count}\n')
            file.write(f'Syllable Per Word: {syllables_per_word_value:.2f}\n')
            file.write(f'Personal Pronouns Count: {personal_pronouns_count}\n')
            file.write(f'Average Word Length: {avg_word_length:.2f}\n')

        print(f"Scores for {filename} saved to {output_file_path}")

print("All files processed and scores saved.")
