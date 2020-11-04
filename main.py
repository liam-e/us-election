from selenium import webdriver

op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)

driver.get("https://www.theguardian.com/us-news/ng-interactive/2020/nov/03/us-election-2020-live-results-donald-trump-joe-biden-who-won-presidential-republican-democrat")

biden_count = int(driver.find_element_by_xpath('/html/body/div[4]/article/div/div[2]/div/figure/figure/div/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[1]').text)
trump_count = int(driver.find_element_by_xpath('/html/body/div[4]/article/div/div[2]/div/figure/figure/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[2]').text)


print(round(biden_count/270*50, 2), round(trump_count/270*50, 2))
