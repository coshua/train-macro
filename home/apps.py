from django.apps import AppConfig
import os
from helpercode.TrainTicketMacro import Ticketing
from helpercode.Scheduler import setup_tickets_scrapping
id = "21-76066504"
password = "rhdehdwns!"
class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def hello(self):
        print('hello')
    def ready(self):
        # make sure ready() runs once
        if not os.environ.get('HOME'):
            os.environ['HOME'] = 'True'
            print('Home ready')
            app = Ticketing(id, password)
            app.login()
            setup_tickets_scrapping(app.writeTicketInfo, "update")