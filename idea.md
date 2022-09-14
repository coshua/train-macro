## 최적화

element value 직접 바꿔서 진행할수 있는 내용
pageLoadStrategy

# 성능표

조회부터 신청
default ~ 10s
headless ~ 7.7s
options.page_load_strategy = 'eager' ~ 7.7s

## 지식

신청 - 취소 - 잔여석으로 예약

## 추가구현

현재표, 취소표, 스케쥴러 셋업되어있는 표 확인 기능
timestamp
에러, 성공 로그
기능별 성능 로그
GUI pyqt5
폰, 태블릿에서 신청 예약
히로쿠에서 돌리기
두 구간으로 예약

# 알림

배정 결과 (1차 배정-미배정 2차 배정-성공)
잔여석 성공

## 오류

창원중앙역이 dropdown 에서는 창중으로 뜸, 하드코딩
날짜 변경 안된상태에서 elements 찾을 가능성 (해당 날짜가 다른 기차 목록 불러올경우 에러 발생)
인터넷 안될때
플로우 고장났을때
서버에서 시간대 맞을지
