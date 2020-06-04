from telethon import TelegramClient, events, Button
from power_data import get_state_data, get_top5data, get_region_data, get_region_state_data, get_county_data
from us_states import is_state_value, two_letter_statecode, reformat_2W_states, states, state_list
from us_states import regions, south, pacific, get_state_buttons, get_buttons, split
from us_states import all_regions
import yaml
import logging
from logging import handlers
from timezone_list import get_zones, get_zone_buttons
from timezone_list import get_common_buttons, get_commontz, get_localized_time

import datetime as dt 
from pymongo_tools import get_count, delete_doc, find_doc, add_doc, drop_bulk_db

log_path = '/Users/octo/url-watcher-bot/logs/logfile'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

########################################
# Log to a rotating file - why isn't this working?
level = logging.INFO
logger.setLevel(level)
# 5*5MB log files max:
h = logging.handlers.RotatingFileHandler(log_path, encoding='utf-8', maxBytes=5 * 1024 * 1024, backupCount=5)
# example of format: 2019-04-05 20:28:45,944  INFO: blah
h.setFormatter(logging.Formatter("%(asctime)s\t%(levelname)s:%(message)s"))
h.setLevel(level)
logger.addHandler(h)
########################################

path  = "./"
config_file = path + 'config_test.yml'
with open(config_file, 'rb') as f:
    config = yaml.safe_load(f)

TOKEN = config['bot_token']
print(f'Bot Token: {TOKEN}')
outbound = config['outbound']
print(f'Outbound Feed: {outbound}')
inbounds = config['inbound_streams']
print(f'Inbound Feeds: {inbounds}')

client = TelegramClient(config["session_name"], 
                        config["api_id"], 
                        config["api_hash"])

# Default to another parse mode
client.parse_mode = 'html'

def get_regional_tz_buttons(region, df):
    rzones = df[df['region'] == region]['name']
    ul  = rzones.values.tolist()
    buttons = get_common_buttons(ul)
    return buttons


@client.on(events.CallbackQuery())
async def callback(event):
    query_name = event.data.decode()
#    print(f"callback: " + query_name)
    await event.edit('Thank you for clicking {}!'.format(query_name))
    df = get_commontz()
    timezone_regions = df.region.unique()

    msg = ""
    # print(state_list)
    if query_name in regions:
        msg = get_region_state_data(query_name)
        await client.send_message(event.sender_id, msg)
        state_buttons = get_state_buttons(query_name)
        note =  "\nGet more data below:\n"
        await client.send_message(event.sender_id, note, buttons=state_buttons)
    elif query_name in state_list:
    #   print(f"getting state data {query_name.lower()}")
        msg = get_state_data(reformat_2W_states(query_name))
        await client.send_message(event.sender_id, msg)
    elif query_name in timezone_regions:
        tzbuttons = get_regional_tz_buttons(query_name, df)        
        await client.send_message(event.sender_id, "select a timezone", buttons=tzbuttons)
    elif query_name in list(df['name']):
        # fix the pacific option, which conflicts with state regions
        loctime = get_localized_time(query_name)
        msg = "Your localtime is: " + str(loctime)
        await client.send_message(event.sender_id, msg)
    

@client.on(events.NewMessage(pattern='(?i)/contact', incoming=True, outgoing=True))    
async def new_handler(event):
    msg = 'Original Data is from poweroutage.us.'
    msg = msg + 'Telegram bot development is independent, has no affliation to above site. \n\n'
    msg = msg + 'Questions, bug reports? Contact us via @powerfeedback_bot\n'
    await client.send_message(event.sender_id, msg)
    

@client.on(events.NewMessage(pattern='(?i)/start', forwards=False, outgoing=False))
async def new_handler(event):
    msg = 'Welcome to PowerOutage.US watcher bot\n\n'
    msg = msg + '/outages - outages by region,\n'
    msg = msg + '/alerts - setup alerts  \n'
    msg = msg + "/contact - info about this bot\n"
    await client.send_message(event.sender_id, msg)


@client.on(events.NewMessage(incoming=True, outgoing=False))
async def state_handler(event):
    try:
        input = str(event.raw_text)
#       print(f'state/county handler: {input}')
        if len(input) == 4:
            msg = get_county_data(input)
            await client.send_message(event.sender_id, msg)            
        if len(input) == 2:
            state_name = two_letter_statecode(input)
            msg = get_state_data(state_name)
            await client.send_message(event.sender_id, msg)
        elif len(input) > 0 and is_state_value(input):
            msg = get_state_data(reformat_2W_states(input))
            await client.send_message(event.sender_id, msg)
    except Exception as e:
            await client.send_message(event.sender_id, 'Not a State or not found. Please give a valid state.')


thresholds = ['10k', '50k', '100k']
time_intervals = ['6', '12', '24']

def parse_alert(inputstr, userid, username): 
    iarr  = inputstr.split(' ')
    print(iarr)
    oktogo = True
    # validate inputs
    if iarr[1] not in thresholds:
        logger.info("invalid threshold: "+ iarr[1])
        oktogo = False
    if iarr[2] not in time_intervals:
        logger.info("invalid time interval: "+ iarr[2])
        oktogo = False
    if iarr[3] not in all_regions:
        logger.info("invalid location: "+ iarr[3])
        oktogo = False
    if oktogo:
        # add to mongodb
        add_post ={
            'userid':  userid,
            'username': username,
            'time_interval': iarr[1],
            'threshold': iarr[2],
            'region' : iarr[3],
            'active' : True,
            'initdate': dt.datetime.now()
        }
        print(add_post)
        
        result = add_doc(add_post)
        print(result)

    return oktogo
        

@client.on(events.NewMessage(incoming=True, outgoing=False))
async def alert_handler(event):
    try:
        inputstr = event.raw_text
        if '/setalert' in inputstr:
            uname = await event.get_sender()
            print("username " + str(uname.username))
            print("sender id " + str(event.sender_id))
            result = parse_alert(inputstr, event.sender_id, uname.username)
            if result is True:
                msg = 'Ok, settng alert for: ' + inputstr
                await client.send_message(event.sender_id, msg)
            elif result is False:
                msg = 'Error setting alert, bad parameters'
                await client.send_message(event.sender_id, msg)
    except Exception as e:
            logger.info(e)
            await client.send_message(event.sender_id, 'Invalid Alert parameters.')


@events.register(events.NewMessage(incoming=True, outgoing=False))
async def alerthandler(event):
    input = str(event.raw_text)
#    print("outages handler: {input}")
    if '/alerts' in event.raw_text:
        print(input)
        msg = 'Fetching.... ' + input
        await client.send_message(event.sender_id, msg, buttons=[
            [Button.text('Set Alert', resize=True, single_use=True),
             Button.text('Stop Notifications', resize=True, single_use=True)],
            [Button.text('Show Alerts', resize=True, single_use=True),
             Button.text('/start', resize=True, single_use=True)]])
    elif 'Set Alert' in event.raw_text:
        # set up alert
        msg = "example: /setalert 10k 24 California"
        await client.send_message(event.sender_id, msg)
    elif 'Stop Notifications' in event.raw_text:
        msg = "Stopping all notifications"
        await client.send_message(event.sender_id, msg)        
    elif 'Show Alerts' in event.raw_text:
        # get alert information from mongodb
        msg = "Here are the currently active alerts:" 
        await client.send_message(event.sender_id, msg)


@events.register(events.NewMessage(incoming=True, outgoing=False))
async def handler(event):
    input = str(event.raw_text)
#    print("outages handler: {input}")

    if '/outages' in event.raw_text:
        await client.send_message(event.sender_id, 'Get Updates', buttons=[
#            [Button.text('/alerts', resize=True, single_use=True), # show alerts, # stop alerts
#             Button.text('Set Time Zone', resize=True, single_use=True),],
            [Button.text('Top 5 Outages', resize=True, single_use=True),
            Button.text('Regional Outages', resize=True, single_use=True),], 
            [Button.text('State', resize=True, single_use=True),
            Button.text('County', resize=True, single_use=True)]
        ])
    elif 'Top 5 Outages' in event.raw_text:
        msg, top5states = get_top5data()
        top5_buttons = get_buttons(top5states)
        top5b = split(top5_buttons, 2)
        await client.send_message(event.sender_id, msg, buttons=top5b)
        logger.info("inside top 5 outages")
    elif 'Regional Outages' in event.raw_text:
        msg = get_region_data()
        msg += "\n Get more data from below:\n"
        region_buttons = get_buttons(regions)
        rbuttons = split(region_buttons, 2)
        await client.send_message(event.sender_id, msg, buttons=rbuttons)
    elif 'State' in event.raw_text:
        msg = "Enter State Name or 2 letter code: (E.g. California or CA)"
        await client.send_message(event.sender_id, msg)
    elif 'County' in event.raw_text:
        msg = "Enter 4 letter county code. You can find code in the link on PowerOutage.US\n"
        msg = "e.g. 2939 for San Francisco -  https://poweroutage.us/area/county/2939\n"
        await client.send_message(event.sender_id, msg)
    elif 'Set Time Zone' in event.raw_text:
        try:
            logger.info("Inside Set Time zone, geo region")
            msg = "\nSelect your Geo Region: \n"
            df = get_commontz()
            uniq = df.region.unique()  
            zones = get_common_buttons(uniq)
            await client.send_message(event.sender_id, msg, buttons=zones)
            
        except Exception as e:
            logger.info(e)
            
client.start(bot_token=TOKEN)

with client:
    client.add_event_handler(handler)
    client.add_event_handler(alerthandler)

    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()


"""
time interval : 'every 24 hrs'
alert zone : all regions, state, country

Power levels thresholds
10k - 50k Outages  (Yellow Alert)
50k - 100k Outages (Orange Alert)
>100k Outages (Red Alert)

Example code: https://github.com/LonamiWebs/Telethon/blob/master/telethon_examples/replier.py
"""