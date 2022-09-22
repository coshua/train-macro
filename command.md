### Heroku cli

# heroku ps

current status of application

# heroku ps:scale macro=1

launch a macro runner

# heroku logs --tail

view recent logs

## 환경변수

# heroku config

# heroku config:set 변수=값

# heroku config:get 변수

### django

# python manage.py runserver

runserver

### VM

129.154.51.199

# access VM

ssh -i C:\Users\bitle\.ssh\ssh-key-macro.key ubuntu@129.154.51.199
password: elwpdl

# switch to root

su - root

alias macro='cd /usr/local/share/train-macro'

# virtualenv

cd /usr/local/share
source macroproject/local/bin/activate
deactivate

### git

token
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
