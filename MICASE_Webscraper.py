"""
MICASE xml file download scheme
Created by Jacob Dirkx for University of Oregon's LCR-ADS Lab
Last updated 5/5/24

Notes:

Xml transcript download links are not actually download links, but rather transcript links
As such the script currently just iterates over them and writes them into new xml links

Script creates a new dir in the cwd to write xml files into

Takes several minutes to complete due to inclusion of pause in iteration over transcript links 
to not spook the server

"""
from bs4 import BeautifulSoup
import requests
import os
import time

MAIN_URL = "https://quod.lib.umich.edu/cgi/c/corpus/corpus?c=micase&cc=micase&type=browse"

def download_xml(url, filename) -> 'writes page contents to new xml file':
    response = requests.get(url)
    with open(os.path.join('XMLs', filename), 'wb') as f:
        f.write(response.content)

try:
#make dir for xml downloads in cwd
    if not os.path.exists('XMLs'):
        os.makedirs('XMLs')
#get main page soup
    main_response = requests.get(MAIN_URL)
    main_soup = BeautifulSoup(main_response.text, 'html.parser')
#iterate over links on main page, add them to list
    transcript_links = []
    for link in main_soup.find_all('a', href=True):
        if 'transcript' in link['href']:
            transcript_links.append(link['href'])
#iterate over transcript page links, get soup
    for transcript_link in transcript_links:
        transcript_url = transcript_link        
        transcript_response = requests.get(transcript_url)
        transcript_soup = BeautifulSoup(transcript_response.text, 'html.parser')
        # Find the 'download XML' link
        download_xml_link = transcript_soup.find('a', text='Download entire transcript in XML')
        if download_xml_link:
            download_xml_url = download_xml_link['href']
            # Download XML file
            xml_filename = f"{transcript_url.split(';id=')[-1]}.xml"
            download_xml(download_xml_url, xml_filename)
            print(f"Downloaded XML file: {xml_filename}")
            #pause for 2 secs to not spook the server
            time.sleep(2)
        else:
            print("Download XML link not found on:", transcript_url)
    #success
    print("XML files downloaded successfully")

#error raising for HTTP errors, request exceptions, and other exceptions
except requests.HTTPError as e:
    print('HTTP Error:', e)
except requests.RequestException as e:
    print('Request Exception:', e)
except Exception as e:
    print('Error:', e)