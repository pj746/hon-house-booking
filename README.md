
# Booking bot for accommodation

## Overview
This is the script I used for booking the student accommodation at Home-in-Berlin. The script is based on `selenium`, which can
- refrash the page automatically;
- crawl the information of the rooms when they're released;
- filter the room with certain condictions;
- remind the user when a suitable room is available by WeChat/ Teltgram/ Whatsapp;
- book the room automatically (still not quite stable).

## How to use
To run the script, try
`python3 run.py`,
and keep the script running from 9am to 5pm.

### Reminder
To set up the token for reminding on WeChat:
a. search 'server饭' on WeChat and acquire a token for your WeChat account.
b. replace your token between the two `=` [here](https://github.com/pj746/hon-house-booking/blob/8d3b9ce0c0130daa576b428277e84bfcd5419a5a/booking/filtering.py#L16).

To setup the token for reminding on WhatsApp/Telegram/text message:
a. Connect your account to the [CallMeBot](callmebot.com)
b. Replace your username after `user=` [here](https://github.com/pj746/hon-house-booking/blob/8d3b9ce0c0130daa576b428277e84bfcd5419a5a/booking/filtering.py#L20).

### Filtering the rooms and booking automatically
To add filters, modify the condictions [here](https://github.com/pj746/hon-house-booking/blob/8d3b9ce0c0130daa576b428277e84bfcd5419a5a/booking/filtering.py#L56-L93).

Once the scraper get the suitable room, it may help you to book it automatically, though the function is still not stable. To fill out your information and book the room, you need modify the information in the `try_fill()` of `booking.py`.

### Test the code
To test and see if the script function well, comment out the line 1-24 of `run.py` and uncomment the last four line. This enables testing the reminding function. Mind your filter condictions if you are only testing the reminder.
