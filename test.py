from telethon import TelegramClient, events, Button
from power_data import get_state_data, get_top5data, get_region_data, get_county_data
from us_states import is_state_value, two_letter_statecode, reformat_2W_states, states
import yaml
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

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

####
@client.on(events.CallbackQuery(data=b'clickme'))
async def callback(event):
    print(event.data)
    await event.edit('Thank you for clicking {}!'.format(event.data))

@client.on(events.NewMessage(incoming=True, outgoing=True))    
async def new_handler(event):
    if 'alerts' in event.raw_text:
        await client.send_message(event.sender_id, 'A single button, with "clickme" as data',
                        buttons=Button.inline('Get Data', b'clickme'))
#####

@client.on(events.NewMessage(pattern='(?i)/start', forwards=False, outgoing=False))
async def new_handler(event):
    await client.send_message(event.sender_id, 'Welcome to PowerOutage.US watcher bot\n\n/outages - outages by region\n/state california - get state data \n/alerts - setup alerts ')


@client.on(events.NewMessage(incoming=True, outgoing=False))
async def state_handler(event):
    try:
        input = str(event.raw_text)
        print(f'state/county handler: {input}')
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
        
        
@events.register(events.NewMessage(incoming=True, outgoing=False))
async def handler(event):
    input = str(event.raw_text)
    print("outages handler: {input}")
    if '/outages' in event.raw_text:
        await client.send_message(event.sender_id, 'Get Updates', buttons=[
            Button.text('Top 5 Outages', resize=True, single_use=True),
            Button.text('Regional Outages', resize=True, single_use=True),
            Button.text('State', resize=True, single_use=True),
            Button.text('County', resize=True, single_use=True)
        ])
    elif 'Top 5 Outages' in event.raw_text:
        msg = get_top5data()
        await client.send_message(event.sender_id, msg)
    elif 'Regional Outages' in event.raw_text:
        msg = get_region_data()
        await client.send_message(event.sender_id, msg)
    elif 'State' in event.raw_text:
        msg = "Enter State Name or 2 letter code: (E.g. California or CA)"
        await client.send_message(event.sender_id, msg)
    elif 'County' in event.raw_text:
        msg = "Enter 4 letter county code. You can find on PowerOutage.US"
        await client.send_message(event.sender_id, msg)
    
                
client.start(bot_token=TOKEN)

with client:
    client.add_event_handler(handler)
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()


"""
Power levels
10k - 50k Outages  (Yellow Alert)
50k - 100k Outages (Orange Alert)
>100k Outages (Red Alert)

Example code: https://github.com/LonamiWebs/Telethon/blob/master/telethon_examples/replier.py
"""