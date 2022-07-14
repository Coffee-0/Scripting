from bs4 import BeautifulSoup
import requests
import csv


def get_url(position):
	template = f"https://in.indeed.com/jobs?q={position}&l&vjk=4cbec201f39319a7"
	url = template
	# print(url)
	return url


url = get_url("python")
response = requests.get(url)
# print(response)


soup = BeautifulSoup(response.text, 'html.parser')
cards = soup.find_all('div', 'job_seen_beacon')


for card in cards:

	job_title = card.find('a', class_="jcs-JobTitle")
	company_name = card.find('span', class_="companyName")
	location = card.find('div', class_="companyLocation")
	job_summary = card.find('div', class_="job-snippet")
	date_posted = card.find('span', class_="date")
	try:
		salary = card.find('div', class_="attribute_snippet").text
	except AttributeError:
		salary = ''

	print("Job Title: ", job_title.text.strip())
	print("Company Name: ", company_name.text.strip())
	print("Job Location: ", location.text.strip())
	print("Job Summary: ", job_summary.text.strip())
	print("Date Posted: ", date_posted.text.strip())
	print("Job Salary: ", salary)
	print()
	print()

