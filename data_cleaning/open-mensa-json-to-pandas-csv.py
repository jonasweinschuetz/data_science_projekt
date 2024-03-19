import pandas as pd
import json
from cleaning import domain, filter_vvo_tags, classify_vvo_instance_by_file
from files import list_to_file, file_to_list

def json_to_df(openmensa_path):
    
    vgn_names = set(file_to_list("Data/tags/vgn_names.txt"))
    veg_names = set(file_to_list("Data/tags/veg_names.txt"))
    meat_names = set(file_to_list("Data/tags/meat_names.txt"))
    vgn_veg_names = set(file_to_list("Data/tags/vgn_veg_names.txt"))
    meat_vgn_veg_names = set(file_to_list("Data/tags/vgn_veg_names.txt"))
    
    vgn_tags = set(file_to_list("Data/tags/vgn_tags.txt"))
    veg_tags = set(file_to_list("Data/tags/veg_tags.txt"))
    meat_tags = set(file_to_list("Data/tags/meat_tags.txt"))
    vgn_veg_tags = set(file_to_list("Data/tags/vgn_veg_tags.txt"))
    
    
    with open(openmensa_path, "r") as file:
        data_json = json.load(file)
    
    data = []
    fails = 0
    attempts = 0
    
    for mensa in data_json:
        mensa_id = mensa["canteen_id"]
        
        # meal is dictionary with the following keys ['id', 'name', 'category', 'prices', 'notes','date']
        for meal in mensa["meals"]:     
            attempts += 1
            try:
                student_price, employee_price, _ , guest_price = list(meal["prices"].values()) 
                ## ignore all meals that do not have at least one valid price:
                #if student_price == None and employee_price == None and guest_price == None:
                #    fails += 1
                #    print("Entry has no valid price in the three categories:")
                #    print(mensa_id, meal)
                #    continue

                student_price = float("nan") if student_price == None else student_price
                employee_price = float("nan") if employee_price == None else employee_price

                if guest_price == None:
                    guest_price = float("nan") 
            except:
                fails += 1
                print("Failed to retrieve prices in", mensa_id)
                print(meal)
    
            tags = list(set(meal["notes"]))     # convert to set to remove duplicates
            tags = [tag.replace("\n", " ").lower() for tag in tags]   # replace linebreaks in tags and formalize tag string to lower case

            try:
                meal_id = meal["id"]
                meal_name = meal["name"].lower()
                #print(tags)
                date = meal["date"]
            except:
                fails += 1
                print("Failed to retrieve one of the following values: meal_id, name, notes or date", mensa_id)
                print(meal)
    
            vvo_status = classify_vvo_instance_by_file(tags, meal_name, vgn_names, veg_names, meat_names, vgn_veg_names, meat_vgn_veg_names, vgn_tags, veg_tags, meat_tags, vgn_veg_tags)
            #print(meal)
            data.append((mensa_id, date, meal_id, meal_name, vvo_status, tags, student_price, employee_price, guest_price))
    
    
    features = ["mensa_id", "date", "meal_id", "meal_name", "vvo_status", "tags", "student_price", "employee_price", "guest_price"]
    
    om_data = pd.DataFrame(data, columns=features)
    om_data["date"] = pd.to_datetime(om_data["date"], format="%Y-%m-%d")

    print(f"Attempts: {attempts}")
    print(f"Successes: {100*round((attempts-fails)/attempts, 4)}% or {attempts-fails}")
    print(f"fails: {100*round(fails/attempts, 4)}% or {fails}")

    return om_data


data = json_to_df("Data/Meals All Canteens/full_all_canteens.json")
data.to_csv("Data/german-canteens(filtered).csv", sep="@")
print("Finished open-mensa-all")

#data = json_to_df("Data/path.json")
#data.to_csv("Data/path.csv", sep="@")
#print("Finished SH")
#print(data)


#data = pd.read_csv("Data/german-canteens(filtered).csv", sep="@", infer_datetime_format=True)
# evaluates tag_list as list (from string)
#data["tags"] = list(map(eval, data["tags"]))

#entry_count = len(data["tags"])
#vegan = vegetarian = 0
#
#vgn_set = set(["vegan", "Vegan", "Vegane Speisen (V*)", "Veganes Gericht", "Vegane Speisen"])
#veg_set = set(["vegetarisch", "Vegetarisch", "vegetarian", "Vegetarian", "Vegetarische Speisen (V)", "Vegetarisches Gericht", "Vegetarische Speisen"])
#
#for tag_list in data["tags"]:
#    tag_set = set(tag_list)
#    if bool(veg_set & tag_set):
#        vegetarian += 1
#        continue
#
#    if bool(vgn_set & tag_set):
#        vegan += 1
#        continue
#
#print(f"Total: {entry_count}")
#print(f"Enthält tag \"vegan\": {100*round(vegan/entry_count, 4)}% or {vegan}")
#print(f"Enthält tag \"vegetarisch\": {100*round(vegetarian/entry_count, 4)}% or {vegetarian}")

#print(data["tags"])
#tag_domain = domain(data["tags"])
#
#print(len(tag_domain))
#for tag in tag_domain:
#    print(tag)

#vvo_tags, info_tags = filter_vvo_tags(data["tags"], ["vegan", "vegetarisch"], [])
#count = 0
#for tag in vvo_tags:
#    count += len(tag)
#print(count)

