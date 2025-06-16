"""Data preprocess for GPQA
Data Link: https://huggingface.co/datasets/Idavidrein/gpqa
"""
import csv
import json
import random
from tqdm import tqdm

# Paths to data
split = 'diamond'  # diamond, main, extended
data_path = f'./GPQA/original_data/gpqa_{split}.csv'
output_path = f'./GPQA/{split}.json'

# Define the keys we want to keep
keys_to_keep = [
    'id',
    'Question',
    'Subdomain',
    'High-level domain',
    'Correct Answer',
    'Incorrect Answer 1',
    'Incorrect Answer 2',
    'Incorrect Answer 3'
]

filtered_data = []
with open(data_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for idx, row in enumerate(tqdm(csv_reader), 0):
        # Add id field
        row['id'] = idx
        # Create new dictionary with only desired keys
        filtered_row = {key: row[key] for key in keys_to_keep}

        # Extract answers and shuffle them
        answers = [
            ('Correct Answer', filtered_row['Correct Answer']),
            ('Incorrect Answer 1', filtered_row['Incorrect Answer 1']),
            ('Incorrect Answer 2', filtered_row['Incorrect Answer 2']),
            ('Incorrect Answer 3', filtered_row['Incorrect Answer 3'])
        ]
        random.shuffle(answers)

        # Assign new choices A, B, C, D in order and determine the correct choice
        choices = ['A', 'B', 'C', 'D']
        formatted_answers = []
        correct_choice = None
        for i, (label, answer) in enumerate(answers):
            choice = choices[i]
            formatted_answers.append((choice, answer))
            if label == 'Correct Answer':
                correct_choice = choice

        # Update the Question field
        formatted_choices = "\n".join([f"({choice}) {answer}" for choice, answer in formatted_answers])
        filtered_row['Question'] = f"{filtered_row['Question']} Choices:\n{formatted_choices}\n"

        # Add the Correct Choice field
        filtered_row['Correct Choice'] = correct_choice

        # Append the updated row to filtered_data
        filtered_data.append(filtered_row)

# Write the updated data to JSON
with open(output_path, mode='w', encoding='utf-8') as json_file:
    json.dump(filtered_data, json_file, indent=4, ensure_ascii=False)
