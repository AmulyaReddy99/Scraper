import csv

lines = open('faculty.txt').read().split('\n')
for i in range(len(lines)//7):
	lines.remove('')

facultyFile = open('faculty.csv','a')
fields = ['Prof name', 'Prof', 'Edu', 'Research Areas', 'Research Center/Lab']
with facultyFile:
	writer = csv.DictWriter(facultyFile, fieldnames = fields)
	writer.writeheader()

facultyFile = open('faculty.csv','a')
with facultyFile:
	writer = csv.DictWriter(facultyFile, fieldnames = fields)
	for i in range(len(lines)//6):
		writer.writerow({'Prof name': lines[i*6], 'Prof': lines[i*6+1],'Edu': lines[i*6+2], 'Research Areas': lines[i*6+4], 'Research Center/Lab': lines[i*6+5][21:]})

