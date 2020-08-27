# Import libraries
from parsel import Selector
from time import sleep
from selenium import webdriver
import re
import pandas as pd

# Create empty pandas dataframe with required columns
column_names = ["heading", "description"]
df = pd.DataFrame(columns=column_names)

# Start the webdriver
driver = webdriver.Chrome('C://Users//Hritik Attri//Downloads//chromedriver')

# Get the required URL
base_url = "https://www.holidify.com/"
driver.get(base_url)
sleep(0.5)

# Enter Delhi in the search field
search_field = driver.find_element_by_name("fname") 
search_field.send_keys("Delhi")
sleep(2)

# Click on "Places in New Delhi" button
places_to_visit_element = driver.find_elements_by_xpath("//*[@class='tt-suggestion tt-selectable']")[1]
places_to_visit_element.click()
sleep(3)

# We scrape as long as we can find the next page in the URL
next_page_found = True 
while next_page_found:
    # I used Selector from parsel library for searching xpath, it is just my preference when scraping data
    sleep(3)
    sel = Selector(text = driver.page_source)
    places_to_visit = sel.xpath("//*[@class='card content-card']")

    # For each place, scrape heading and description
    for place in places_to_visit:
        heading = place.xpath(".//*[@class='card-heading']/text()").extract_first().strip()
        heading = " ".join(re.findall("[^0-9.]+", heading)).strip()

        text = place.xpath(".//*[@class='card-text']/text()").extract_first().strip() 

        row = {"heading": heading, "description": text}

        # Append the results to dataframe
        df = df.append(row, ignore_index=True)

    # Try to find next page and visit it, but if not found exit the while loop
    try:
        next_page = driver.find_elements_by_xpath(".//li[contains(@class, 'next')]/a[@href]")[0].get_attribute("href")
        driver.get(next_page)
    except IndexError: 
        next_page_found = False

# Save results to csv
df.to_csv("results.csv", sep=",")

# Stop the webdriver
driver.quit()





