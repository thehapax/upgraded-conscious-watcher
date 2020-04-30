from telethon import TelegramClient, events
import yaml

path  = "./"
config_file = path + 'config.yml'
with open(config_file, 'rb') as f:
    config = yaml.safe_load(f)

##### single outbound stream ######
outbound = config['outbound']
print(f'Outbound Feed: {outbound}')

inbounds = config['inbound_streams']
print(f'Inbound Feeds: {inbounds}')

client = TelegramClient(config["session_name"], 
                        config["api_id"], 
                        config["api_hash"])


@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')


@client.on(events.NewMessage(chats=inbounds))
async def event_two(event):
    await client.send_message(outbound, 'Cool! Hello, myself!')
    
client.start()
client.run_until_disconnected()