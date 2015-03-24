from lxml import html
from lxml import etree
import requests
import re
from sets import Set
import json
from bs4 import BeautifulSoup
import html5lib
import sys

def cleanUpHTML(sections_temp):
	sections = []
	for section in sections_temp:
		soup = BeautifulSoup(section.prettify(), 'html5lib')
		sections.append(soup.findAll('div')[2])
	return sections

def getClassName(div):
	tree = html.fromstring(div.prettify())
	name_unformatted = tree.xpath('//span/text()')
	return name_unformatted[0].strip()

def getClassType(div):
	tree = html.fromstring(div.prettify())
	type_unformatted = tree.xpath('text()')
	return type_unformatted[2].strip()

def getNumber(div):
	tree = html.fromstring(div.prettify())
	number_unformatted = tree.xpath('text()')
	return number_unformatted[2].strip()

def getAvailability(div):
	tree = html.fromstring(div.prettify())
	availability_unformatted = tree.xpath('//span/text()')
	return availability_unformatted[0].strip()

def getOpenSeats(div):
	tree = html.fromstring(div.prettify())
	open_seats_unformatted = tree.xpath('text()')
	return open_seats_unformatted[2].strip()

def getOpenRestrictedSeats(div):
	#Not worrying about open restricted seats
	return div

def getWaitlist(div):
	tree = html.fromstring(div.prettify())
	waitlist_unformatted = tree.xpath('text()')
	return waitlist_unformatted[2].strip()

def getTimeDateLocation(div, x):
	tree = html.fromstring(div.prettify())
	tds = tree.xpath('//td/text()')
	if(len(tds) == 0):
		return "-", "-", "-", "-"
	else:
		date_unformatted = tds[0]
		time_unformatted = tds[1]
		location_unformatted = tds[2]
		times = re.split('\s-\s', time_unformatted.strip())
		if len(times) not in [1, 2]:
			print time_unformatted.strip()
			sys.exit()
		if times[0] == "TBA":
			return 	times[0], times[0], date_unformatted.strip(), location_unformatted.strip()
		return times[0], times[1], date_unformatted.strip(), location_unformatted.strip()

def findCoursePage(department, class_num):
	count = 1
	#page with class schedule
	page = requests.get('http://www.lsa.umich.edu/cg/cg_detail.aspx?content=' + semesterCode + department + class_num + '001&termArray=' + semester + '_' + semesterCode)
	
	#retrieve each 'div' for the different sections of the class
	soup = BeautifulSoup(page.text, 'html5lib')
	sections_temp = soup.findAll('div', attrs={"class": "row clsschedulerow toppadding_main bottompadding_main"})
	while(len(sections_temp) == 0):
		count += 1
		if count < 10:
			count_str = "00" + str(count)
		elif count < 100:
			count_str = "0" + str(count)
		else:
			count_str = str(count)
		page = requests.get('http://www.lsa.umich.edu/cg/cg_detail.aspx?content=' + semesterCode + department + class_num + count_str + '&termArray=' + semester + '_' + semesterCode)
		soup = BeautifulSoup(page.text, 'html5lib')
		sections_temp = soup.findAll('div', attrs={"class": "row clsschedulerow toppadding_main bottompadding_main"})
		if count > 1000:
			errorFile = open('errors.txt', 'a')
			errorFile.write("TOO MANY PAGES: " + department + class_num + '\n')
			errorFile.close()
			return "skip"
			#sys.exit()

	#narrow in on the portion of the html we want
	return cleanUpHTML(sections_temp)

def getDaysArray(days_string, start, end):
	days_dictionary = {}
	if start == "TBA" and end == "TBA":
		return {"TBA": 0}
	times = ["8:00AM", "8:30AM", "9:00AM", "9:30AM", "10:00AM", "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM", "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM", "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", "9:00PM", "9:30PM", "10:00PM", "10:30PM", "11:00PM"]
	
	try:
		start_index = times.index(start)
		end_index = times.index(end)
	except:
		return "none"

	time_bitarray = ""
	for i in range(0, len(times) - 1):
		if i in range(start_index, end_index):
			time_bitarray += "1"
		else:
			time_bitarray += "0"
	d = re.split("(M|Tu|W|Th|F)", days_string)
	for elt in d:
		if elt == "":
			continue
		days_dictionary[elt] = int(time_bitarray, 2)
	return days_dictionary


CLASSES_JSON = []

courseGroups = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90), (90, 100), (100, 110), (110, 120), (120, 130), (130, 140), (140, 1000)]

if len(sys.argv) != 4:
	print "Not enough arguments"
	sys.exit()

scrapingGroup = int(sys.argv[1]) - 1  #0-14  ---  user inputs 1-15
semester = sys.argv[2]           #'f_15'
semesterCode = sys.argv[3]       #'2060'

#page with all departments
page = requests.get('http://www.lsa.umich.edu/cg/')
tree = html.fromstring(page.text)

CourseShortnames = tree.xpath('//select[@id="contentMain_lbSubject"]/option/@value')

#used to not add the same class more than once
scraped_subjects = Set([])

#176 subbjects so break up into CourseShortnames[0:45]  CourseShortnames[45:90]  CourseShortnames[90:135]  CourseShortnames[135:]

for subject in CourseShortnames[courseGroups[scrapingGroup][0]:courseGroups[scrapingGroup][1]]: #CourseShortnames[125:]: #CourseShortnames:
	
	pageCount = 1
	#page with all classes in the department - REMEMBER TO CHANGE "w_15"
	page = requests.get('http://www.lsa.umich.edu/cg/cg_results.aspx?termArray=' + semester + '_' + semesterCode + '&cgtype=ug&show=80&department=' + subject + '&iPageNum=' + str(pageCount))
	tree = html.fromstring(page.text)
	
	#The while loop is because all of the departments classes might not fit on one page so loop through all pages in the department
	while tree.xpath('//div[@class="alert alert-danger"]/strong/text()') != ['Error:']:
		#classes in the department
		classes = tree.xpath('//div[@class="row ClassRow ClassHyperlink result" or @class="row ClassRow ClassHyperlink resultalt"]//a//font/text()')
		for row in classes:
			class_info = re.split('\s+', row)
			class_description = re.split('\s{2,}', (re.split('\s-\s', row)[1]))[1]

			#   class_info[1] == department    class_info[2] == class number

			#don't add the same class more than once
			if (class_info[1] + class_info[2]) in scraped_subjects:
				continue
			else:
				scraped_subjects.add(class_info[1] + class_info[2])

			#used to output in JSON format
			json_dict = {"courseName": class_description, "courseShortname": class_info[1] + " " + class_info[2], "REC": [], "LEC": [], "DIS": [], "SEM": [], "LAB": [], "IND": []}

			#find the course page that has all of the department's courses and store 
			sections = findCoursePage(class_info[1], class_info[2])

			if sections == "skip":
				continue

			skip = False
			
			for section in sections:
				soup = BeautifulSoup(section.prettify(), 'html5lib')
				divs = soup.findAll('div')

				#seperate divs to deal with seperately
				name = getClassName(divs[1])
				type_ = getClassType(divs[3])
				number = getNumber(divs[6])
				#availability = getAvailability(divs[9])   <-- don't worry about it
				#open_seats = getOpenSeats(divs[12])   <-- don't worry about it
				#open_restricted_seats = getOpenRestrictedSeats(divs[15])  <-- don't worry about it
				waitlist = getWaitlist(divs[18])
				start_time, end_time, days, location = getTimeDateLocation(divs[21], class_info[1] + class_info[2])
				
				# if days == "-" then the class has no time information
				if days != "-":
					if "Course Number" not in json_dict:
						json_dict["courseNumber"] = number
					if len(re.findall('\((.+)\)', name)) != 0:
						dayz = getDaysArray(days, start_time, end_time)
						if dayz == "none":
							errorFile = open('errors.txt', 'a')
							errorFile.write("Times on the 15min - " + class_info[1] + class_info[2] + '\n')
							errorFile.close()
							skip = True
							break
						json_dict[re.findall('\((.+)\)', name)[0]].append({"section": re.findall('(\d\d\d)', name)[0], "start": start_time, "end": end_time, "location": location, "daysArray": dayz})

			if not skip:
				#print "Good: " + class_info[1] + class_info[2] 
				CLASSES_JSON.append(json_dict)


		pageCount += 1
		#page with all classes in the department
		page = requests.get('http://www.lsa.umich.edu/cg/cg_results.aspx?termArray=' + semester + '_' + semesterCode + '&cgtype=ug&show=80&department=' + subject + '&iPageNum=' + str(pageCount))
		tree = html.fromstring(page.text)

outfile = open("courses" + sys.argv[1] + ".txt", 'w')
outfile.write(json.dumps(CLASSES_JSON, indent=4, separators=(',', ': ')))
outfile.close()