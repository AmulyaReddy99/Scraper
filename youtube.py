from bs4 import BeautifulSoup
import requests
import click

@click.command()
def cli():
	print("Youtube Trends")

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

url='https://youtube.com/feed/trending'
page=requests.get(url).text
soup = BeautifulSoup(page,"lxml")
headings = soup.find_all('h3',{'class':'yt-lockup-title'})
description = soup.find_all('div',{'class':'yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2'})
other = soup.find_all('ul',{'class':'yt-lockup-meta-info'})

for i in range(1,10):
	print(bcolors.BOLD+headings[i].text+bcolors.ENDC)
	print(description[i].text)
	meta_info = other[i].find_all('li')
	print(bcolors.OKGREEN+meta_info[0].text+"\t"+meta_info[1].text+bcolors.ENDC)
	print("\n")


