import syllables 
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import re
from bs4 import BeautifulSoup
import os
import pandas as pd
import requests

df= pd.read_csv("Input.csv")
df=df.dropna()



def link_to_text(url):
    r = requests.get(url)
   
    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    extracted_text = ""
    
    paragraphs = soup.find_all('p')
    extracted_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
    return extracted_text




folder_path = r"D:\Python\WS\StopWords"

# Get a list of all files in the folder
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]



for stop_words_file in file_paths:  
    with open(stop_words_file, "r") as stop_words_file:
        
        lines = stop_words_file.readlines()
        stop_words = [line.split('|')[0].strip() for line in lines]
        # Remove the characters after "|" in each line
    


with open("negative-words.txt", "r") as stop_words_file:
     
        lines = stop_words_file.readlines()
        negative_words = [line.split('|')[0].strip() for line in lines]

with open("positive-words.txt", "r") as stop_words_file:
        
        lines = stop_words_file.readlines()
        positive_words = [line.split('|')[0].strip() for line in lines]



#"""
def sentimental_analysis(text):
    # Cleaning using Stop Words Lists
    tokens = word_tokenize(text.lower())
    cleaned_text = [word for word in tokens if word.isalpha() and word not in stop_words]
    

    
    positive_score = sum(1 for word in cleaned_text if word in positive_words)
    negative_score = sum(1 for word in cleaned_text if word in negative_words)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_text) + 0.000001)


    # Average Sentence Length
    sentences = sent_tokenize(text)
    avg_sentence_length = len(cleaned_text) / len(sentences)

    # Percentage of Complex Words
    complex_words = [word for word in cleaned_text if syllables.estimate(word) > 2]
    percentage_complex_words = len(complex_words) / len(cleaned_text)

    # Fog Index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Average Number of Words Per Sentence
    avg_words_per_sentence = len(cleaned_text) / len(sentences)

    # Complex Word Count
    complex_word_count = len(complex_words)

    # Word Count
    total_word_count = len(cleaned_text)

    # Syllables Per Word
    syllables_per_word = sum(len(re.findall(r'[aeiouy]+', word)) for word in cleaned_text) / total_word_count

    # Personal Pronouns
    personal_pronouns = sum(1 for word in cleaned_text if word.lower() in {"i", "we", "my", "ours", "us"})

    # Average Word Length
    avg_word_length = sum(len(word) for word in cleaned_text) / total_word_count
    
    return positive_score, negative_score, polarity_score, subjectivity_score, \
           avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, \
           complex_word_count, total_word_count, syllables_per_word, personal_pronouns, avg_word_length
    
    



def link_to_output(link):
     text= link_to_text(link)
     results = sentimental_analysis(text)
     return results

df[["positive_score", "negative_score", "polarity_score", "subjectivity_score", \
           "avg_sentence_length", "percentage_complex_words", "fog_index", "avg_words_per_sentence", \
            "complex_word_count", "total_word_count", "syllables_per_word", "personal_pronouns", "avg_word_length"]] = df['URL'].apply(link_to_output).apply(pd.Series)




df.to_excel('output_1.xlsx', index=False)

print("DataFrame saved to 'output_1.xlsx'")


