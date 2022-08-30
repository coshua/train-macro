# 220811

run a sample APScheduler
looking for a setup on Heroku
1st attempt to deploy on Heroku - crashed due to different environment settings

# 220812

building a simple Django project
adding features on Macro so it can display tickets conferred to users, or else.

# 220816

/state parses current ticket list and displays
need to find a logic to find seat recursively with scheduler

# 220819

deployed to Heroku

todo

need to implement Singleton pattern

# 220822

Solution 1: Manage everything on Scheduler.py and only export set_func to other modules, no class.

Handled with Solution 1, now is able to pass TrainTicketMacro func to Scheduler on app initialization.

# 220823

Important: exception handling, informative logs
added comments for TrainTicketMacro functions

Error:
Scheduler ids are different

Todo:
how to remove job upon specific return value

# 220825

parsing python list to js list for setting up reservation with a button click.

Todo:
how to remove job upon specific return value; from event listener?
button submit form for reservation

# 220829

Added event listener so Scheduler can remove job if it succeeded its goal
Todo: reservation confirmation alert is not dismissed properly
Find alternative trip if not possible to find a ticket for entire trip
@searchforTrain, @searchforSeatandConfirm

# 220830

Applied python docstring for annotation
Todo: find alternative trip
