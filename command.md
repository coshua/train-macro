### VM

129.154.51.199

# access VM

ssh -i C:\Users\bitle\.ssh\ssh-key-macro.key ubuntu@129.154.51.199
password: elwpdl

# reboot VM

shutdown -r

# switch to root

su - root
vi ~/.bashrc

alias macro='cd /usr/local/share/train-macro'

# virtualenv

alias envtmo='source /usr/local/share/macroproject/local/bin/activate'
alias envmovie='source /usr/local/share/movie/local/bin/activate'

deactivate

### git

token
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

git push github master

bash 에서
git add .
git pull

git log --oneline
git revert 12741e5

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

### 파일 관리

# display the file content

cat filename

# edit file content

vi filename

편집
i esc :wq
