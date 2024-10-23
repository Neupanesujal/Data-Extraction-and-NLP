import os

# Paths to the folders
scraped_data_folder = 'scraped_data'  # Replace with your actual path if different
stopwords_folder = 'StopWords'        # Replace with your actual path if different
output_folder = 'SW_Removed'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load all stopwords from the StopWords folder
stopwords = set()

for filename in os.listdir(stopwords_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(stopwords_folder, filename)
        with open(file_path, 'r', encoding='ISO-8859-1') as file:  # Using ISO-8859-1 encoding
            words = file.read().splitlines()
            stopwords.update(words)

# Function to remove stopwords from a text and track removed words
def remove_stopwords(text, stopwords):
    words = text.split()
    removed_words = [word for word in words if word.lower() in stopwords]
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return ' '.join(filtered_words), removed_words

# Loop through each file in the scraped_data folder
for filename in os.listdir(scraped_data_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(scraped_data_folder, filename)

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove stopwords from the content and capture removed words
        cleaned_content, removed_words = remove_stopwords(content, stopwords)

        # Save the cleaned content to the SW_Removed folder
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

        # Print the removed words for this file
        print(f"Stopwords removed from {filename}: {', '.join(removed_words)}")

        print(f"Content saved to {output_path}")
