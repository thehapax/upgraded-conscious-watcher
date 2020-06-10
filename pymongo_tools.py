from pymongo import MongoClient, DESCENDING, ASCENDING
import datetime
import logging
from logging import handlers
from us_states import regions, state_list
import datetime as dt
from power_data import get_state_outage

# https://github.com/mongodb/homebrew-brew
# $ brew services start mongodb-community

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

# region example : state or county, e.g. California
threshold = ['10k', '50k','100k'] # threshold for alert
time_interval = ['24', '12', '6'] # check very 6,12, or 24 hrs
username = 'testuser'
user_id = '1234234324'

########################################################## 
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
mongo_url = 'mongodb://localhost:27017'
client = MongoClient('localhost', port=27017)
db=client.admin
# name of db is pymongo_test
db = client.powerwatcher
# get all posts
posts = db.posts

# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#print(serverStatusResult)

# get count of posts by user id
def get_count(userid):   
    try:
        num_alerts = posts.count_documents({'userid': userid})
        return num_alerts
    except Exception as e:
        logger.error(e)
            
# delete a document
def delete_doc(userid):
    try:
#        result = posts.delete_one({'userid': userid})
        result = posts.delete_many({'userid': userid})
        return result
    except Exception as e:
        logger.error(e)

# find a document based on criteria
def find_doc(userid):
    fmt = '%Y-%m-%d ' # %H:%M' #:%S %Z%z'
    try:
        post_string = "" # readily formatted for output to viewer
#        get_post = posts.find_one({'userid': userid})
        get_posts = posts.find({'userid': userid})
        for each_post in get_posts:
            postdate = each_post['initdate'].strftime(fmt)
            post_string = post_string +  "\n- " + each_post['region'] + ", "
            post_string = post_string + " Threshold: " + each_post['threshold'] + " every " + each_post['time_interval'] + "hrs"
            post_string = post_string + " StartDate: "  + postdate
        print(post_string)
        return post_string
    except Exception as e:
        logger.error(e)

def drop_bulk_db(pattern2drop):
    # example: pattern2drop == 'intro-mongodb-testing"
    try:
        dbnames = client.list_database_names()
        for each in dbnames:
            if pattern2drop in each:
                logger.info(each)
                client.drop_database(each, session=None)
    except Exception as e:
        logger.error(e)


def add_doc(post_one):
    # add a document
    try:
        result = posts.insert_one(post_one)
        logger.info('One post: {0}'.format(result.inserted_id))
        return result
    except Exception as e:
        logger.error(e)

# find posts by time interval
def find_by_interval(slot):
    update = posts.find({'time_interval': slot})
    return update


post_one ={
    'userid': '12345',
    'username': 'joetest',
    'time_interval': '6',
    'threshold': '10k',
    'region' :'California',
    'active' : True,
    'initdate': dt.datetime.now()
}

def construct_post(userid, username, threshold, time_interval, region):
    post ={
    'userid': userid,
    'username': username,
    'time_interval': time_interval,
    'threshold': threshold,
    'region' : region,
    'active' : True,
    'initdate': dt.datetime.now()
    }
    return post

"""
print("adding one test post")
result = add_doc(post_one)
print(result)
"""

"""
# find posts sort by ID
print("find and sort posts by id")
posts_by_id = posts.find().sort("_id", DESCENDING)
print(posts_by_id)
"""

"""
print("find posts by time interval")
entries = find_by_interval("6")
for i in entries:
    userid = i['userid']
    region = i['region']
    thres = i['threshold']
    print(f'userid: {userid}, region: {region}, thres: {thres}')

"""

for state in state_list:
    count = get_state_outage(state)
    print(f'State: {state} Outage: {count}')


"""
# get count of posts
print("get count of posts by user 'joetest'")
num = get_count('joetest')
print(num)
"""



# =====================================
# capture data
# username, 
# telegram_user_id,
# Time_interval (check 24, 12, or 6 hrs) (ask user)
# Threshold (10k, >50k, >100k) (ask user)
# Region (region, state or county #)
# ===================
# Timezone (optional)

