from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
from us_states import states

main_url = "https://poweroutage.us/"
state_base = main_url + "area/state/"
regions_url = main_url +  "area/regions"
#california = state_base + "california"
print(states['WA'])
#print(soup.prettify()) # print the parsed data of html


def get_top5data(): 
    html_content = requests.get(main_url).text
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.title.text)
    topfive_page = soup.find("table", attrs={"class" : "topfivetable table-striped"})
    return topfive_page

def get_region_data():
    html_content = requests.get(regions_url).text
    soup = BeautifulSoup(html_content, "lxml")
    region_data = soup.find("table")
    return region_data

def get_state_data(state):
    state_url = state_base + state
    print(state_url)
    html_content = requests.get(state_url).text
    soup = BeautifulSoup(html_content, "lxml")
    print(soup.title.text)
    state_data = soup.find("div", attrs={"class" : "row col-md-12"})
    return state_data

    
if __name__ == "__main__":
    print("\nTOP AREAS FOR OUTAGES:")
    top5 = get_top5data()
    print(top5)
    
    print("\nREGIONAL OUTAGES:")
    region = get_region_data()
    print(region.text)
    
    print("\nSTATE LEVEL DATA")
    state = get_state_data("california")
    print("====")
#    print(state)
#    sinfo = state.text.strip("\t")
#    print(sinfo)
    
    pass





"""
    # traversing example:
    top_table_data = topfive_page.find_all("tr")
    print(top_table_data)
    for i in top_table_data:
        for item in i.find_all("td"):
           print(item.text)
           

df = pd.DataFrame()
top_areas = pd.read_html(main_url, header=0)
top_areas = pd.read_html(regions, header=0)
print(top_areas[0])
print(type(top_areas))

"""
