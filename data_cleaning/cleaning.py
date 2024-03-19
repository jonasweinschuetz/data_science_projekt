import pandas as pd
from files import list_to_file, file_to_list

# takes the tag_lists of entries (2D list) and returns all tags found
def domain(series):
    # isolate entries in category
    checked = []
    for tag_list in series:
        tag_list = tag_list
        #print(tag_list, len(tag_list))
        for tag in tag_list:
            if tag not in checked:
                checked.append(tag)
    return checked

def filter_vvo_tags(series, vvo_tags, non_vvo_tags):
    vvos = [] # will contain list of vvo_tags (most of the time only 1, rarely 2)
    info = [] # will contain list of non vvo_tags (most of the time empty or not interesting)

    for tag_list in series:
        vvos.append([tag for tag in tag_list if tag in vvo_tags])
        info.append([tag for tag in tag_list if tag in non_vvo_tags])

        missed_tags = [tag for tag in tag_list if tag not in vvo_tags and tag not in non_vvo_tags]
        if missed_tags != []:
            print("Tag(s) where missed: ", missed_tags)
    return vvos, info

# returns vvo_status list for a given data frame
def classify_df_vvo_from_file(data):
    vvo_status = []

    vgn_names = set(file_to_list("Data/tags/vgn_names.txt"))
    veg_names = set(file_to_list("Data/tags/veg_names.txt"))
    meat_names = set(file_to_list("Data/tags/meat_names.txt"))
    vgn_veg_names = set(file_to_list("Data/tags/vgn_veg_names.txt"))
    meat_vgn_veg_names = set(file_to_list("Data/tags/vgn_veg_names.txt"))
    
    vgn_tags = set(file_to_list("Data/tags/vgn_tags.txt"))
    veg_tags = set(file_to_list("Data/tags/veg_tags.txt"))
    meat_tags = set(file_to_list("Data/tags/meat_tags.txt"))
    vgn_veg_tags = set(file_to_list("Data/tags/vgn_veg_tags.txt"))
    
    
    for index, meal in data.iterrows():
            tag_set = set(meal["tags"])
            meal_name = meal["meal_name"]
            
            # categorization happens after the strictness of the "querries"
            
            if bool(meat_tags & tag_set):
                vvo_status.append("meat")
                continue
                
            # for these categories we detect conventions only used by 3 states, not usefull :(, classify after strongest class
            if bool(vgn_veg_tags & tag_set):
                vvo_status.append("veget.") 
                continue
                
            if meal_name in meat_vgn_veg_names:
                vvo_status.append("meat") 
                continue
            
            if meal_name in vgn_veg_names:
                vvo_status.append("veget.") 
                continue
                
            if bool(veg_tags & tag_set):
                vvo_status.append("veget.")
                continue
    
            if bool(vgn_tags & tag_set):
                vvo_status.append("vegan")
                continue
                
            if meal_name in veg_names:
                vvo_status.append("veget.")
                continue
    
            if meal_name in vgn_names:
                vvo_status.append("vegan")
                continue
            
            vvo_status.append("-1")
    return vvo_status

# returns vvo_status acording to the given category sets for a tag list and a meal name 
def classify_vvo_instance_by_file(tag_list, meal_name, vgn_names, veg_names, meat_names, vgn_veg_names, meat_vgn_veg_names, vgn_tags, veg_tags, meat_tags, vgn_veg_tags):
    tag_set = set(tag_list)
    
    # categorization happens after the strictness of the "querries"
    
    if bool(meat_tags & tag_set):
        return "meat"
        
    if bool(vgn_veg_tags & tag_set):
        return "veget."
        
    if meal_name in meat_vgn_veg_names:
        return "meat"
    
    if meal_name in vgn_veg_names:
        return "veget."
        
    if bool(veg_tags & tag_set):
        return "veget."
    
    if bool(vgn_tags & tag_set):
        return "vegan"
        
    if meal_name in veg_names:
        return "veget."
    
    if meal_name in vgn_names:
        return "vegan"

    return "-1"
