from telethon import TelegramClient, events, sync, utils, functions, Button
import yaml
import sys
import logging

# https://docs.telethon.dev/en/latest/modules/client.html?highlight=event.message#telethon.client.messages.MessageMethods.send_message

### this script will consolidate multiple channels to one channel/group/user on telgram
# source code examples from https://docs.telethon.dev/en/latest/basic/quick-start.html
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)


path  = "./"
config_file = path + 'config.yml'
with open(config_file, 'rb') as f:
    config = yaml.safe_load(f)

client = TelegramClient(config["session_name"], 
                        config["api_id"], 
                        config["api_hash"])


def get_ids(client):
    # You can print all the dialogs/conversations that you are part of:
    for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)


def get_inbound(config):
    inbounds = config['inbound_streams']
    print(f'Inbound Feeds: {inbounds}')
    return inbounds



async def main():
    # client.start()

    # Getting information about yourself
    me = await client.get_me()
    print(me.stringify())
    username = me.username
    print(username)
    get_ids(client)
    
    # Default to another parse mode
    client.parse_mode = 'html'
    
    # Single inline button
    await client.send_message(outbound, 'A single button, with "clk1" as data',
                        buttons=Button.inline('Click me', b'clk1'))

with client:
    client.run_until_disconnected(main())


"""
    @client.on(events.CallbackQuery)
    async def callback(event):
        await event.edit('Thank you for clicking {}!'.format(event.data))


    # listen and send messsages
    @client.on(events.NewMessage(chats=inbound_groups))
    async def handler(event):
        inbound_message = event.message.raw_text
        await client.send_message(outbound, inbound_message, parse_mode='html')
"""



"""
if __name__ == "__main__":
    
    try:
        path  = "./"
        config_file = path + 'config.yml'
        with open(config_file, 'rb') as f:
            config = yaml.safe_load(f)

        # We have to manually call "start" if we want an explicit bot token
        # with actual user account
        client = TelegramClient(config["session_name"], 
                                config["api_id"], 
                                config["api_hash"])
        ##### get inbound streams ######
        inbound_groups = get_inbound(config)

        ##### single outbound stream ######
        outbound = config['outbound']
        print(f'Outbound Feed: {outbound}')
    
        with client:
            client.run_until_disconnected(main())
            
    except Exception as e:
        logger.error(e)

#    main(config)

"""
