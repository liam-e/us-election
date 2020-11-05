#!/usr/bin/python3
from selenium import webdriver
import json
from datetime import datetime
import platform
import os
import logging
import requests

date_fmt = '%d/%m/%Y %H:%M:%S'


def update_colleges():
	log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

	logging.basicConfig(filename='main.log', filemode='w', format=log_fmt, datefmt=date_fmt, level=logging.INFO)

	source_dir = os.path.dirname(os.path.abspath(__file__))

	logging.info(f'Source directory = {source_dir}')

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	# options.add_argument('--disable-gpu')
	# options.add_argument('--remote-debugging-port=9222')

	if platform.system() == "Windows":
		driver = webdriver.Chrome(options=options)
	else:
		driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)

	logging.info(f'Set up chromedriver for {platform.system()} OS')

	url = "https://www.google.com/search?q=us+election&oq=us+election&aqs=chrome.0.69i59l4j69i60l3.1503j0j4&sourceid=chrome&ie=UTF-8"

	logging.info(f'Requesting HTTP from URL...')

	resp = requests.get(url)

	if resp.status_code == 200:
		logging.info(f'Response status code {resp.status_code}')
	else:
		logging.error(f'Response status code {resp.status_code}')
		write_to_log_list(False)
		return

	driver.get(url)

	biden_xpath = '/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[4]/div/div[1]/div[1]/div/div[2]/span'
	trump_xpath = '/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[4]/div/div[1]/div[3]/div/div[2]/span'

	try:
		biden_element = driver.find_element_by_xpath(biden_xpath)
		trump_element = driver.find_element_by_xpath(trump_xpath)
	except:
		print(f'Cannot retrieve element from webpage')
		logging.error(f'Cannot retrieve element from webpage')
		write_to_log_list(False)
		return

	if biden_element and trump_element:
		try:
			biden_count = int(biden_element.text.strip())
			trump_count = int(trump_element.text.strip())
		except ValueError:
			print(f'Cannot retrieve data from webpage element')
			logging.error(f'Cannot retrieve data from webpage element')

			with open(f"{source_dir}/public_html/us-election/data.json", "r") as f:
				old_data = json.load(f)
			biden_count = old_data["biden"]["college_count"]
			trump_count = old_data["trump"]["college_count"]
	else:
		print(f'Cannot retrieve element from webpage')
		logging.error(f'Cannot retrieve element from webpage')
		with open(f"{source_dir}/public_html/us-election/data.json", "r") as f:
			old_data = json.load(f)

		biden_count = old_data["biden"]["college_count"]
		trump_count = old_data["trump"]["college_count"]

	data = {
		"biden": {
			"college_count": f"{biden_count}",
			"width": f"{round(biden_count / 270 * 50, 2)}%"
		},
		"trump": {
			"college_count": f"{trump_count}",
			"width": f"{round(trump_count / 270 * 50, 2)}%"
		},
		"time_updated": datetime.now().strftime(date_fmt)
	}

	for i, state_name in enumerate(['Georgia', 'Nevada', 'North Carolina', 'Pennsylvania', 'Arizona', 'Florida']):

		row = i + 1

		state_name_cell = driver.find_element_by_xpath(
			f"/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/g-accordion/div/g-expandable-container/div/div[{row}]/div/div[1]/span")

		if state_name_cell and state_name_cell.text.strip() == state_name:

			college_votes = driver.find_element_by_xpath(
				f"/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/g-accordion/div/g-expandable-container/div/div[{row}]/div/div[1]/div/span[1]")

			biden_perc = driver.find_element_by_xpath(
				f"/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/g-accordion/div/g-expandable-container/div/div[{row}]/div/div[2]/div[1]/span[1]")
			trump_perc = driver.find_element_by_xpath(
				f"/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/g-accordion/div/g-expandable-container/div/div[{row}]/div/div[2]/div[2]/span[1]")

			biden_votes = driver.find_element_by_xpath(
				f"/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/g-accordion/div/g-expandable-container/div/div[{row}]/div/div[2]/div[1]/span[2]")
			trump_votes = driver.find_element_by_xpath(
				f"/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/g-accordion/div/g-expandable-container/div/div[{row}]/div/div[2]/div[2]/span[2]")

			perc_counted = driver.find_element_by_xpath(
				f"/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/g-accordion/div/g-expandable-container/div/div[{row}]/div/div[1]/div/span[3]")

			if biden_perc and trump_perc and biden_votes and trump_votes and perc_counted:
				won = False
				try:
					biden_w = biden_perc.value_of_css_property("color")
					trump_w = trump_perc.value_of_css_property("color")
					if biden_w == "rgba(255, 255, 255, 1)" or trump_w == "rgba(255, 255, 255, 1)":
						won = True
				except:
					pass

				try:
					college_votes = int(college_votes.text.strip().split(" ")[0])

					biden_perc = float(biden_perc.text.strip().split("%")[0])
					trump_perc = float(trump_perc.text.strip().split("%")[0])

					biden_votes = int("".join(biden_votes.text.strip().split(",")))
					trump_votes = int("".join(trump_votes.text.strip().split(",")))

					perc_counted = int(perc_counted.text.strip().split("%")[0])

					if biden_votes > trump_votes:
						leaning = "Biden"
					else:
						leaning = "Trump"

					state_d = {
						"name": state_name,
						"college_votes": college_votes,
						"biden_perc": biden_perc,
						"trump_perc": trump_perc,
						"biden_votes": biden_votes,
						"trump_votes": trump_votes,
						"perc_counted": perc_counted,
						"won": won,
						"leaning": leaning,
					}

					data["-".join(state_name.lower().split(" "))] = state_d
				except ValueError:
					print(f'Cannot retrieve state data from webpage - format error')
					logging.error(f'Cannot retrieve state data from webpage - format error')
					write_to_log_list(False)
					return
			else:
				print(f'Cannot retrieve state element from webpage')
				logging.error(f'Cannot retrieve state element from webpage')
				write_to_log_list(False)
				return

		else:
			print(f'Cannot retrieve state element from webpage - wrong state name - should be {state_name}')
			logging.error(f'Cannot retrieve state element from webpage - wrong state name - should be {state_name}')
			write_to_log_list(False)
			return

	with open(f"{source_dir}/public_html/us-election/data.json", "w") as f:
		json.dump(data, f, indent=4)

	write_to_log_list()

	driver.close()

	driver.quit()

	logging.info(f'Successful.')


def write_to_log_list(success=True):
	if success:
		success_failure = "success"
	else:
		success_failure = "failure"

	with open(f"{os.path.dirname(os.path.abspath(__file__))}/list.log", "a") as f:
		f.write(f"{success_failure} {datetime.now().strftime(date_fmt)}\n")


if __name__ == "__main__":
	update_colleges()
