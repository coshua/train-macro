from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
import time
from helpercode.Scheduler import Scheduler
import datetime
import os
path = None
url = 'http://dtis.mil.kr/internet/dtis_rail/index.public.jsp'
id = "21-76066504"
password = "rhdehdwns!"
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.page_load_strategy = 'normal'

if os.environ.get("GOOGLE_CHROME_BIN"):
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--no-sandbox")
    path = os.environ.get("CHROMEDRIVER_PATH")
else:
    path = r'C:\Users\bitle\Downloads\chromedriver_win32\chromedriver.exe'

class Ticketing():
    start_time, end_time = 0, 0
    id, password = "", ""
    def __init__(self, id, password):
        self.driver = webdriver.Chrome(executable_path=path, chrome_options=options)
        self.driver.get(url)
        self.id, self.password = id, password
        while self.driver.title == "":
            time.sleep(0.1)
            self.driver.get(url)
        # self.driver.maximize_window()

    def login(self): 
        try:
            category_element = wait(self.driver, 2).until(lambda d: d.find_element(By.ID, "military"))
            category_dropdown = Select(category_element)
            category_dropdown.select_by_index(2)

            self.driver.find_element(By.ID, "sId").send_keys(self.id)
            self.driver.find_element(By.ID, "sPw").send_keys(self.password + Keys.ENTER)
        except:
            # already logined
            pass
    
    def hello(self, job_id, cnt):
        print("hello")
    def openRequestWindow(self):
        # wait(self.driver, 5).until(lambda d: d.find_element(By.ID, "menu_btn_001")).click()
        # wait(self.driver, 5).until(lambda d: d.find_element(By.ID, "chk_bx1"))
        # for i in range(9):
        #     self.driver.find_element(By.ID, "chk_bx" + str(i + 1)).click()
        # wait(self.driver, 3).until(expected_conditions.alert_is_present())
        # # unexpected error using following
        # # wait.until(lambda d: d.expected_conditions.alert_is_present())
        # alert = self.driver.switch_to.alert
        # alert.accept()
        # wait(self.driver, 3).until(lambda d: d.find_element(By.ID, ("btnApply")))
        # self.driver.execute_script("document.getElementById('btnApply').style.visibility = 'visible';")
        # self.driver.find_element(By.ID, "request").click()
        self.driver.get("http://dtis.mil.kr/internet/dtis_rail/WSCWWMLPTEmbrktnAppMgtTF.public.jsp")
    
    def searchforDates(self, dateFrom, dateTo):
        self.start_time = time.time()
        wait(self.driver, 5).until(lambda d: d.find_element(By.ID, "toDt"))
        self.driver.execute_script(f'document.getElementById("fromDt").value = "{dateFrom}";')
        self.driver.execute_script(f'document.getElementById("toDt").value = "{dateTo}";')
        self.driver.execute_script("srch();")
    
    # 기차 목록에서 신청하려는 기차를 찾고 해당 기차의 예약 페이지를 연다
    # return -1 오류가 있다면
    # return 0 해당 기차를 찾고 페이지를 켰다면
    # return 1 이미 배정받은 좌석이 있다면
    def searchforTrain(self, numofTrain):
        try:
            wait(self.driver, 5).until(lambda d: d.find_element(By.CSS_SELECTOR, ("table#request_table > tbody > tr > td > input[name='main_lst_trainnam']")))
            train_list = self.driver.find_elements(By.CSS_SELECTOR, ("table#request_table > tbody > tr > td > input[name='main_lst_trainnam']"))
            matching_train_idx = 0
            for i in range(len(train_list)):
                if train_list[i].get_attribute("value") == numofTrain:
                    matching_train_idx = i + 1
                    break
            if not matching_train_idx:
                print(f"There is no train {numofTrain}")
                return -1  
            else:
                isAssigned = wait(self.driver, 5).until(lambda d: d.find_element(By.CSS_SELECTOR, (f"table#request_table > tbody > tr:nth-child({matching_train_idx}) > td:nth-child(2) > a")))
                if isAssigned.get_attribute("innerText") == "배정완료":
                    print("이미 배정받은 좌석이 있습니다")
                    return 1
                request_button = wait(self.driver, 3).until(lambda d: d.find_element(By.CSS_SELECTOR, (f"table#request_table > tbody > tr:nth-child({matching_train_idx}) > td:nth-child(3) > a")))
                request_button.click()
                # wait(self.driver, 5).until(lambda d: d.find_element(By.CLASS_NAME, ("open_199")))
                # self.driver.find_element(By.CSS_SELECTOR, (f"table#request_table > tbody > tr:nth-child(1) > td:nth-child(3) > a")).click()
                # for id in matching_train_idx:
                #     matching_train_list.append(self.driver.find_element(By.CSS_SELECTOR, (f"table#request_table > tbody > tr:nth-of-type(0) > td:nth-child(3)")))
                # print("matching number is " + len(matching_train_list))
                # matching_train_list[0].click()
                
                self.driver.find_element(By.ID, "close_btn").click()
                return 0
        except Exception as e:
            print(e)

    # return True if reservation succeeded
    def searchforSeatandConfirm(self, departStation, destStation):
        try:
            click_condition = []
            # for converting station to int, so find out available interval
            stations_idx = {}
            # store longest trip available within your depart and destination
            # in case there is no trip getting on and off at exact station
            longest_available_inverval = [100, -1]
            reserved = False
            while len(click_condition) < 2:
                click_condition = self.driver.find_elements(By.CSS_SELECTOR, ("select#rmndr_sstation > option"))
                time.sleep(0.1)
            for i in range(1, len(click_condition)):
                stations_idx[click_condition[i].get_attribute("innerText")] = i
                if click_condition[i].get_attribute("innerText") == "창중":
                    stations_idx["창원중앙"] = i   
            seat_list = self.driver.find_elements(By.CSS_SELECTOR, (f"table#popup_table_01 > tbody:nth-child(2) > tr"))
            for i in range(len(seat_list)):
                seat_info = seat_list[i].get_attribute("innerText").split()
                if stations_idx[seat_info[2][:-1]] <= stations_idx[departStation] and stations_idx[seat_info[3][:-1]] >= stations_idx[destStation]:
                    self.driver.execute_script(f"setInfo({i})")
                    # seat_list[i].click()

                    # dropdown 에서 원하는 승하차역으로 변경
                    depart_dropdown_element = self.driver.find_element(By.ID, ("rmndr_sstation"))
                    depart_dropdown = Select(depart_dropdown_element)
                    depart_dropdown.select_by_index(stations_idx[departStation])
                    destination_dropdown_element = self.driver.find_element(By.ID, ("rmndr_estation"))
                    destination_dropdown = Select(destination_dropdown_element)
                    destination_dropdown.select_by_index(stations_idx[destStation])

                    self.driver.execute_script("rmndrSeatRsvtn();")
                    self.end_time = time.time()
                    reserved = True
                    # 알림창: 신청하시겠습니까?
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    break
                    # alert = self.driver.switch_to.alert
            if not reserved:
                print("예약 가능한 좌석이 없습니다.")
            return reserved
        except Exception as e:
            print(e)
    
    # 현재 신청, 확정된 승차권 정보 반환
    def displayTicketStatus(self):
        self.driver.get("http://dtis.mil.kr/internet/dtis_rail/milTrnTicktPrnt.public.jsp")
        ticket_list = self.driver.find_elements(By.CSS_SELECTOR, "table#request_table > tbody > tr")
        ticket_info = []
        for i in ticket_list:
            cols = i.get_attribute("innerText").split("\t")
            cur_ticket = []
            # 호차, 좌석, 배정여부, 날짜, 열차번호, 승차역, 하차역
            col_array = [1, 2, 3, 4, 5, 15, 16]
            for i in col_array:
                cur_ticket.append(cols[i])
            ticket_info.append(cur_ticket)
        ticket_info.sort(key=lambda lst: lst[3])
        return ticket_info[:-1]

    # 현재 신청 ,확정된 승차권 정보 ../static/tickets.txt 에 저장.
    # 첫줄 시간정보, 이후 한줄씩 티켓 정보
    def writeTicketInfo(self):
        print("Writing ticket info on /static/tickets.txt")
        try:
            ticket_list = self.displayTicketStatus()
            filename = os.path.join(os.path.dirname(__file__), os.pardir, 'static', 'tickets.txt')
            f = open(filename, 'w', encoding="UTF-8")
            f.write(datetime.datetime.now().strftime('%B %d, %a %X'))
            for ticket in ticket_list:
                f.write('\n')
                f.writelines('|'.join(ticket))
            f.close()
            print("Finished updating current ticket result")
        except Exception as e:
            print("Error on func writeTicketInfo")
            print(e)

    def findSeatRecursively(self, date, numofTrain, departStation, destStation):
        self.openRequestWindow()
        self.searchforDates(date, date)
        isAssigned = self.searchforTrain(numofTrain)
        if isAssigned == 0:
            self.searchforSeatandConfirm(departStation, destStation)
        return isAssigned

dateFrom, dateTo = "2022-08-17", "2022-08-17"
def process():
    print("Ticketing running")
    app = Ticketing()
    app.login(id, password)
    app.openRequestWindow()
    app.searchforDates(dateFrom, dateTo)
    isSeatOpen = app.searchforTrain("#127")
    #잔여석 열리는 시간보다 일찍 들어갔을때 재시도
    while not isSeatOpen:
        print("해당 열차는 현재 잔여석 예약이 불가능합니다.")
        app.searchforDates(dateFrom, dateTo)
        isSeatOpen = app.searchforTrain("#127")
    app.searchforSeatandConfirm("서울", "수원")
    print("Ticketing finished")
    print("Time passed ", app.end_time - app.start_time)
    app.driver.quit()
if __name__ == "__main__":
    app = Ticketing(id, password)
    app.login()
    app.openRequestWindow()
    app.searchforDates(dateFrom, dateTo)
    isSeatOpen = app.searchforTrain("#025")
    # app.openRequestWindow()
    # app.searchforDates(dateFrom, dateTo)
    # isSeatOpen = app.searchforTrain("#127")
    # #잔여석 열리는 시간보다 일찍 들어갔을때 재시도
    # while not isSeatOpen:
    #     print("해당 열차는 현재 잔여석 예약이 불가능합니다.")
    #     app.searchforDates(dateFrom, dateTo)
    #     isSeatOpen = app.searchforTrain("#127")
    # app.searchforSeatandConfirm("서울", "수원")
    # print("Time passed ", app.end_time - app.start_time)
    # while True:
    #     pass