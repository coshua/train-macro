from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
import os
from Scheduler import Scheduler

path = None
url = 'http://dtis.mil.kr/internet/dtis_rail/index.public.jsp'
id = "21-76066504"
password = "rhdehdwns!"
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.page_load_strategy = 'normal'

# configure chromedriver depends on environment
if os.environ.get("GOOGLE_CHROME_BIN"):
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--no-sandbox")
    path = os.environ.get("CHROMEDRIVER_PATH")
else:
    path = r'C:\Users\bitle\Downloads\chromedriver_win32\chromedriver.exe'

class Ticketing():
    start_time, end_time = 0, 0
    passwords = None
    drivers = None
    def __init__(self):
        # self.driver = webdriver.Chrome(executable_path=path, chrome_options=options)
        # self.driver.get(url)
        # self.id, self.password = id, password
        # while self.driver.title == "":
        #     time.sleep(0.1)
        #     self.driver.get(url)
        # self.driver.maximize_window()
        self.drivers = {}
        self.passwords = {}
        return

    def login(self, id, password):
        """
        Open ticketing site - dtis.mil.kr than login with given id and password.
        Each login is managed by different chrome driver

        Args:
            id (string): military id (22-76013374)
            password (string): password

        Returns:
            None
        """ 
        print("@login - Trying open up ticketing page")
        if id not in self.drivers:
            self.drivers[id] = webdriver.Chrome(executable_path=path, chrome_options=options)
            self.passwords[id] = password
        self.drivers[id].get(url)
        while self.drivers[id].title == "":
            time.sleep(0.1)
            self.drivers[id].get(url)
        print("@login - Ticketing page was successfully rendered")
        try:
            print(f"@login - Trying login to system for user {id}")
            category_element = wait(self.drivers[id], 2).until(lambda d: d.find_element(By.ID, "military"))
            category_dropdown = Select(category_element)
            category_dropdown.select_by_index(2)

            self.drivers[id].find_element(By.ID, "sId").send_keys(id)
            self.drivers[id].find_element(By.ID, "sPw").send_keys(password + Keys.ENTER)
            print(f"@login - ID and password was put and submitted {id}")
        except:
            # already logined
            print("@login - Already logged in to the system")
            pass
    
    def openRequestWindow(self, id):
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
        self.drivers[id].get("http://dtis.mil.kr/internet/dtis_rail/WSCWWMLPTEmbrktnAppMgtTF.public.jsp")
        print(f"@openRequestWindow - Trying open a reservation page, id: {id}")
    
    def searchforDates(self, dateFrom, dateTo, id):
        """
        Set specific dates on request window getting from #openRequestWindow

        Args:
            dateFrom (string): date from which user wants to search (2023-01-01)
            dateTo (string): date to which user wants to search (2023-01-03)
            id (string): military id (22-76013374)
        Returns:
            None
        """
        print("@searchforDates - Waiting date picker being displayed")
        self.start_time = time.time()
        wait(self.drivers[id], 5).until(lambda d: d.find_element(By.ID, "toDt")) #necessary?
        self.drivers[id].execute_script(f'document.getElementById("fromDt").value = "{dateFrom}";')
        self.drivers[id].execute_script(f'document.getElementById("toDt").value = "{dateTo}";')
        self.drivers[id].execute_script("srch();")
        print(f"@searchforDates - Run search id: {id}")

    def searchforTrain(self, numofTrain, id):
        """
        It opens a reservation page where leftover seats are displayed for given train.
        It is supposed to be executed after pulling off the exact date.

        Args:
            numofTrain (string): The identification number of the train (#025).
            id (string): military id (22-76013374)

        Returns:
            numofTicket (int): 
            Return -1 if something went wrong while trying to find the train.
            Return 0 if it finds the train and opens a page for it.
            Return 1 if it finds the train and opens a page for it, but notices there is a ticket for that train.
            Return 2 if it finds the train, but notices two tickets so it is not able to reserve more seats.
        """
        numofTicket = -1
        try:
            print(f"@searchforTrain - Looking for train {numofTrain}, id: {id}")
            wait(self.drivers[id], 5).until(lambda d: d.find_element(By.CSS_SELECTOR, ("table#request_table > tbody > tr > td > input[name='main_lst_trainnam']")))
            train_list = self.drivers[id].find_elements(By.CSS_SELECTOR, ("table#request_table > tbody > tr > td > input[name='main_lst_trainnam']"))
            matching_train_idx = 0
            for i in range(len(train_list)):
                if train_list[i].get_attribute("value") == numofTrain:
                    matching_train_idx = i + 1
                    break
            if not matching_train_idx:
                print(f"@searchforTrain - There is no train {numofTrain}, id: {id}")
                return numofTicket

            isAssigned = wait(self.drivers[id], 5).until(lambda d: d.find_element(By.CSS_SELECTOR, (f"table#request_table > tbody > tr:nth-child({matching_train_idx}) > td:nth-child(3) > a")))
            if isAssigned.get_attribute("innerText") == "2회배정":
                print(f"@searchforTrain - Train was found, but not able to get ticket as you hold two tickets for {numofTrain}, id: {id}")
                numofTicket = 2
                return numofTicket
            elif isAssigned.get_attribute("innerText") == "2회잔여석":
                print(f"@searchforTrain - Train was found, but you already have a ticket for the train {numofTrain}")
                numofTicket = 1
            else:
                print(f"@searchforTrain - Train was found {numofTrain}")
                numofTicket = 0
            request_button = wait(self.drivers[id], 3).until(lambda d: d.find_element(By.CSS_SELECTOR, (f"table#request_table > tbody > tr:nth-child({matching_train_idx}) > td:nth-child(3) > a")))
            request_button.click()         
            self.drivers[id].find_element(By.ID, "close_btn").click()
            print(f"@searchforTrain - A reservation page was opened for {numofTrain}, id: {id}")
            return numofTicket
        except Exception as e:
            print("\n!!!Error on @searchforTrain!!!")
            print(e)
            return -1

    def searchforSeatandConfirm(self, departStation, destStation, id, partial=True):
        """
        When leftover seats are open to be reserved, find available seat. It is supposed to be executed after seats open.
        
        Args:
            deparatStation (string): The name of station user departs from (동대구).
            destStation (string): The name of station user heads to (서울).
            id (string): military id (22-76013374).
            partial (bool, optional): True if it is okay to confirm a seat which travels partially.
            
        Returns:
            reserved (string): containing station names getting on and off (동대구-서울).
            Return empty string if fails to make a reservation.
        """
        try:
            print(f"@searchforSeatandConfirm - Try to finding a seat for a trip from {departStation} to {destStation}, id: {id}")
            click_condition = []
            # for converting station to int, so find out available interval
            stations_idx = {}
            # store longest trip available within your depart and destination
            # in case there is no trip getting on and off at exact station user has specified
            longest_available_inverval = [-1, -1]
            reserved = ""
            while len(click_condition) < 2:
                click_condition = self.drivers[id].find_elements(By.CSS_SELECTOR, ("select#rmndr_sstation > option"))
                time.sleep(0.1)
            
            # parsing station list of this train
            for i in range(1, len(click_condition)):
                stations_idx[click_condition[i].get_attribute("innerText")] = i
                # 창원중앙역이 list dropdown 에서 창중으로 뜬다 에러 없도록 보정
                if click_condition[i].get_attribute("innerText") == "창중":
                    stations_idx["창원중앙"] = i   
            
            # parsing all seats and find appropriate one
            seat_list = self.drivers[id].find_elements(By.CSS_SELECTOR, (f"table#popup_table_01 > tbody:nth-child(2) > tr"))
            for i in range(len(seat_list)):
                seat_info = seat_list[i].get_attribute("innerText").split()

                # 전체 구간 티켓 없을때 가장 긴 일부 구간 찾기
                if stations_idx[seat_info[3][:-1]] > stations_idx[departStation]:
                    interval = [max(stations_idx[departStation], stations_idx[seat_info[2][:-1]]), min(stations_idx[destStation], stations_idx[seat_info[3][:-1]])]
                    if interval[1] - interval[0] > longest_available_inverval[1] - longest_available_inverval[0]:
                        longest_available_inverval = interval

                # departStation 에서 승차, destStation 하차하는 자리 있다면 예매
                if stations_idx[seat_info[2][:-1]] <= stations_idx[departStation] and stations_idx[seat_info[3][:-1]] >= stations_idx[destStation]:
                    self.drivers[id].execute_script(f"setInfo({i})")
                    # seat_list[i].click()

                    # dropdown 에서 원하는 승하차역으로 변경
                    # if dropdown is not rendered when setInfo() is called, it leaves the form empty
                    # so entering information manually to prevent error
                    depart_dropdown_element = self.drivers[id].find_element(By.ID, ("rmndr_sstation"))
                    depart_dropdown = Select(depart_dropdown_element)
                    depart_dropdown.select_by_index(stations_idx[departStation])
                    destination_dropdown_element = self.drivers[id].find_element(By.ID, ("rmndr_estation"))
                    destination_dropdown = Select(destination_dropdown_element)
                    destination_dropdown.select_by_index(stations_idx[destStation])

                    self.drivers[id].execute_script("rmndrSeatRsvtn();")
                    self.end_time = time.time()
                    reserved = f"{departStation}-{destStation}"
                    # 알림창: 신청하시겠습니까?
                    alert = self.drivers[id].switch_to.alert
                    alert.accept()

                    self.openRequestWindow()
                    try:
                        time.sleep(1)
                        alert = self.drivers[id].switch_to.alert
                        alert.accept()
                    except:
                        print("@searchforSeatandConfirm - No final alert appeared")
                    print(f"@searchforSeatandConfirm - Found a seat for a trip {departStation} to {destStation} and made a reservation at", datetime.now(), f"id: {id}")
                    break
            if not reserved:
                print("예약 가능한 좌석이 없습니다.")
                self.drivers[id].find_element(By.ID, "close_btn").click()
                print(f"@searchforSeatandConfirm - There is no available seat for a trip {departStation} to {destStation}")
            return reserved
        except Exception as e:
            print("\n!!!Error on @searchforSeatandConfirm!!!")
            print(e)
    
    # fix
    # 취소표에서 구간은 처음과 끝으로 보이고 이후의 창에서 세부 구간 취소해야함
    def cancelTicket(self, operationDate, numofTrain, departStation, destStation, id):
        """
        It tries to drop off the ticket with given information.

        Args:
            operationDate (string): The date of train scheduled (2023-01-01)
            numofTrain (string): The identification number of the train (#025)
            departStation (string): The station from which this ticket is designated to depart (동대구역)
            destStation (string): The station which this ticket is designated to arrive (서울역)
            id (string): Military id (22-76013374)

        Returns:
            (bool) : True if there was a ticket matching the given information and successfully dropped it off.
            False if it fails to find such ticket.
        """
        print(f"@cancelTicket - Try cancel the ticket {numofTrain}, {departStation}-{destStation} on {operationDate}")
        self.drivers[id].get("http://dtis.mil.kr/internet/dtis_rail/milTrnBdngCancel.public.jsp")
        future_date = datetime.now() + timedelta(days=10)
        future_date = future_date.strftime('%Y-%m-%d')
        self.drivers[id].execute_script(f'document.getElementById("toDt").value = "{future_date}";')
        self.drivers[id].execute_script("srch();")
        tickets_list = wait(self.drivers[id], 5).until(lambda d: d.find_elements(By.CSS_SELECTOR, ("table#request_table > tbody > tr")))
        for i in range(len(tickets_list)):
            # 2, 5, 7, 8
            # 날짜, 열차명, 출발역, 도착역
            cols = tickets_list[i].get_attribute("innerText").split("\t")
            if cols[2] == operationDate and cols[5] == numofTrain \
            and cols[7] == departStation and cols[8] == destStation:
                self.drivers[id].find_element(By.CSS_SELECTOR, f"table#request_table > tbody > tr:nth-child({i + 1}) > td:nth-child(2) > a").click()
                return True
        return False

    # 현재 신청, 확정된 승차권 정보 반환
    def displayTicketStatus(self, id):
        print(f"@displayTicketStatus - Try open ticket state page for id: {id}")
        try:
            self.drivers[id].get("http://dtis.mil.kr/internet/dtis_rail/milTrnTicktPrnt.public.jsp")
        except Exception as e:
            print(f"@displayTicketStatus - Error while open state page, retry login id: {id}")
            print(e)
            self.login(id, self.passwords[id])
            self.drivers[id].get("http://dtis.mil.kr/internet/dtis_rail/milTrnTicktPrnt.public.jsp")
        ticket_list = self.drivers[id].find_elements(By.CSS_SELECTOR, "table#request_table > tbody > tr")
        ticket_info = []
        for i in ticket_list:
            cols = i.get_attribute("innerText").split("\t")
            cur_ticket = []
            # 호차, 좌석, 배정여부, 날짜, 열차번호, 승차역, 하차역
            col_array = [1, 2, 3, 4, 5, 15, 16]
            for i in col_array:
                cur_ticket.append(cols[i])
            # 군번
            cur_ticket.append(cols[12])
            ticket_info.append(cur_ticket)
        ticket_info.sort(key=lambda lst: lst[3])
        return ticket_info[:-1]

    # 현재 신청 ,확정된 승차권 정보 ../static/tickets.txt 에 저장.
    # 첫줄 시간정보, 이후 한줄씩 티켓 정보
    def writeTicketInfo(self):
        print("@writeTicketInfo - Writing ticket info on /static/tickets.txt")
        try:
            filename = os.path.join(os.path.dirname(__file__), os.pardir, 'static', 'tickets.txt')
            f = open(filename, 'w', encoding="UTF-8")
            f.write(datetime.now().strftime('%B %d, %a %X'))
            for each_id in self.drivers:
                ticket_list = self.displayTicketStatus(each_id)
                for ticket in ticket_list:
                    f.write('\n')
                    f.writelines('|'.join(ticket))
            f.close()
            print("@writeTicketInfo - Finished updating ticketing results")
        except Exception as e:
            print("\n!!!Error on @writeTicketInfo!!!")
            # self.driver.get(url)
            # self.login()
            print("@writeTicketInfo - Try login")
            for each_id in self.drivers:
                self.login(each_id, self.passwords[each_id])

    def findSeatRecursively(self, date, numofTrain, departStation, destStation, id):
        
        isAssigned = self.searchforTrain(numofTrain, id)
        print(isAssigned)
        if isAssigned == 0:
            self.searchforSeatandConfirm(departStation, destStation, id)
        elif isAssigned == 1:
            self.searchforSeatandConfirm(departStation, destStation, id, False)
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
    app = Ticketing()
    app.login("22-76013374", "gangn10!")
    sc = Scheduler()
    app.openRequestWindow("22-76013374")
    app.searchforDates("2022-09-23", "2022-09-23", "22-76013374")
    sc.setup_ticketing(app.findSeatRecursively, ("2022-09-23", "#126", "동대구", "서울", "22-76013374"), "18:45 macro")
    
    while True:
        pass
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