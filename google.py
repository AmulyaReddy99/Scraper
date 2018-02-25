#!/usr/bin/env python
from bs4 import BeautifulSoup
from stackoverflow import devHelp
import requests
import os
import shlex
import struct
import platform
import subprocess

MAX=5
query=''

def requestPg(query="today+news+headlines"):
	url='https://www.google.com/search?q='
	page=requests.get(url+query).text
	soup = BeautifulSoup(page,"lxml")

	for i in range(0,MAX):
		try:
			w=str(_get_terminal_size_linux()[0]-15)
			stri = "%-"+w+"s %10s"
			print (stri % ("","*** Bot ***"))
			c=soup.find_all('div', {'class':'g'})[i]
			heading=c.find('h3', {'class': 'r'}).text #heading
			para=c.find('span',{'class':'st'}).text
			w=str(_get_terminal_size_linux()[0]-len(heading)-10)
			stri = "%-"+w+"s %10s"
			print (stri % ("",heading))
			print (stri % ("",para))
		except:
			pass
	
	if(input("Do you want to switch to developer help center?(Y/N)\n").lower()=="y"): 
		devHelp()
	else:
		query=input("What else? \n")
		if(query=="quit"): exit()
		else: requestPg(query)

def chat():
	greetings()
	requestPg()

def greetings():
	print("="*_get_terminal_size_linux()[0])
	print("Hi! Welcome..")
	print("Enter quit to exit")
	print("Here are broad categories you can search for...")
	choice = input("Developer help center\n News \nWeather \nTranslate \nCalculator \nYoutube \nDictionary \nMore?\n")
	if(choice.lower()=="more"):
		choice = input("Restaurants near me \nMovies \nHorroscope \nCheap fights \nCalendar \nGames \nQuotes \nQuiz or Trivia\n")
	if(choice=="quit"): exit()
	else: requestPg(choice.replace(' ','+'))

def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

chat()
