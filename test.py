from telethon import TelegramClient, events, Button
import yaml
import logging
from power_data import get_state_data, get_top5data, get_region_data

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

@client.on(events.CallbackQuery(data=b'clickme'))
async def callback(event):
    print(event.data)
    await event.edit('Thank you for clicking {}!'.format(event.data))

@client.on(events.NewMessage(pattern='(?i)/start', forwards=False))
#@client.on(events.NewMessage(incoming=True))
async def new_handler(event):
    if 'hello' in event.raw_text:
        # await event.reply('respond - hi!')
        await client.send_message(event.sender_id, 'A single button, with "clickme" as data',
                        buttons=Button.inline('Click me', b'clickme'))
    else:
        await client.send_message(event.sender_id, 'Welcome to PowerOutage.US watcher bot')
  
#@client.on(events.NewMessage)
@events.register(events.NewMessage(incoming=True, outgoing=False))
async def handler(event):
    print(event.raw_text)
    if '/alerts' in event.raw_text:
        await client.send_message(event.sender_id, 'Get Updates', buttons=[
            Button.text('Top 5 Outages', resize=True, single_use=True),
            Button.text('Regional Outages', resize=True, single_use=True),
            Button.text('>100k Outages (Red Alert)', resize=True, single_use=True)
        ])
    elif 'Top 5 Outages' in event.raw_text:
        #msg = "<b>html header</b>"
        msg = get_top5data()
        print(msg.text)
        await client.send_message(event.sender_id, msg.text)
    elif 'Regional Outages' in event.raw_text:
        msg = get_region_data()
        print(msg.text)
        await client.send_message(event.sender_id, msg.text)
    elif '>100k Outages (Red Alert)' in event.raw_text:
        msg = "<b>placeholder text</b>"        
        await client.send_message(event.sender_id, msg)
                

@client.on(events.InlineQuery)
#@events.register(events.InlineQuery)
async def inlinehandler(event):
    builder = event.builder
    # Two options (convert user text to UPPERCASE or lowercase)
    await event.answer([
        builder.article('UPPERCASE', text=event.text.upper()),
        builder.article('lowercase', text=event.text.lower()),
    ])

client.start(bot_token=TOKEN)

with client:
    client.add_event_handler(handler)
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()

# @client.on(events.NewMessage(chats=inbounds))
#   Button.request_location('Send location', resize=True, single_use=True)

"""
Power levels

10k - 50k Outages  (Yellow Alert)
50k - 100k Outages (Orange Alert)
>100k Outages (Red Alert)

Example code: https://github.com/LonamiWebs/Telethon/blob/master/telethon_examples/replier.py
"""