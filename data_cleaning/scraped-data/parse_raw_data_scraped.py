import json

def parse_mensa_files(file_name, days):
    weeks = []
    attempted = 0
    success = 0
    failed = 0
    
    file_path = f'raw-data/{file_name}.json-lines'
    with open(file_path, "r") as file:
        for line in file:
            week = json.loads(line)
            weeks += [week]
    
    i = 0
    for week in weeks:
        i += 1
        for day in week:
            try:
                date, menu = day
            except:
                failed += 1
                #print(f"Failed date/menu categorization in {i}th row: {day}")
                continue

            for dish in menu:
                attempted += 1
                try:
                    einrichtung, name, [price_stud, price_fac, price_guest], category_list = dish 
                except:
                    failed += 1
                    #print(f"Failed dish categorization in {i}th row: {dish}")
                    continue
    
                if einrichtung not in ["Cafeteria", "Mensa"]:
                    failed += 1
                    #print(f"Einrichtun in {i}th not Cafeteria or Mensa")
                    continue
                
                success += 1
                location = file_name
                mensa = True if einrichtung == 'Mensa' else False
                days += [[location, date, mensa, name, price_stud.replace(",",".").replace(" €",""), price_fac.replace(",",".").replace(" €",""), price_guest.replace(",",".").replace(" €",""), category_list]]
    return attempted, success, failed
