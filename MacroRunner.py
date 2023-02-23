from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time
import datetime
import os, sys

# Local imports
from helpercode.TrainTicketMacro import Ticketing
from helpercode.Scheduler import Scheduler
from helpercode.Notification import Notification
import config

updater = Updater(token=config.TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
TELEGRAM_CHAT_ID = 5794019445

app = Ticketing()
sc = Scheduler()

dispatcher.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"Macro Runner just has been set up")

def login(update: Update, context):
    driver_name = context.args[0] if context.args else "dj"
    res = app.login(driver_name, config.TMO_ID, config.TMO_PASSWORD)
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

# supposed to receive message at 11:58
def login_and_run(update: Update, context):
    date, numofTrain, depart, dest, driver_name, task_name = context.args
    res = app.login(driver_name, config.TMO_ID, config.TMO_PASSWORD)
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

    app.openRequestWindow(driver_name)
    
    execution_date = datetime.datetime.strptime(context.args[0], "%Y-%m-%d")
    execution_date += datetime.timedelta(hours=12, days=-2)

    res = sc.search_and_find(app.searchforTrainThenFind, ([date, numofTrain, depart, dest, driver_name]), execution_date, task_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

def set_macro(update: Update, context):
    next_run_time = datetime.datetime.now()
    two_days_before = datetime.datetime.strptime(context.args[0], "%Y-%m-%d")
    two_days_before += datetime.timedelta(hours=12, days=-2)
    next_run_time = two_days_before
    print(f"next run time is {next_run_time}")
    print(f"Current time is {datetime.datetime.now()}")
    res = sc.setup_ticketing(app.findSeatRecursively, (context.args[:5]), int(context.args[5]), next_run_time, context.args[6])
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

def kill_macro(update: Update, context):
    res = sc.kill_scheduler(context.args[0])
    context.bot.send_message(chat_id=update.effective_chat.id, text=res) 

def get_ticketinfo(update: Update, context):
    driver_name = context.args[0] if context.args else "dj"
    res = app.displayTicketStatus(driver_name)
    text = "\n".join([" ".join(ticket[:-1]) for ticket in res])
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def get_active_jobs(update: Update, context):
    res = sc.get_active_jobs()
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

def kill_drivers(update: Update, context):
    res = app.killDrivers()
    sc.kill_every_scheduler()
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

dispatcher.add_handler(CommandHandler('login', login))
dispatcher.add_handler(CommandHandler('set', set_macro))
dispatcher.add_handler(CommandHandler('loginrun', login_and_run))
dispatcher.add_handler(CommandHandler('kill', kill_macro))
dispatcher.add_handler(CommandHandler('tickets', get_ticketinfo))
dispatcher.add_handler(CommandHandler('tasks', get_active_jobs))
dispatcher.add_handler(CommandHandler('clear', kill_drivers))

if __name__ == "__main__":
    id = config.TMO_ID
    password = config.TMO_PASSWORD
    driver_name = "dj"

    #app.login(driver_name, id, password)
    next_run_time = datetime.datetime(2022, 10, 6, 14, 1)
    next_run_time = datetime.datetime.now()
    login_time = next_run_time - datetime.timedelta(minutes = 2)
    #sc.setup_login(app.login, ("dj", "22-76013374", "gangn10!"), login_time, "login before macro")
    #sc.setup_ticketing(app.findSeatRecursively, ("2022-10-14", "#058", "동대구", "서울", driver_name), 60, next_run_time, "test macro")
    updater.start_polling()
    updater.idle()
    while True:
        pass