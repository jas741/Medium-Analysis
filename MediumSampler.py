

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas
from random import *


# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
browser = webdriver.Chrome(executable_path='/path/to/chromedriver', chrome_options=option)

browser.get("https://medium.com/@mediumstaff/followers")

# Wait 20 seconds for page to load

timeout = 20
try:
    WebDriverWait(browser, timeout)
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()


# scroll down first.

for i in range(1,70):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(.3)

# find_elements_by_xpath - Returns an array of selenium objects.

new_targets = browser.find_elements_by_xpath("//a[starts-with(@href,'https://medium.com/@')]")

link_urls = [link.get_attribute('href') for link in new_targets]

deduped_links = [x for x in link_urls if '?' not in x and 'MediumStaff' not in x]

groupsize = len(deduped_links)

print("We sampled a total of " + str(groupsize) + " initial followers of Medium Staff")

#use a random number method to select an element from deduped_links, go to its page to see its
#following number, and if its between 200 and 500, append it to TestList. Stop at 30.

Testlist = []


def value_to_float(x):
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        return float(x.replace('B', '')) * 1000000000
    else:
        return float(x)


while len(Testlist) < 30:
    test = sample(deduped_links,1)
    browser.get(test[0])

    timeout = 20
    try:
        WebDriverWait(browser, timeout)
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    follows_element0 = browser.find_element_by_xpath("//a[@data-action-value='following']")
    follows_element1 = follows_element0.text.rstrip(" Following")
    follows_number = value_to_float(follows_element1)

    html = browser.page_source
    if 'followers' in html:
        followedby_element0 = browser.find_element_by_xpath("//a[@data-action-value='followers']")
        followedby_element1 = followedby_element0.text.rstrip(" Followers")
        followedby_number = value_to_float(followedby_element1)
    else:
        followedby_number = 0
    if follows_number > 40 and follows_number < 600 and followedby_number < 30000 and test[0] not in Testlist:
        Testlist.append(test[0])


df = pandas.DataFrame(data={"30 Out of " + str(groupsize): Testlist})
                      
df.to_csv("./MediumSampler.csv", sep=',',index=False)
                      




