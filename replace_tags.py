"""
replace_tags.py
Created by Jacob Dirkx for LCRADS @ UO
Last updated 01/28/25
Replaces tags enclosed by ** with random dates, numbers, or items from csvs
"""

import os
import random
import re
from datetime import datetime, timedelta
import pandas as pd

DIR = r"C:\Users\jacob\OneDrive\Desktop\LCRADS\Carla_Dis\All_Samples"  # Change for your directory structure
OUTPUT_DIR = "All_samples_tags_replaced"
PATTERN = r'(\*.*?\*|[\w]+|[^\w\s])'

def random_date(start_date, end_date):
	start = datetime.strptime(start_date, "%d-%m-%Y")
	end = datetime.strptime(end_date, "%d-%m-%Y")
	return start + timedelta(days=random.randint(0, (end - start).days))

def random_excel(filepath):
	data = pd.read_csv(filepath, header=None)
	return random.choice(data[0])

def replace_tags(words):
	tag_files = {
		"*CITY*": "Cities.csv",
		"*FIRST_NAME*": "FirstNames.csv",
		"*LAST_NAME*": "LastNames.csv",
		"*NAME*": "FullNames.csv",
		"*PLACE*": "Places.csv",
		"*STATE*": "States.csv",
		"*UNIVERSITY*": "Universities.csv",
	}

	for index, word in enumerate(words):
		if word == "*AGE*":
			words[index] = str(random.randint(18, 70))
		elif word == "*BIRTH_DATE*":
			words[index] = random_date("01-01-1999", "01-01-2022").strftime("%m-%d-%Y")
		elif word == "*NUMBER*":
			words[index] = str(random.randint(2, 99))
		elif word in tag_files:
			filepath = os.path.join(DIR, tag_files[word])
			words[index] = str(random_excel(filepath))
	return words

def process_file(filepath, filename):
	output_path = os.path.join(OUTPUT_DIR, f"{filename}_TAGS_REPLACED.txt")
	with open(filepath, 'r', encoding='utf-8') as input_file, open(output_path, 'w', encoding='utf-8') as output_file:
		for line in input_file:
			words = re.findall(PATTERN, line)
			words = replace_tags(words)
			output_file.write(' '.join(words) + '\n')

def main():
	if not os.path.exists(DIR):
		raise FileNotFoundError(f"The directory '{DIR}' does not exist.")
	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)

	for filename in os.listdir(DIR):
		filepath = os.path.join(DIR, filename)
		if os.path.isfile(filepath) and filename.endswith('.txt'):
			process_file(filepath, filename)

if __name__ == "__main__":
	main()