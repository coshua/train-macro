### 잔여석

59분에 로그인
00분에 날짜선택, 좌석선택
여러 번 트라이 뿌림,
실패하면 다음 트라이 자동

## 로그인

def login()

## 탑승신청

def openRequestWindow()

## 날짜 선택 검색

def searchforDates(from, to)
def searchforTrain(numofTrain)

## 목록에서 특정 row 선택

def searchforSeatandConfirm(departStation, destStation)

**참고**

openpopup('open_199','RmndrSeatRsvtn','54204||20220811||0','20220811')
2, 3 번째 파라미터 getValue() 로 전달, 해당 열차 잔여 좌석 생성
54204 가 getValue 에서 p_dailymvmgtno 라는 값으로 전달된다.

### 탑승예약

# 예약신청

onclick="rsvtnApp()"
(점수는 form에 들어가지 않는다)
