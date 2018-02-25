from bs4 import BeautifulSoup
import requests

questions=[]

def devHelp():
	url="https://stackoverflow.com" #use +
	query=input("Enter the keywords of question\n").replace(' ','+')
	page=requests.get(url+'/search?q='+query).text
	soup=BeautifulSoup(page,"lxml")

	print("*** Showing the 5 topmost relavant voted answer ***")
	question=soup.find_all('div', {'class':'summary'})
	for i in range(5):
		print(question[i].find('a').text.strip())
	query=question[0].find('a', href=True)['href']

	#new request
	page=requests.get(url+query).text
	soup=BeautifulSoup(page,"lxml")
	post_text=soup.find_all('div', {'class':'post-text'})
	print(post_text[0].text.strip())
	try:
		print(post_text[1].text.strip())
	except:
		pass