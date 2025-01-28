import os
import re

DIR = r"C:\Users\jacob\OneDrive\Desktop\LCRADS\Carla_Dis\All_Samples_tags_replaced" 


def process_file(filepath):
	pattern = r"\*(\w+)\*"
	with open(filepath, 'r', encoding='utf-8') as file:
		tags = re.findall(pattern, file.read())
		if tags:
			print(f"{tags} found in {filepath}")

def main():
	if not os.path.exists(DIR):
		raise FileNotFoundError(f"The directory '{DIR}' does not exist.")

	for filename in os.listdir(DIR):
		filepath = os.path.join(DIR, filename)
		if os.path.isfile(filepath) and filename.endswith('.txt'):
			process_file(filepath)


if __name__ == "__main__":
	main()