from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
from us_states import states

main_url = "https://poweroutage.us/"
state = main_url + "area/state/"
regions = main_url +  "area/regions"
california = state + "california"
#print(states['WA'])
#print(soup.prettify()) # print the parsed data of html


def get_top5data(): 
    html_content = requests.get(main_url).text
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.title.text)

    topfive_page = soup.find("table", attrs={"class" : "topfivetable table-striped"})
    return topfive_page
    
if __name__ == "__main__":
    top5 = get_top5data()
    print(top5)
    pass

"""
    top_table_data = topfive_page.find_all("tr")
    print(top_table_data)

    for i in top_table_data:
        for item in i.find_all("td"):
            print(item)
    #        print(item.text)


"""
    
    
"""
df = pd.DataFrame()
top_areas = pd.read_html(main_url, header=0)
top_areas = pd.read_html(regions, header=0)
print(top_areas[0])
print(type(top_areas))
"""
