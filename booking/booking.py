from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
import time

class Booking:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def back_to_body(self):
        self.driver.find_element(By.CLASS_NAME,'cdk-overlay-container').click()

    def try_fill(self, element, string):
        assert len(element)>=2
        try:
            element[0].send_keys(string)
        except ElementNotInteractableException:
            element[1].send_keys(string)

    def try_excute(self, fn, times=2):
        max_retry = 0
        done = False
        while max_retry <times:
            try:
                self.back_to_body()
                fn
                done = True
                break
            except Exception:
                time.sleep(1)
            max_retry += 1
        return done

    def choose_lang(self):
        taal = self.driver.find_element(By.XPATH,"//mat-select[contains(@id, 'select_preferredLanguage')]")
        # try:
        taal.click()
        # except:
        #     taal[1].click()
        self.driver.implicitly_wait(0.5)
        eng = self.driver.find_elements(By.XPATH,"//mat-option/span[contains(text(), 'Englisch')]")
        try:
            eng[1].click()
        except Exception:
            eng[0].click()

    def basic_info(self):
        # fill in the name
        first_names = self.driver.find_elements(By.XPATH,"  //input[contains(@id, 'input_firstname')]")
        if len(first_names)>=2:
            self.try_fill(first_names, 'Peixuan')
        else:
            first_names[0].send_keys('Peixuan')
        
        last_names = self.driver.find_elements(By.XPATH,"  //input[contains(@id, 'input_lastname')]")
        if len(last_names)>=2:
            self.try_fill(last_names,'Wu')
        else:
            last_names[0].send_keys('Wu')

        # get birthday
        birth = self.driver.find_element(By.XPATH,"//input[contains(@title, 'Geburtsdatum')]")
        birth.click()
        default_birth_year = self.driver.find_element(By.CLASS_NAME,'mat-datetimepicker-calendar-body-active')
        year = int(default_birth_year.get_attribute('aria-label')[-4:])
        birth_year_clicks = year-1997
        previous_year = self.driver.find_element(By.CLASS_NAME,"mat-datetimepicker-calendar-previous-button")
        for _ in range(birth_year_clicks):
            previous_year.click()
            time.sleep(0.4)
        march = self.driver.find_element(By.CSS_SELECTOR,'td[aria-label="März 1997"]')
        march.click()
        march19 = self.driver.find_element(By.XPATH,"//div[contains(text(), ' 19 ')]")
        march19.click()

        # select gender
        sex = self.driver.find_element(By.XPATH,"//mat-select[contains(@id, 'select_gender')]")
        sex.click()
        fem = self.driver.find_element(By.XPATH,"//*[contains(text(), 'weiblich')]")
        fem.click()

        # select nationality
        nat = self.driver.find_element(By.XPATH,"//mat-select[contains(@id, 'select_nationalityEnumId')]")
        nat.click()
        Chi = self.driver.find_element(By.XPATH,"//*[contains(text(), 'China')]")
        Chi.click()

        # fill phone nr.
        phone_ctry_code = self.driver.find_elements(By.XPATH,"//input[contains(@id, 'input_countryCode')]")
        if len(phone_ctry_code)>=2:
            self.try_fill(phone_ctry_code,'0031')
        else:
            phone_ctry_code[0].send_keys('0031')
        
        phone = self.driver.find_elements(By.XPATH,"//input[contains(@id, 'input_phone')]")
        if len(phone)>=2:
            self.try_fill(phone,'659361714')
        else:
            phone[0].send_keys('659361714')
        
        # fill child nr.
        child = self.driver.find_elements(By.XPATH,"//input[contains(@id, 'input_amountOfChildren')]")
        if len(child)>=2:
            self.try_fill(child,'0')
        else:
            child[0].send_keys('0')

        email = self.driver.find_elements(By.XPATH,"//input[contains(@id, 'input_email')]")
        if len(email)>=2:
            self.try_fill(email,'wpp_123@live.com')
        else:
            email[0].send_keys('wpp_123@live.com')
        email2 = self.driver.find_elements(By.XPATH,"//input[contains(@id, 'input_confirmEmail')]")
        if len(email2)>=2:
            self.try_fill(email2,'wpp_123@live.com')
        else:
            email2[0].send_keys('wpp_123@live.com')

    def institution(self):
        occupation = self.driver.find_element(By.ID,'occupation')
        occupation.click()
        stu = self.driver.find_element(By.XPATH,"//div[@id= 'occupation-panel']/mat-option/span[contains(text(),'Studierende')]")
        stu.click()
        uni = self.driver.find_elements(By.XPATH,"//input[contains(@id, 'input_occupationFacility')]")
        if len(uni)>=2:
            self.try_fill(uni,'Charité – Universitätsmedizin Berlin')
        else:
            uni[0].send_keys('Charité – Universitätsmedizin Berlin')
        
        # material = self.driver.find_element(By.XPATH,"//button/span/mat-icon[contains(text(),'attach_file')]")
        # material.click()
        material = self.driver.find_element(By.XPATH,"//input[contains(@id, 'file_attachment')]")
        material.send_keys(r'C:\Users\wpp_1\Documents\Neurasmus\Charité\Admission letter Charite-Wu.pdf')

    def move_in_info(self):
        begin_date = self.driver.find_element(By.XPATH,"//div/*/mat-select[contains(@id,'plannedMoveInDate')]")
        begin_date.click()
        begin_choice = self.driver.find_element(By.XPATH,"//div[contains(@id,'select_plannedMoveInDate')]")
        begin_choice.click()

        end_year = self.driver.find_element(By.CLASS_NAME,'mat-datetimepicker-calendar-header-year')
        assert (end_year.text == '2023')
        for i in range(8):
            self.driver.find_element(By.CLASS_NAME,'mat-datetimepicker-calendar-next-button').click()
            if self.driver.find_element(By.CLASS_NAME,'mat-datetimepicker-calendar-period-button').text =='September':
                break
        self.driver.find_element(By.XPATH,"//div[contains(text(), ' 30 ')]").click()

        move_in = self.driver.find_element(By.XPATH,"//input[@title='Datum und Uhrzeit deiner Anreise']")
        move_in.send_keys('2022-09-05T14:00:00+02:00')

        self.back_to_body()

    def confirm(self, elements):
        cond0 = (elements[-6].text =='Admission letter Charite-Wu.pdf')
        cond1 = ('Aug. 2022' in elements[-5].text) | ('Sep. 2022' in elements[-5].text)
        cond2 = (elements[-4].text=='30. Sep. 2023')
        cond3 = (elements[-3].text=='06. Sep. 2022, 14:00')
        if not self.driver.test:
            cond4 = int(elements[-2].text[:4])<= 450
        else:
            cond4 = int(elements[-2].text[:4])<800
        overall = cond0 & cond1 & cond2 & cond3 & cond4
        return overall

    def finalization(self):
        checks = self.driver.find_elements(By.CLASS_NAME,'mat-checkbox-layout')
        for i in checks:
            if 'der' in i.text:
                i.click()

        agree = self.driver.find_elements(By.XPATH, "//mat-radio-button/label/span[contains(text(), ' Akzeptiert ')]")
        assert len(agree)==2
        agree[0].click()
        self.driver.find_element(By.XPATH, "//button/span/span[contains(text(), 'Ich bin damit einverstanden')]").click()
        agree[1].click()
        self.driver.find_element(By.XPATH, "//button/span/span[contains(text(), 'Ich bin damit einverstanden')]").click()

        if not self.driver.test:
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        else:
            print('Filled!')

    def fill_form(self):
        finished = False
        
        d1 = self.try_excute(self.choose_lang())
        d2 = self.try_excute(self.basic_info())
        d3 = self.try_excute(self.institution)
        d4 = self.try_excute(self.move_in_info())

        # get to the next page
        self.driver.find_element(By.XPATH,"//button/span[contains(text(), ' weiter ')]").click()
        
        # Check the information
        confirms = self.driver.find_elements(By.CLASS_NAME,'confirm-value')
        correctness = self.confirm(confirms)
        if not correctness:
            finished=True
            return finished
        else:
            d5 = self.try_excute(self, self.finalization())
            finished=d1&d2&d3&d4&d5
        return finished