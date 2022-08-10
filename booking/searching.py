import os
import datetime
import time
from selenium import webdriver
import booking.constants as const
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException, ElementNotInteractableException
from booking.booking import Booking
from booking.filtering import Filtering

class Searching(webdriver.Chrome):
    def __init__(self, driver_path=r";C:\Users\wpp_1\Documents\Codes\housing_scrap", test=False):
        self.driver_path = driver_path
        self.test = test
        self.search_window = None
        os.environ['PATH'] += self.driver_path
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-gpu')
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Searching, self).__init__(chrome_options=option)
        self.implicitly_wait(5)
    
    def land_first_page(self):
        self.get(const.BASE_URL)
        self.search_window = self.current_window_handle

    def cookie_permit(self):
        try:
            cookie_ok = self.find_element(By.CLASS_NAME,'cc-btn')
            cookie_ok.click()
        except Exception:
            pass

    def click_search(self):
        try:
            try:
                start_search = self.find_element(By.CLASS_NAME,'mat-raised-button')
            except ElementClickInterceptedException:
                start_search = self.find_element(By.XPATH,'//mat-icon[contains(text(), "search")]')
            start_search.click()
        except Exception:
            pass

    def fill_move_in(self, date=1):
        try:
            who = self.find_element(By.CLASS_NAME,'mat-select-value')
            who.click()
            time.sleep(0.5)
            try:
                stu = self.find_element(By.ID,'mat-option-0')
                stu.click()
                time.sleep(1)
            except Exception:
                stu = self.find_element(By.XPATH,'//*[contains(text(), "Studierende")]')
                stu.click()
                time.sleep(0.5)
            try:
                moveindate = self.find_element(By.CSS_SELECTOR,'input[matinput]')
                moveindate.click()
                time.sleep(1)
                right_arrow = self.find_element(By.CLASS_NAME,'mat-datetimepicker-calendar-next-button')
                right_arrow.click()
                time.sleep(1)
                aug16 = self.find_element(By.XPATH,f"//div[contains(text(), ' {str(date)} ')]")
                # aug16 = self.find_element(By.XPATH,"//div[contains(text(), ' 16 ')]")
                aug16.click()
                time.sleep(1.5)
            except Exception:
                moveindate = self.find_element(By.XPATH,'//*[contains(., "mat-input-")]')
                moveindate.click()
                time.sleep(1)
                aug16 = self.find_element(By.XPATH,f"//div[contains(text(), ' {str(date)} ')]")
                # aug16 = self.find_element(By.XPATH,"//div[contains(text(), ' 16 ')]")
                aug16.click()
                time.sleep(1.5)
        except Exception:
            pass

    def first_search(self,date=16):
        self.cookie_permit()
        self.fill_move_in(date=date)
        self.click_search()
        try:
            print(self.find_element(By.ID,'offeringErrorMessage').text,flush=True)
        except NoSuchElementException:
            try:
                room = self.check_results()
                if room:
                    print("There're rooms!", flush=True)
            except NoSuchElementException:
                self.click_search()


    def finalize_the_day(self):
        self.execute_script("window.open('');")
        time.sleep(2)  # It takes time to open a new tab!
        self.switch_to.window(self.window_handles[-1])
        self.get(r'C:\Users\wpp_1\Documents\Codes\housing_scrap\housing\booking_bot\booking\stop_search.html')

    def check_results(self):
        # TODO: Add condition to the returned results
        room = self.find_element(By.CLASS_NAME,"mat-card-content")
        return room

    def return_and_search(self):
        self.switch_to.window(self.window_handles[0])
        time.sleep(30)
        self.search()

    def search(self):
        while True:
            bingo_count = 0
            try:
                room = self.check_results()
                if room:
                    status = self.get_prices()
                    if status:
                        bingo_count +=1
                        time.sleep(90)
                    self.return_and_search()
                    if bingo_count == 10:
                        break
            except NoSuchElementException:
                timeNow = datetime.datetime.now()
                today5pm = timeNow.replace(hour=17, minute=0, second=0, microsecond=0)
                today9am = timeNow.replace(hour=9, minute=0, second=0, microsecond=0)
                late = (timeNow >= today5pm) & (not self.test)
                early = (timeNow <= today9am) & (not self.test)
                # print(judgement, flush=True)
                if early:
                    time.sleep(300)
                    self.return_and_search()
                elif late:
                    self.finalize_the_day()
                    break
                else:
                    if not self.test:
                        time.sleep(3)
                    time.sleep(2)
                    self.click_search()
            else:
                break

    def get_prices(self):
        filter = Filtering(self)
        status = filter.filter_rooms()
        return status