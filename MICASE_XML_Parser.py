"""
MICASE XML file parsing scheme
Created by Jacob Dirkx for University of Oregon's LCR-ADS Lab
Last updated 6/8/24

- Iterates over XML files in 'XMLs' folder in current directory 
(as created by webscraper.py)
- Writes metadata and text content to txt files to new directory with original doc id as filename
- Data is in the following format:

# sp_status = NRN
# l1 = EST
# person_id = S1
# discipline = NA 
# text_type = ADV 
# original_doc = adv700ju023 
# utterance_id = 1
# sentence_id = TBD 
so. i see that you're from Hartland Michigan

# sp_status = NS
# l1 = English
# person_id = S2
# discipline = NA
# text_type = ADV
# original_doc = adv700ju023
# utterance_id = 2
# sentence_id = TBD
yes

Notes:

Script creates a new dir in the cwd to write text files

Some XML files [COL425MX075, SVC999MX104] are incomplete due to incorrect coding on the MICASE website,
so their parsed data is also incomplete and will generate parse errors
"""
import xml.etree.ElementTree as ET
import os

#Assumes XML files are contained within folder 'XMLs' in CWD
#As created by webscraper.py - adjust if necessary
DIR = 'XMLs'

def write(output_file, text, sp_status, l1, person_id, text_type, original_doc, utterance_id):
	"""Writes given metadata and text content to output_file"""
	if text:  
		output_file.write(f"# sp_status = {sp_status}\n")
		output_file.write(f"# l1 = {l1}\n")
		output_file.write(f"# person_id = {person_id}\n")
		output_file.write(f"# discipline = NA\n")
		output_file.write(f"# text_type = {text_type}\n")
		output_file.write(f"# original_doc = {original_doc}\n")
		output_file.write(f"# utterance_id = {utterance_id}\n")
		output_file.write(f"# sentence_id = TBD\n")
		output_file.write(f"{text}\n\n")

def process_utterance(utterance, output_file, text_type, original_doc, utterance_id, parent_tail=None):
	"""
	Processes utterance under a single U tag from XML file body

	Parameters:
	- utterance: element of XML body to be parsed
	- output_file: text file to write to 
	- text_type: type of text
	- original_doc: original document ID
	- utterance_id: utterance id incremented via iteration 
	- parent_tail: tail of the parent element, if any

	Returns:
	- utterance_id: utterance id incremented via iteration (returned primarily for recursion for nested elements)
	"""
	# Pulls metadata from U tag 
	person_id = utterance.attrib.get('WHO')
	sp_status = utterance.attrib.get('NSS')
	l1 = utterance.attrib.get('FLANG') if utterance.attrib.get('FLANG') is not None else 'English'
	
	# Writes text of utterance (content before additional nested elements), if any
	if utterance.text and utterance.text.strip():
		text = utterance.text.strip()
		write(output_file, text, sp_status, l1, person_id, text_type, original_doc, utterance_id)
		utterance_id += 1

	for child in list(utterance):
		# Recursive call for nested U tags, checks for parent text following nested U tags, if any
		if child.tag.startswith('U'):
			if child.tail and child.tail.strip():
				child_tail = child.tail.strip()
			else:
				child_tail = None
			if parent_tail:
				parent_tail_copy = parent_tail[:]
				parent_tail_copy.append(child_tail)
			else:
				parent_tail_copy = [output_file, child_tail, sp_status, l1, person_id, text_type, original_doc]
			utterance_id = process_utterance(child, output_file, text_type, original_doc, utterance_id, parent_tail_copy)

		# Writes text, tail for OVERLAP content, if any
		elif child.tag.startswith('OVERLAP') and child.text and child.text.strip():
			overlap_text = child.text.strip()
			if child.tail and child.tail.strip():
				overlap_text = overlap_text + ' ' + child.tail.strip()
			write(output_file, overlap_text, sp_status, l1, person_id, text_type, original_doc, utterance_id)
			utterance_id += 1

		# Skip processing text within FOREIGN tags
		elif child.tag == 'FOREIGN':
			pass
		
		#If text follows a nested tag, add entry attributed to parent speaker
		elif child.tail and child.tail.strip():
			tail_text = child.tail.strip()
			write(output_file, tail_text, sp_status, l1, person_id, text_type, original_doc, utterance_id)
			utterance_id += 1

	# Writes stored parent text following nested U tag, if any 
	if parent_tail and parent_tail[1] and len(parent_tail) == 7:
		parent_tail.append(utterance_id)
		write(*parent_tail)
		utterance_id += 1

	# Returns utterance_id for recursive call
	return utterance_id

def parseXML(xmlfile, filename, output_dir):
	"""Parses a single XML file by creating tree/root structure, pulling metadata, and iterating over XML body
	Parameters
	- xmlfile: opened XML file
	- filename: [XML text ID]_Parsed, to be used for text file containing data
	- output_dir: directory to save output files
	"""
	try:
		# Creates tree and root structure from XML
		tree = ET.parse(xmlfile)
		root = tree.getroot()

		# Creates new/write-over text file with [XML text ID]_Parsed as name (as created by webscraper.py)
		output_path = os.path.join(output_dir, f'{filename}_Parsed.txt')
		with open(output_path, 'w') as output_file:

			# Pulls metadata from XML header
			term_tag = root.find('.//TERM[@TYPE="SPEECHEVENT"]')
			text_type = term_tag.text if term_tag is not None and term_tag.text else 'NA'
			original_doc = root.attrib.get('ID')

			# Initializes utterance_id count, iterates through all U tags in XML Body to process them
			utterance_id = 1
			for utterance in root.findall('.//BODY/*'):
				if utterance.tag.startswith('U'):
					utterance_id = process_utterance(utterance, output_file, text_type, original_doc, utterance_id, None)

		print(f'Created text file: {output_path}')
	except ET.ParseError as e:
		print(f"Parse error in file {filename}: {e}")

def main():
    # Creates new dir, XML_Data, to write to if one does not exist
    output_dir = 'XML_Data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Iterates over XML files in provided directory
    for filename in os.listdir(DIR):
        f = os.path.join(DIR, filename)
        if os.path.isfile(f):
            parseXML(f, os.path.splitext(filename)[0], output_dir)
        else:
            print(f"Error: unable to open file {f}")
    print('Parsed text files created successfully')

if __name__ == '__main__':
    main()


def main():
	# Creates new dir, XML_Data, to write to if one does not exist
	if not os.path.exists('XMLs_Parsed'):
		os.makedirs('XMLs_Parsed')

	# Iterates over XML files in provided directory
	for filename in os.listdir(DIR):
		f = os.path.join(DIR, filename)
		if os.path.isfile(f):
			output_dir = 'XMLs_Parsed'
			parseXML(f, os.path.splitext(filename)[0], output_dir)
		else:
			print(f"Error: unable to open file {f}")
	print('Parsed text files created successfully')

if __name__ == '__main__':
	main()