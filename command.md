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

alias actenv='source /usr/local/share/macroproject/local/bin/activate'
cd /usr/local/share
source macroproject/local/bin/activate
deactivate

### git

token
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

### tmux

# 새로운 세션 생성

tmux new -s (session_name)

# 세션 만들면서 윈도우랑 같이 생성

tmux new -s (session_name) -n (window_name)

# 세션 종료

exit

# 세션 목록

tmux ls

# 세션 다시 시작하기(다시 불러오기)

tmux attach -t session_number

# 세션 중단하기

(ctrl + b) d

# 스크롤하기

ctrl + b + [

# 특정 세션 강제 종료

tmux kill-session -t session_number
