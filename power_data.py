from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
from us_states import states, reformat_2W_states, state_list
import re

main_url = "https://poweroutage.us/"
state_base = main_url + "area/state/"
regions_url = main_url +  "area/regions"
county_base = main_url + "area/county/"
region_state = main_url + "area/region/"
#print(soup.prettify()) # print the parsed data of html

site_link = "<a href=\"https://poweroutage.us\"> PowerOutage.US </a>" + "\n\n"

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def get_top5data(): 
    html_content = requests.get(main_url).text
    soup = BeautifulSoup(html_content, "lxml")
    topfive_page = soup.find("table", attrs={"class" : "topfivetable table-striped"})
    top_table_data = topfive_page.find_all("tr")
  
    top_states = []  
    topfive = site_link
    for i in top_table_data:
        for item in i.find_all("td"):
            str_item = str(item.text)
            if str_item in state_list:
                topfive += "<b>" + str_item + "</b>\t"
                top_states.append(str_item)
            else:
                topfive += str(item.text) + "\t"
        topfive += "\n"
    return topfive, top_states


def get_region_state_data(area):
    url = region_state + reformat_2W_states(area.lower())
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    region_data = soup.find("table")
    all_region = "<b>" + area + " Outages:</b>"
    for i in region_data:
        for item in i.find_all("td"):
           all_region += item.text + "\t"
        all_region += "\n"
    return all_region

    
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

# get outage number
def get_state_outage(state):
    state_url = state_base + state
    html_content = requests.get(state_url).text
    soup = BeautifulSoup(html_content, "lxml")
    state_link = "<a href=\"" +  state_url + "\">" + soup.title.text + "</a>\n"
    state_data = soup.find("div", attrs={"class" : "row col-md-12"})
    rows = state_data.find_all("div", attrs={"class": "row"})
    for i in rows:
        si = str(i)
        if "Outages" in si:
            cleanrow = cleanhtml(si).split()
            for j in cleanrow:
                count = j.replace(",", "")
                if count.isdigit():
                    return count
            
            

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


def get_county_data(county):
    try:
        county_url = county_base + county
        print(county_url + "\n")
        html_content = requests.get(county_url).text
        soup = BeautifulSoup(html_content, "lxml")
        county_link = "<a href=\"" +  county_url + "\">" + soup.title.text + "</a>\n"
        county_data = soup.find_all("div", attrs={"class": "col-xs-12 col-sm-4"})
        data = ""
        r = ""
        for row in county_data:
            r = cleanhtml(str(row).replace("  ","")).replace("\n", " ")
            data = data + r + "\n"
           # print(r)
        return county_link + data
    except Exception as e:
        return "No data, or invalid county number"
        
    
if __name__ == "__main__":
    """
    top5 = get_top5data()
    print(top5)
    print("====")
    
    region = get_region_data()
    print(region)
    print("====")
    """
    print("\nSTATE LEVEL DATA\n")
    state = get_state_data("california")
    print(state)
    print("====")
    
    """
    print("\nSan Francisco County: 2939\n")
    county = get_county_data("2939")
    print(county)
    print("=====")
    """

    area = "Pacific"    
    print(f"Testing area: {area}\n\n")
    state_regions = get_region_state_data(area)
    print(state_regions)