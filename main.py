#!/usr/bin/python3
from selenium import webdriver
import json
from datetime import datetime
import platform


def update_colleges():

	datetime_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

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

	url = "https://www.theguardian.com/us-news/ng-interactive/2020/nov/03/us-election-2020-live-results-donald-trump-joe-biden-who-won-presidential-republican-democrat"

	driver.get(url)

	biden_xpath = '/html/body/div[4]/article/div/div[2]/div/figure/figure/div/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[1]'
	trump_xpath = '/html/body/div[4]/article/div/div[2]/div/figure/figure/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[2]'

	try:
		biden_count = int(driver.find_element_by_xpath(biden_xpath).text.strip())
		trump_count = int(driver.find_element_by_xpath(trump_xpath).text.strip())
	except ValueError:
		with open("log.txt", "a") as f:
			f.write(f"Failure ValueError {datetime_string}\n")
			return

	if biden_count and trump_count:

		data = {
			"biden": {
				"college_count": f"{biden_count}",
				"width": f"{round(biden_count/270*50, 2)}%"
			},
			"trump": {
				"college_count": f"{trump_count}",
				"width": f"{round(trump_count/270*50, 2)}%"
			},
			"time_updated": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		}

		with open("public_html/us-election/data.json", "w") as f:
			json.dump(data, f, indent=4)

	with open("log.txt", "a") as f:
		f.write(f"Success {biden_count}-{trump_count} {datetime_string}\n")

	driver.close()

	driver.quit()


if __name__ == "__main__":
	update_colleges()
