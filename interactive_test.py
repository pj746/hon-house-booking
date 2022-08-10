# %%
import os
# os.chdir('booking_bot')
from booking.searching import Searching
inst = Searching(test=True)
# print('\ntest')
# sys.stdout.flush()
inst.land_first_page()
# import pdb; pdb.set_trace()
inst.first_search(date=1)
# inst.get_prices()
# %%
from booking.filtering import Filtering
filter = Filtering(inst)
# %%
filter.bingo()
# %%
filter.filter_rooms()

# %%
from selenium.webdriver.common.by import By
location_boxes = filter.driver.find_elements(By.XPATH,f"//*[contains(text(), 'Single') or contains(text(), 'Friends')]")
locations = [location_box.text for location_box in location_boxes]
price_boxes = filter.driver.find_elements(By.XPATH,f"//*[contains(text(), '€ / Monat')]")
prices= [int(price_box.text[:3]) for price_box in price_boxes if 'Kurzzeitmiete' not in price_box.text]
date_boxes = filter.driver.find_elements(By.XPATH,f"//*[contains(text(), ' frei ab')]")
dates= [date_box.text[8:] for date_box in date_boxes]
days=[int(date[:2]) for date in dates]
months=[date[4:7] for date in dates]
status = False

# %%
from selenium.webdriver.common.by import By
from booking.booking import Booking
book = Booking(inst)
book.fill_form()
# %%
