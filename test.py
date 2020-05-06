from telethon import TelegramClient, events, Button
import yaml
import logging
from power_data import get_state_data, get_top5data, get_region_data
from us_states import is_state_value, two_letter_state, states

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

#####
@client.on(events.CallbackQuery(data=b'clickme'))
async def callback(event):
    print(event.data)
    await event.edit('Thank you for clicking {}!'.format(event.data))

@client.on(events.NewMessage(incoming=True, outgoing=False))    
async def new_handler(event):
    if 'hello' in event.raw_text:
        # await event.reply('respond - hi!')
        await client.send_message(event.sender_id, 'A single button, with "clickme" as data',
                        buttons=Button.inline('Click me', b'clickme'))
#####


@client.on(events.NewMessage(pattern='(?i)/start', forwards=False, outgoing=False))
async def new_handler(event):
    await client.send_message(event.sender_id, 'Welcome to PowerOutage.US watcher bot\n\n/outages - outages by region\n/state california - get state data \n/alerts - setup alerts ')


@client.on(events.NewMessage(pattern='(?i)/state', incoming=True, outgoing=False))
async def state_handler(event):
    try:
        print(f'state handler')
        input = str(event.raw_text).lower().split(" ")
        print(input[1])
        if len(input[1]) == 2:
            state_name = two_letter_state(input[1])
            msg = get_state_data(state_name)
            await client.send_message(event.sender_id, msg)
                  
        elif len(input[1]) > 0:
            result = is_state_value(input[1])
            if result:
                msg = get_state_data(input[1])
                print(msg)
                await client.send_message(event.sender_id, msg)
            else:
                await client.send_message(event.sender_id, 'Not a State or not found. Please give a valid state.')
    except Exception as e:
            await client.send_message(event.sender_id, 'Not a State or not found. Please give a valid state.')
        
        

@events.register(events.NewMessage(incoming=True, outgoing=False))
async def handler(event):
    print("outages:")
    print(event.raw_text)
    if '/outages' in event.raw_text:
        await client.send_message(event.sender_id, 'Get Updates', buttons=[
            Button.text('Top 5 Outages', resize=True, single_use=True),
            Button.text('Regional Outages', resize=True, single_use=True),
        ])
    elif 'Top 5 Outages' in event.raw_text:
        msg = get_top5data()
        await client.send_message(event.sender_id, msg)
    elif 'Regional Outages' in event.raw_text:
        msg = get_region_data()
        await client.send_message(event.sender_id, msg)
        
                
@events.register(events.NewMessage(incoming=True, outgoing=False))
async def alerthandler(event):
    print("alert handler")
    print(event.raw_text)
    if '/alerts' in event.raw_text:
        await event.reply('Auto Notify me for the following:')

                
client.start(bot_token=TOKEN)

with client:
    client.add_event_handler(handler)
    client.add_event_handler(alerthandler)
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()


"""
Power levels
10k - 50k Outages  (Yellow Alert)
50k - 100k Outages (Orange Alert)
>100k Outages (Red Alert)

Example code: https://github.com/LonamiWebs/Telethon/blob/master/telethon_examples/replier.py
"""