from bs4 import BeautifulSoup
import requests


def get_url(position):
	template = f"https://in.indeed.com/jobs?q={position}&l&vjk=4cbec201f39319a7"
	return template


URL = get_url("python")  # Enter Role Here
response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')
jobs = soup.find_all('div', 'job_seen_beacon')


def get_jobs(x):
	job_title = x.find('a', class_="jcs-JobTitle")
	company_name = x.find('span', class_="companyName")
	location = x.find('div', class_="companyLocation")
	job_summary = x.find('div', class_="job-snippet")
	date_posted = x.find('span', class_="date")
	try:
		salary = x.find('div', class_="attribute_snippet").text
	except AttributeError:
		salary = ''

	record = {"Job Title: ": job_title.text.strip(),
	          "Company Name: ": company_name.text.strip(),
	          "Job Location: ": location.text.strip(),
	          "Job Summary: ": job_summary.text.strip(),
	          "Date Posted: ": date_posted.text.strip(),
	          "Job Salary: ": salary}

	return record


JOBS = []

for i in range(1, 101):
	if i % 15 == 0:
		try:
			URL = "https://in.indeed.com" + soup.find('a', {'aria-label': 'Next'}).get('href')
		except AttributeError:
			break

	response = requests.get(URL)
	soup = BeautifulSoup(response.text, 'html.parser')
	jobs = soup.find_all('div', 'job_seen_beacon')

	for job in jobs:
		record = get_jobs(job)
		JOBS.append(record)


for i in JOBS:
	print(i)
	print()
	print()


# while True:
# 	try:
# 		URL = "https://in.indeed.com" + soup.find('a', {'aria-label': 'Next'}).get('href')
# 	except AttributeError:
# 		break
#
# 	response = requests.get(URL)
# 	soup = BeautifulSoup(response.text, 'html.parser')
# 	jobs = soup.find_all('div', 'job_seen_beacon')
#
# 	for job in jobs:
# 		record = get_jobs(job)
# 		JOBS.append(record)
#
# 		print(job)
