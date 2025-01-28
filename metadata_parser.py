"""
metadata_parser.py
Created by Jacob Dirkx for LCRADS @ UO
Last updated 01/28/25
Parses metadata folders, extracts content to CSV
"""
import csv
import os

DIR = r"C:\Users\jacob\OneDrive\Desktop\LCRADS\Carla_Dis\Metadata" #change for own directory
FOLDERS = ["Metadata_01_famous", "Metadata_02_vacation", "Metadata_03_terrible", "Metadata_04_beautiful"]
OUTPUT_FILE = "Metadata_Parsed.csv"
SEX = ["Female", "Male", "I do not identify with either genders"]

def write_to_csv(file_name, **kwargs):

	try:
		with open(file_name, 'r') as f:
			has_header = f.readline() != ''
	except FileNotFoundError:
		has_header = False
	with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=kwargs.keys())
		if not has_header:
			writer.writeheader()
		writer.writerow(kwargs)

def extract_content(filepath, filename):

	with open(filepath, 'r', encoding='utf-8') as file:
		line = file.readline()
		items = line.split("|||")
		metadata = items[:3] + [" "] * (3 - len(items))
		if metadata[1] in SEX:
			metadata[1], metadata[2] = metadata[2], metadata[1]
		write_to_csv(OUTPUT_FILE, 
			filename=filename,
			level=metadata[0],
			age=metadata[1],
			sex=metadata[2]
			)

def main():
	if not os.path.exists(DIR):
		raise FileNotFoundError(f"The directory '{DIR}' does not exist.")
	for folder in FOLDERS:
		dir = os.path.join(DIR, folder)
		for filename in os.listdir(dir):
			filepath = os.path.join(dir, filename)
			if os.path.isfile(filepath) and filename.endswith('.txt'):
				extract_content(filepath, os.path.splitext(filename)[0])

if __name__ == "__main__":
	main()