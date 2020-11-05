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
	options.add_argument('--disable-gpu')
	options.add_argument('--remote-debugging-port=9222')

	if platform.system() == "Windows":
		driver = webdriver.Chrome(options=options)
	else:
		driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)

	logging.info(f'Set up chromedriver for {platform.system()} OS')

	url = "https://www.theguardian.com/us-news/ng-interactive/2020/nov/03/us-election-2020-live-results-donald-trump-joe-biden-who-won-presidential-republican-democrat"

	logging.info(f'Requesting HTTP from URL...')

	resp = requests.get(url)

	if resp.status_code == 200:
		logging.info(f'Response status code {resp.status_code}')
	else:
		logging.error(f'Response status code {resp.status_code}')
		write_to_log_list(False)
		return

	driver.get(url)

	biden_xpath = '/html/body/div[4]/article/div/div[2]/div/figure/figure/div/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[1]'
	trump_xpath = '/html/body/div[4]/article/div/div[2]/div/figure/figure/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[2]'

	biden_element = driver.find_element_by_xpath(biden_xpath)
	trump_element = driver.find_element_by_xpath(trump_xpath)

	if biden_element and trump_element:
		try:
			biden_count = int(biden_element.text.strip())
			trump_count = int(trump_element.text.strip())
		except ValueError:
			logging.error(f'Cannot retrieve data from webpage element')
			write_to_log_list(False)
			return
	else:
		logging.error(f'Cannot retrieve element from webpage')
		write_to_log_list(False)
		return

	data = {
		"biden": {
			"college_count": f"{biden_count}",
			"width": f"{round(biden_count/270*50, 2)}%"
		},
		"trump": {
			"college_count": f"{trump_count}",
			"width": f"{round(trump_count/270*50, 2)}%"
		},
		"time_updated": datetime.now().strftime(date_fmt)
	}

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
