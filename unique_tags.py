"""
unique_tags.py
Created by Jacob Dirkx for LCRADS @ UO
Last updated 01/11/25
Iterates through txt files in cwd to pull
unique tags enclosed by **
"""
import os
import re
import numpy as np

DIR = r"C:\Users\jacob\OneDrive\Desktop\LCRADS\Carla_Dis\All_Samples" #change to fir your directory structure
OUTPUT_FILE = 'ALL_SAMPLES_TAGS.txt'

def process_file(filepath):
	tags = []
	pattern = r"\*(\w+)\*"
	with open(filepath, 'r', encoding='utf-8') as file:
		tags.extend(re.findall(pattern, file.read()))
	return tags

def main():
	if not os.path.exists(DIR):
		raise FileNotFoundError(f"The directory '{DIR}' does not exist.")

	all_tags = []
	for filename in os.listdir(DIR):
		filepath = os.path.join(DIR, filename)
		if os.path.isfile(filepath) and filename.endswith('.txt'):
			all_tags.extend(process_file(filepath))
    

	all_tags = np.unique(all_tags)

	if os.path.exists(OUTPUT_FILE):
		os.remove(OUTPUT_FILE)

	with open(OUTPUT_FILE, 'w', encoding='utf-8') as output_file:
		for tag in all_tags:
			output_file.write(tag + '\n') 

if __name__ == "__main__":
	main()