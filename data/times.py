import random
from datetime import datetime


# AUTO TIMES SECONDS
def random_button_time():
    time = random.randint(3600, 21600)
    return time

first_button_time = random_button_time()
restart_time = datetime.now().timestamp()
button_time = None

def dont_random_button_time():
    time = random.randint(3600, 3601)
    return time

dont_first_button_time = dont_random_button_time()
dont_restart_time = datetime.now().timestamp()
dont_button_time = None

auto_message_time = 14400

# COUNTDOWN
countdown_time = datetime(2023, 9, 7, 12, 00, 00)
countdown_title = "Xchange launch"
countdown_desc = "https://app.x7.finance"

# LAUNCH DATES
x7m105 = datetime(2022, 8, 13, 13, 10, 17)
migration = datetime(2022, 9, 25, 4, 0, 11)

burn_increment = 100
