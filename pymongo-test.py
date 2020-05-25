from pymongo import MongoClient
import datetime
import logging
from logging import handlers
from us_states import regions, state_list

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

def drop_bulk_db(pattern2drop):
    # example: pattern2drop == 'intro-mongodb-testing"
    dbnames = client.list_database_names()
    for each in dbnames:
        if pattern2drop in each:
            print(each)
            client.drop_database(each, session=None)
            

# region example : state or county, e.g. California
threshold = ['10k', '>50k','>100k'] # threshold for alert
time_interval = ['24', '12', '6'] # check very 6,12, or 24 hrs
username = 'testuser'
user_id = '1234234324'
###### 


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
mongo_url = 'mongodb://localhost:27017'
client = MongoClient('localhost', port=27017)
db=client.admin

# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#print(serverStatusResult)
db = client.pymongo_test



# capture data
# username, 
# telegram_user_id,
# Time_interval (check 24, 12, or 6 hrs) (ask user)
# Threshold (10k, >50k, >100k) (ask user)
# Region (region, state or county #)
# ===================
# Timezone (optional)

