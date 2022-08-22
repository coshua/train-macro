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
