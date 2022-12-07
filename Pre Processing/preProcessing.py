import string
import pandas as pd

# Data pre-processing:
# Import the db file as a csv file
# Use pandas to read the csv file
# Process: Take one column at a time from the table,  do pre-processing

# Reading csv file using pandas
df = pd.read_csv("E:\Apps\Sqlite\DB Browser\Databases\preProcessedTable.csv") # This is the location of the csv file of the dataset

# Drop the rows in the table where at least one element is missing:
df.dropna(axis=0,how='any',subset=None,inplace=True)

# Converting all the letters in 'related lesson' column to lowercase
df['Related Lesson'] = df["Related Lesson"].str.lower()

# Print the csv table
# print(df.head(30))

# Function to remove punctuations
def remove_punctuations(text):
    punctuations = string.punctuation
    return text.translate(str.maketrans('','', punctuations))

# Removing punctuations in 'related lesson' column
df['Related Lesson'] = df["Related Lesson"].apply(lambda x: remove_punctuations(x))

#Removing extra white spaces:
def remove_whitespace(text):
    return  " ".join(text.split())

# Removing extra white spaces in 'related lessons' columns
df['Related Lesson'] = df['Related Lesson'].apply(lambda x: remove_whitespace(x))

#Spelling corrections
from spellchecker import SpellChecker
spell = SpellChecker()

def correct_spelling(text):
    corrected_text = []
    misspelled_text = spell.unknown(text.split())

    # This is to find out the words written incorrectly
    # print(misspelled_text)

    for word in text.split():
        if word in misspelled_text:
            corrected_text.append(spell.correction(word))
        else:
            corrected_text.append(word)

    return " ".join(filter(None,corrected_text)) # Filtered none values from the corrected_text list using filter

# Spelling correction in 'related lesson' column
df['Related Lesson'] = df['Related Lesson'].apply(lambda x: correct_spelling(x))

# # Spelling correction in 'Question' column
# df['Question'] = df["Question"].apply(lambda x: correct_spelling(x))

# # Spelling correction in 'Correct Answer' column
# df['Correct Answer'] = df['Correct Answer'].apply(lambda x: correct_spelling(x))
#
# # Spelling correction in 'Incorrect Answer 1' column
# df['Incorrect Answer 1'] = df['Incorrect Answer 1'].apply(lambda x: correct_spelling(x))
#
# # Spelling correction in 'Incorrect Answer 2' column
# df['Incorrect Answer 2'] = df['Incorrect Answer 2'].apply(lambda x: correct_spelling(x))
#
# # Spelling correction in 'Incorrect Answer 3' column
# df['Incorrect Answer 3'] = df['Incorrect Answer 3'].apply(lambda x: correct_spelling(x))
#
# # Spelling correction in 'Incorrect Answer 4' column
# df['Incorrect Answer 4'] = df['Incorrect Answer 4'].apply(lambda x: correct_spelling(x))

# Saving the data after all the operations
df.to_csv("E:\Apps\Sqlite\DB Browser\Databases\preProcessedTable.csv",encoding='utf-8',index=False)

# Shuffle and print the csv table
print(df.sample(frac=1).head())