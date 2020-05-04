from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
from us_states import states
import re

main_url = "https://poweroutage.us/"
state_base = main_url + "area/state/"
regions_url = main_url +  "area/regions"
#print(soup.prettify()) # print the parsed data of html

site_link = "<a href=\"https://poweroutage.us\"> PowerOutage.US </a>" + "\n"

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def get_top5data(): 
    html_content = requests.get(main_url).text
    soup = BeautifulSoup(html_content, "lxml")
    topfive_page = soup.find("table", attrs={"class" : "topfivetable table-striped"})
    top_table_data = topfive_page.find_all("tr")

    topfive = site_link
    
    for i in top_table_data:
        for item in i.find_all("td"):
            
            topfive += str(item.text) + "\t"
        topfive += "\n"

    return topfive


def get_region_data():
    html_content = requests.get(regions_url).text
    soup = BeautifulSoup(html_content, "lxml")
    region_data = soup.find("table")
    all_region = "<b>Regional Outages:</b>"
    for i in region_data:
        for item in i.find_all("td"):
           all_region += item.text + "\t"
        all_region += "\n"

    return all_region


def get_state_data(state):
    state_url = state_base + state
    #print(state_url)
    
    html_content = requests.get(state_url).text
    soup = BeautifulSoup(html_content, "lxml")

    state_link = "<a href=\"" +  state_url + "\">" + soup.title.text + "</a>\n"
    
    state_data = soup.find("div", attrs={"class" : "row col-md-12"})
    rows = state_data.find_all("div", attrs={"class": "row"})
    clean_rows = ""
    data = ""
    for i in rows:
        data += str(i).replace("  ", "")
    clean_rows = cleanhtml(data)

    return state_link + clean_rows


    
if __name__ == "__main__":
    top5 = get_top5data()
    print(top5)
    print("====")
    
    region = get_region_data()
    print(region)
    print("====")

    print("\nSTATE LEVEL DATA\n")
    state = get_state_data("california")
    print(state)
    print("====")

