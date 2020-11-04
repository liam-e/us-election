from selenium import webdriver
import json
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)

driver.get("https://www.theguardian.com/us-news/ng-interactive/2020/nov/03/us-election-2020-live-results-donald-trump-joe-biden-who-won-presidential-republican-democrat")

biden_count = int(driver.find_element_by_xpath('/html/body/div[4]/article/div/div[2]/div/figure/figure/div/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[1]').text)
trump_count = int(driver.find_element_by_xpath('/html/body/div[4]/article/div/div[2]/div/figure/figure/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[2]').text)

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

driver.quit()
