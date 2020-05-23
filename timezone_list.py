import pandas as pd
import requests
import lxml.html as lh
from telethon import Button
import datetime as dt
import re
import pytz
from pytz import timezone
from pytz import common_timezones_set, common_timezones

long_url = "https://www.timeanddate.com/time/zones/"
sortedbytime_url = "https://www.timeanddate.com/time/current-number-time-zones.html"

def pull_from_web(url):
    table = pd.read_html(url)
    zone_table = table[0]
    print(zone_table.columns)
    print(zone_table)
    zone_table.to_csv("zones.csv")


def get_zones():
    zones = pd.read_csv("zones.csv", index_col=0)
    zone_display = zones[['UTC Offset', 'Example Location']] 
    zonelist = zone_display.values.tolist()
    return zonelist


def get_timezone():
    # source from pytz.common_timezones
    zones = pd.read_csv("pytz_zones.csv")
    zone_names  = zones.values.tolist()
    return zone_names


def get_zone_buttons(zones):
    buttons = []
    for zone in zones:
        utc_offset = str(zone[0])
        desc = "[" + utc_offset + "]\t" + str(zone[1])
        buttons.append([Button.inline(desc, utc_offset)])
    return buttons


def get_commontz():
    zones = pd.DataFrame(columns=['region', 'name'])
    for tz in pytz.common_timezones:
#        print(tz)
        if "/" in tz:
            dict1 = {}
            region = tz.split("/")
            dict1 = {'region': region[0], 'name': tz}
            zones = zones.append(dict1, ignore_index=True)
#            print(dict1)
    return zones
            

if __name__ == "__main__":
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    tz = pytz.timezone('US/Pacific')
    ct = dt.datetime.now(tz=tz)
    print(f'timezone: {tz}')
    print(f'ct : {ct}')
    fct = ct.strftime(fmt)
    print(f'fct: {fct}')

    pd = get_commontz()
    uszones = pd[pd['region'] == 'US']
    print(uszones['name'])
    
    utc_time = dt.datetime.now(tz=pytz.utc)
    print(utc_time)
    
    #pull_from_web(sortedbytime_url)
    #zonelist = get_zones()
    #print(zonelist)
        
"""
    # This timestamp is in UTC
    my_ct = dt.datetime.now(tz=pytz.UTC)
    print(my_ct)

    # Now convert it to another timezone
    new_ct = my_ct.astimezone(tz)
    print(new_ct)
 
""" 
   
"""
    # don't use, this is from timeanddate.com
    # its harder to convert and not as effective
    # use the pytz_zones list
    offset_sample = "UTC +8"
    offset_time = get_time_from_utc(offset_sample) 
    print(type(offset_time))
    print(offset_time)
"""