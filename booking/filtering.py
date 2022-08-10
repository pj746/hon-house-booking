from tkinter.tix import Tree
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver # Enable for typing for auto-completion
import time
from booking.booking import Booking

class Filtering:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def reminder(self):
        self.driver.execute_script("window.open('');")
        self.driver.implicitly_wait(3)  # It takes time to open a new tab!
        self.driver.switch_to.window(self.driver.window_handles[1])
        # self.driver.get(r'C:\Users\wpp_1\Documents\Codes\housing_scrap\housing\booking_bot\booking\bingo.html')
        self.driver.get(r'https://api.letserver.run/message/info?token=cbm8nigjn874h62h4uog&msg=有房啦！')
        self.driver.execute_script("window.open('');")
        self.driver.implicitly_wait(3)
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.driver.get(r'http://api.callmebot.com/start.php?user=@Kazan1832&text=The+house+is+leasing&lang=en-GB-Standard-B&rpt=5&cc=yes&timeout=100')

    def wait_and_close(self):
        if self.driver.test == True:
            self.driver.implicitly_wait(15)
        else:
            time.sleep(60)
        wind_num = len(self.driver.window_handles)
        for i in range(1,wind_num):
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.close()
        self.driver.switch_to.window(self.driver.search_window)

    def bingo(self):
        self.reminder()
        self.wait_and_close()

    def react_bingo(self,location_box,book):
        status0 = False
        max_retry = 0
        times = 2
        done = False
        while max_retry <times:
            try:
                location_box.click()
                self.driver.implicitly_wait(5)
                self.bingo()
                time.sleep(15)
                book.fill_form()
                status0 = True
                break
            except Exception:
                max_retry += 1
                self.driver.switch_to.window(self.driver.search_window)
        return status0

    def filter_rooms(self):
        location_boxes = self.driver.find_elements(By.XPATH,f"//*[contains(text(), 'Single') or contains(text(), 'Friends')]")
        locations = [location_box.text for location_box in location_boxes]
        price_boxes = self.driver.find_elements(By.XPATH,f"//*[contains(text(), '€ / Monat')]")
        prices= [int(price_box.text[:3]) for price_box in price_boxes if 'Kurzzeitmiete' not in price_box.text]
        date_boxes = self.driver.find_elements(By.XPATH,f"//*[contains(text(), ' frei ab')]")
        dates= [date_box.text[8:] for date_box in date_boxes]
        days=[int(date[:2]) for date in dates]
        months=[date[4:7] for date in dates]
        status = False
        try:
            assert len(locations) == len(prices)
            assert len(locations) == len(dates)
        except Exception:
            return status
        if self.driver.test:
            book = Booking(self.driver)
            for i in range(len(locations)):
                if ('Alfred-Jung' in locations[i]) & (prices[i] <= 799) & (('Aug' in months[i]) | ('Sep' in months[i])):
                    status = self.react_bingo(location_boxes[i],book)
                elif ('Wedding' in locations[i]) & (prices[i] <= 680) & (('Aug' in months[i]) | ('Sep' in months[i])):
                    status = self.react_bingo(location_boxes[i],book)
                elif ('Hanielweg' in locations[i]) & (prices[i] <= 450) & (('Aug' in months[i]) | ('Sep' in months[i])):
                    status = self.react_bingo(location_boxes[i],book)
        else:
            for i in range(len(locations)):
                book = Booking(self.driver)
                if ('Brunnen' in locations[i]) & (prices[i] <= 450) & (('Aug' in months[i]) | ('Sep' in months[i])):
                    status = self.react_bingo(location_boxes[i],book)
                elif ('Walther-May' in locations[i]) & (prices[i] <= 450) & ('Sep' in months[i]):
                    status = self.react_bingo(location_boxes[i],book)
                elif ('Haul-Hertz' in locations[i]) & (prices[i] <= 450) & ('Sep' in months[i]):
                    status = self.react_bingo(location_boxes[i],book)
                elif (('Ernst' in locations[i]) & ('Friends' in locations[i])) & (prices[i] <= 750) & (('Aug' in months[i]) | ('Sep' in months[i])):
                    status = self.react_bingo(location_boxes[i],book)
                else:
                    print('No suitable result. Search again')
        return status