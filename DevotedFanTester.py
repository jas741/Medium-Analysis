from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas
from statistics import mean
from statistics import median
import numpy as np



# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
browser = webdriver.Chrome(executable_path='/path/to/chromedriver', chrome_options=option)

# get the list of people we collected using mediumsampler.py
starterdf = pandas.read_csv("./MediumSampler.csv")

#Check column name (see mediumsampler.py)
sourcelist = starterdf["30_of_578"].tolist()


#for each person in this list, we are going to find how many of the people they follow have no posts, and how many both have no posts and clap only for them (devotedfans)




total_followed = []
total_evaluated = []
postless_followed = []
percent_postless = []
devotedfan_followed = []
percent_devotedfan = []




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


for source in sourcelist:


# Go to desired website

    browser.get(source + "/following")

# Wait 20 seconds for page to load

    timeout = 20
    try:
        WebDriverWait(browser, timeout)
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

# get number of followers, and calibrate the scrolldown for it

    sourcefollows0 = browser.find_element_by_xpath("//a[@data-action-value='following']")
    sourcefollows1 = sourcefollows0.text.rstrip(" Following")
    follows_float = value_to_float(sourcefollows1)
    scrollnumber = int(follows_float/7)
    print(source + " follows " + str(follows_float))
    total_followed.append(follows_float)





# scroll down first. --- medium usually gives you 10 or so per scroll action, so diving the total by 7 seems safe but close enough. Add more sleeptime if your connection is slow (to allow loading)

    for i in range(1,scrollnumber):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.7)

# find_elements_by_xpath - Returns an array of selenium objects.

    new_targets = browser.find_elements_by_xpath("//a[contains(@href,'/@')]")


#getAttribute gets an href value from an element eg a div or an a

    link_urls = [link.get_attribute('href') for link in new_targets]

    deduped_links = [x for x in link_urls if '?' not in x and source not in x]


    haspostslist = []
    onlyclapsforlist = []

    for target in deduped_links:


# Go to desired website

        browser.get(target + "/latest")

        timeout = 20
        try:
            WebDriverWait(browser, timeout)
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        html1 = browser.page_source

    

#######. 'has not written' shows up on the /latest page of a medium user only if...

        if 'has not written' not in html1:
            haspostslist.append(True)
        else:
            haspostslist.append(False)

#### now lets check for whether theyve clapped only for the source ...

        browser.get(target + "/has-recommended")

        timeout = 20
        try:
            WebDriverWait(browser, timeout)
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
            
        clap_targets = browser.find_elements_by_xpath("//a[contains(@href,'/@')]")
        clap_links = [link.get_attribute('href') for link in clap_targets]
        other_claps = [x for x in clap_links if target not in x]
        outside_claps = [x for x in clap_links if source not in x and target not in x]



        if len(outside_claps) == 0 and len(other_claps) != 0:
            onlyclapsforlist.append(True)
        else:
            onlyclapsforlist.append(False)
    
#we want to confirm that we have in fact checked all of the reported followers. 
        
    total_evaluated.append(len(onlyclapsforlist))
 

    print(source + " total evaluated: " + str(len(onlyclapsforlist)))
    


    dfsketch = pandas.DataFrame(data={"Who": deduped_links, "Has_Posts?": haspostslist,  "Devoted": onlyclapsforlist})

    postfilter = dfsketch["Has_Posts?"]
    nopostfilter = postfilter == False

    NoPosts = dfsketch[nopostfilter] 

    postless_followed.append(len(NoPosts))
    percent_postless.append((len(NoPosts)/len(onlyclapsforlist))*100)


    devotedfilter = dfsketch["Devoted"]
    superfanfilter = np.logical_and(postfilter == False,devotedfilter == True)
    superfan = dfsketch[superfanfilter]


# OPTIONAL: save a csv of the list of superfans for each source
#   superfan.to_csv("./" + source + "_superfans.csv", sep=',', index=False)

    devotedfan_followed.append(len(superfan))
    percent_devotedfan.append((len(superfan)/len(onlyclapsforlist))*100)


    print(source + " postless followed: " + str(len(NoPosts)))
    print(source + " follows " + str(len(superfan)) + "devoted fans")



df = pandas.DataFrame(data={"source": sourcelist, "total_followed": total_followed, "total_evaluated": total_evaluated, "postless_followed": postless_followed, "percent_postless": percent_postless, "devotedfan_followed": devotedfan_followed, "percent_devoted": percent_devotedfan})
df.to_csv("./DevotedFansTestOutput.csv", sep=',',index=False)

