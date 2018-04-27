#npm install -g chromedriver
#chromedriver
from selenium import webdriver
import re
import requests
import json
import csv
import sys

PATH="/usr/local/lib/node_modules/chromedriver/lib/chromedriver/chromedriver"
browser=webdriver.Chrome(executable_path=PATH)
url="http://www.osmania.ac.in/res07/20180472.jsp" #3rd year
#url="http://www.osmania.ac.in/res07/20180472.jsp" #2rd year
browser.get(url)

#index of list l gives the roll number(last digits only)
myFile = open('OU Marks.csv', 'a')
with myFile:
	myFields = ['Name','Roll No','Sub1', 'Sub2','Sub3','Sub4','Sub5','Sub6','Sub7','Sub8','Sub9']
	writer = csv.DictWriter(myFile, fieldnames = myFields)
	writer.writeheader()
l=[]
def results(pattern,n=1,end=120):
	htno=pattern+'000'
	for i in range(n,end):
		if len(str(abs(i)))==1: htno=htno[:-1]+str(i)
		if len(str(abs(i)))==2: htno=htno[:-2]+str(i)
		if len(str(abs(i)))==3: htno=htno[:-3]+str(i)
		try:
			browser.find_element_by_xpath('//*[@id="AutoNumber6"]/tbody/tr[1]/td/b/font/input[1]').send_keys(htno)
			browser.find_element_by_xpath('//*[@id="AutoNumber6"]/tbody/tr[1]/td/b/font/input[2]').click()
			browser.find_element_by_xpath('//*[@id="AutoNumber5"]/tbody/tr[3]/td[3]/b/font').text
			details=browser.find_element_by_id('AutoNumber3').text
			t=re.split('\n',details)
			name=t[2].split(' Father')[0][5:]
			# roll=t[1].split('  ')[1][:12]
		except: pass
		#---> id="AutoNumber4": Marks details
		#get 3rd td in all trs in table of id="AutoNumber4"
		marks=browser.find_element_by_id('AutoNumber4').text
		subwise=re.split('  |\n|',marks)
		i=2
		count=0
		while(i<len(subwise)): #9 subjects
			m=subwise[i:i+5] #+5
			subject=m[1]
			try: marks=int(m[2])
			except:marks=0
			try: ses_marks=int(m[3])
			except: ses_marks=0
			status=m[-1]
			count+=1
			# if((i-2)%9==0): 
			# l1.append((marks,ses_marks,status))
			l.append((marks,ses_marks,status))
			if count==9:
				myFile = open('OU Marks.csv', 'a')
				with myFile:
					writer = csv.DictWriter(myFile, fieldnames = myFields)
					writer.writerow({'Name':name,'Roll No':htno,'Sub1':l[0], 'Sub2':l[1],'Sub3':l[2],'Sub4':l[3],'Sub5':l[4],'Sub6':l[5],'Sub7':l[6],'Sub8':l[7],'Sub9':l[8]})
					#search header, if not there add the field, if present
					l.clear()
					# if((i-2)%9==0): 
					# 	writer.writerow({'Sub1' : (marks,ses_marks,status)})
					# if((i-2)%9==1): 
					# 	writer.writerow({'Sub2' : (marks,ses_marks,status)})
					# if((i-2)%9==2): 
					# 	writer.writerow({'Sub3' : (marks,ses_marks,status)})
					# if((i-2)%9==3): 
					# 	writer.writerow({'Sub4' : (marks,ses_marks,status)})
					# if((i-2)%9==4): 
					# 	writer.writerow({'Sub5' : (marks,ses_marks,status)})
					# if((i-2)%9==5): 
					# 	writer.writerow({'Sub6' : (marks,ses_marks,status)})
					# if((i-2)%9==6): 
					# 	writer.writerow({'Sub7' : (marks,ses_marks,status)})
					# if((i-2)%9==7): 
					# 	writer.writerow({'Sub8' : (marks,ses_marks,status)})
					# if((i-2)%9==8): 
					# 	writer.writerow({'Sub9' : (marks,ses_marks,status)})

			# if((i-2)%9==0): writer.writerow({'Sub1' : (marks,ses_marks,status)})
			# if((i-2)%9==1): writer.writerow({'Sub2' : (marks,ses_marks,status)})
			# if((i-2)%9==2): writer.writerow({'Sub3' : (marks,ses_marks,status)})
			# if((i-2)%9==3): writer.writerow({'Sub4' : (marks,ses_marks,status)})
			# if((i-2)%9==4): writer.writerow({'Sub5' : (marks,ses_marks,status)})
			# if((i-2)%9==5): writer.writerow({'Sub6' : (marks,ses_marks,status)})
			# if((i-2)%9==6): writer.writerow({'Sub7' : (marks,ses_marks,status)})
			# if((i-2)%9==7): writer.writerow({'Sub8' : (marks,ses_marks,status)})
			# if((i-2)%9==8): writer.writerow({'Sub9' : (marks,ses_marks,status)})
			i=i+5	 
 
		print("Writing complete")

# n=int(input("Enter the starting of roll numbers "))
# end=int(input("Enter the ending of roll numbers "))
try: results('160815733',1,120)
except Exception as e: print(e)

# def sub(INSUB,roll_no=0):
# 	INSUB=INSUB.upper()
# 	if(roll_no==0):
# 		if INSUB=='MATHS': print(l1)
# 		if INSUB=='SCIENCE': print(l2)
# 		if INSUB=='PHYSICS': print(l3)
# 		if INSUB=='SOCIAL': print(l4)
# 		if INSUB=='LAB1': print(l5)
# 		if INSUB=='LAB2': print(l6)
# 		if INSUB=='ENGLISH': print(l7)
# 		if INSUB=='FRENCH': print(l8)
# 		if INSUB=='SANSKRIT': print(l9)
# 	else:
# 		if INSUB=='MATHS': print(l1[roll_no-1])
# 		if INSUB=='SCIENCE': print(l2[roll_no-1])
# 		if INSUB=='PHYSICS': print(l3[roll_no-1])
# 		if INSUB=='SOCIAL': print(l4[roll_no-1])
# 		if INSUB=='LAB1': print(l5[roll_no-1])
# 		if INSUB=='LAB2': print(l6[roll_no-1])
# 		if INSUB=='ENGLISH': print(l7[roll_no-1])
# 		if INSUB=='FRENCH': print(l8[roll_no-1])
# 		if INSUB=='SANSKRIT': print(l9[roll_no-1])


# print("MATHS | SCIENCE | PHYSICS | SOCIAL | LAB1 | LAB2 | ENGLISH | FRENCH | SANSKRIT\n")
# INSUB=input("Enter the subject: ")
# roll_no=int(input("Enter the roll no if you want to see the individual marks in this subject else press 0 to show all results of the subject "))
# sub(INSUB,roll_no)



