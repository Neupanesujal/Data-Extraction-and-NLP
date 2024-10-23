import os
import pandas as pd

# Paths
count_folder = '/home/sujal-neupane/drives/HDD/part1/BlackCoffer/counts'
excel_file_path = '/home/sujal-neupane/drives/HDD/part1/BlackCoffer/Output Data Structure.xlsx'

# Load the Excel file
df = pd.read_excel(excel_file_path)

# Function to extract the scores from the count files
def extract_scores(file_path):
    scores = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if ':' in line:
                key, value = line.split(":", 1)
                scores[key.strip()] = value.strip()
    return scores

# Iterate through the count files and update the Excel file
for filename in os.listdir(count_folder):
    if filename.endswith('.txt'):
        # Extract the URL_ID from the filename
        url_id = filename.replace('.txt', '')
        
        # Match the URL_ID with the Excel file
        if url_id in df['URL_ID'].values:
            file_path = os.path.join(count_folder, filename)
            scores = extract_scores(file_path)
            
            # Update the respective columns in the DataFrame
            df.loc[df['URL_ID'] == url_id, 'POSITIVE SCORE'] = scores.get('Positive Score', 0)
            df.loc[df['URL_ID'] == url_id, 'NEGATIVE SCORE'] = scores.get('Negative Score', 0)
            df.loc[df['URL_ID'] == url_id, 'POLARITY SCORE'] = scores.get('Polarity Score', 0)
            df.loc[df['URL_ID'] == url_id, 'SUBJECTIVITY SCORE'] = scores.get('Subjectivity Score', 0)
            df.loc[df['URL_ID'] == url_id, 'AVG SENTENCE LENGTH'] = scores.get('Average Sentence Length', 0)
            df.loc[df['URL_ID'] == url_id, 'PERCENTAGE OF COMPLEX WORDS'] = scores.get('Percentage of Complex Words', 0)
            df.loc[df['URL_ID'] == url_id, 'FOG INDEX'] = scores.get('FOG Index', 0)
            df.loc[df['URL_ID'] == url_id, 'AVG NUMBER OF WORDS PER SENTENCE'] = scores.get('Average Number of Words Per Sentence', 0)
            df.loc[df['URL_ID'] == url_id, 'COMPLEX WORD COUNT'] = scores.get('Complex Word Count', 0)
            df.loc[df['URL_ID'] == url_id, 'WORD COUNT'] = scores.get('Word Count', 0)
            df.loc[df['URL_ID'] == url_id, 'SYLLABLE PER WORD'] = scores.get('Syllable Per Word', 0)
            df.loc[df['URL_ID'] == url_id, 'PERSONAL PRONOUNS'] = scores.get('Personal Pronouns Count', 0)
            df.loc[df['URL_ID'] == url_id, 'AVG WORD LENGTH'] = scores.get('Average Word Length', 0)

# Save the updated DataFrame back to the Excel file
df.to_excel(excel_file_path, index=False)

print("Excel file updated successfully!")
