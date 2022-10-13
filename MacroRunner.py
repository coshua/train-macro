from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time
from datetime import datetime, timedelta
import os, sys

# Local imports
from helpercode.TrainTicketMacro import Ticketing
from helpercode.Scheduler import Scheduler
from helpercode.Notification import Notification
import config

updater = Updater(token=config.TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def hello():
    print("HELLO !")

#step3./start 명령어가 입력되었을 때의 함수 정의
def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{context.args}")
    hello()
app = Ticketing()
sc = Scheduler()

def login(update: Update, context):
    res = app.login("dj", config.TMO_ID, config.TMO_PASSWORD)
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

def set_macro(update: Update, context):
    next_run_time = datetime.now()
    res = sc.setup_ticketing(app.findSeatRecursively, (context.args[:5]), int(context.args[5]), next_run_time, context.args[6])
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

def kill_macro(update: Update, context):
    res = sc.kill_scheduler(context.args[0])
    context.bot.send_message(chat_id=update.effective_chat.id, text=res) 

def get_ticketinfo(update: Update, context):
    res = app.displayTicketStatus("dj")
    text = "\n".join([" ".join(ticket[:-1]) for ticket in res])
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def get_active_jobs(update: Update, context):
    res = sc.get_active_jobs
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)
#step4.위에서 정의한 함수를 실행할 CommandHandler 정의
start_handler = CommandHandler('start', start) #('명령어',명령 함수)

#step5.Dispatcher에 Handler를 추가
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler('login', login))
dispatcher.add_handler(CommandHandler('set', set_macro))
dispatcher.add_handler(CommandHandler('kill', kill_macro))
dispatcher.add_handler(CommandHandler('tickets', get_ticketinfo))
#step6.Updater 실시간 입력 모니터링 시작(polling 개념)

if __name__ == "__main__":
    id = config.TMO_ID
    password = config.TMO_PASSWORD
    driver_name = "dj"

    #app.login(driver_name, id, password)
    next_run_time = datetime(2022, 10, 6, 14, 1)
    next_run_time = datetime.now()
    login_time = next_run_time - timedelta(minutes = 2)
    #sc.setup_login(app.login, ("dj", "22-76013374", "gangn10!"), login_time, "login before macro")
    #sc.setup_ticketing(app.findSeatRecursively, ("2022-10-14", "#058", "동대구", "서울", driver_name), 60, next_run_time, "test macro")
    updater.start_polling()
    updater.idle()
    while True:
        pass