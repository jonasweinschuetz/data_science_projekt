import requests
from datetime import date, timedelta
import time

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def print_meals(canteen_id, start_date_t, end_date_t): # dates as 3-tuples (day,month,year)
    start_day, start_month, start_year = start_date_t
    end_day, end_month, end_year = end_date_t

    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)
    
    for day in daterange(start_date, end_date):
        date_string = str(day)
        meals_url = f"http://openmensa.org/api/v2/canteens/{canteen_id}/days/{date_string}/meals"
        time.sleep(0.5)
        try:
            menu = requests.get(meals_url).json()
            print(menu)
        except:
            print(str(day))

def print_canteens():
    canteens = get_canteens()
    for canteen in canteens:
        print(canteen)

def get_canteens(): # retzrns list of canteen dictionaries
    url = 'http://openmensa.org/api/v2/canteens/'
    canteens = requests.get(url).json() # json of all tracked canteens
    return canteens

input("Show list of all canteens")
print_canteens()
input("Show all dishes of 2023 for firt canteen")
canteens = get_canteens()
mensa = canteens[0] 
print(mensa)
m_id = mensa["id"]
print_meals(m_id, (1,1,2023), (1,1,2024))













