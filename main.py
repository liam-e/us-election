from selenium import webdriver
import json
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')

# driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)

driver = webdriver.Chrome(options=options)

url = "https://www.google.com/search?q=us+election&oq=us+election&aqs=chrome.0.69i59l4j69i60l3.1961j0j1&sourceid=chrome&ie=UTF-8"

driver.get(url)

biden_xpath = '/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[4]/div/div[1]/div[1]/div/div[2]/span'
trump_xpath = '/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[4]/div/div[1]/div[3]/div/div[2]/span'
trump_count = None
biden_count = None

try:
	biden_count = int(driver.find_element_by_xpath(biden_xpath).text.strip())
except ValueError:
	print(driver.find_element_by_xpath(biden_xpath).text.strip())

try:
	trump_count = int(driver.find_element_by_xpath(trump_xpath).text.strip())
except ValueError:
	print(driver.find_element_by_xpath(trump_xpath).text.strip())

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

driver.close()

driver.quit()
