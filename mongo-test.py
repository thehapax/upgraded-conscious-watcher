from us_states import regions, state_list
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField
from mongoengine import connect 
import datetime
import logging
from logging import handlers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

class Post(Document):
    username = StringField(required=True, max_length=50)
    user_id = StringField(required=True)
    region = StringField(required=True, max_length=100)
    threshold= StringField(required=True, max_length=20)
    time_interval = IntField(required=True)
    active = BooleanField()
    initdate = DateTimeField(default=datetime.datetime.now)
    
    def live_alerts(self, queryset):
        return queryset.filter(active=True)


try:
    connect('mongoengine_test', host='localhost', port=27017)
    
    alert1 = Post(username='joetest',
                    user_id='12345',
                    region='Pacific',
                    threshold='10k',
                    time_interval='6', 
                    active=True)

    print("\n")
    alert1.save()
    print(alert1.region)

except Exception as e: 
    logger.err(e)
