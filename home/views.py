# where does this come from?
# from turtle import pen
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from helpercode.TrainTicketMacro import Ticketing
from helpercode.Scheduler import setup_ticketing
import os
import datetime
id = "21-76066504"
password = "rhdehdwns!"

# /
# ../static/tickets.txt 의 티켓정보 불러와서 테이블에 보여준다
# 해당 파일의 수정은 Ticketing.writeTicketInfo 에서
def init(request):
    f = open(os.path.join(os.path.dirname(__file__), os.pardir, 'static', 'tickets.txt'), encoding='UTF-8')
    pending_ticket_list = []
    while True:
        line = f.readline().strip()
        if not line:
            break
        pending_ticket_list.append(line.split('|'))
    
    currentTime = datetime.datetime.now().strftime("%B %d, %a %X")
    context = {
        'pending_ticket_list': pending_ticket_list[1:],
        'log_timestamp': pending_ticket_list[0][0],
        'current_timestamp': currentTime
        }
    return render(request, 'home/state.html', context)

# /state
# ../static/tickets.txt 의 티켓정보 불러와서 테이블에 보여준다
# 해당 파일의 수정은 Ticketing.writeTicketInfo 에서
def state(request):
    app = Ticketing(id, password)
    app.login()
    date = "2022-08-30"
    train = "#028"
    setup_ticketing(app.findSeatRecursively, (date, train, "부산", "서울"), date + train)
    f = open(os.path.join(os.path.dirname(__file__), os.pardir, 'static', 'tickets.txt'), encoding='UTF-8')
    pending_ticket_list = []
    while True:
        line = f.readline().strip()
        if not line:
            break
        pending_ticket_list.append(line.split('|'))
    
    currentTime = datetime.datetime.now().strftime("%B %d, %a %X")
    context = {
        'pending_ticket_list': pending_ticket_list[1:],
        'log_timestamp': pending_ticket_list[0][0],
        'current_timestamp': currentTime
        }
    return render(request, 'home/state.html', context)

