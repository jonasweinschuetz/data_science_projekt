import pandas

# takes the tag_lists of entries (2D list) and returns all tags found
def domain(series):
    # isolate entries in category
    checked = []
    for tag_list in series:
        for tag in tag_list:
            if tag not in checked:
                checked.append(tag)
    return checked

def filter_vvo_tags(df, vvo_tags, non_vvo_tags):
    vvos = [] # will contain list of vvo_tags (most of the time only 1, rarely 2)
    info = [] # will contain list of non vvo_tags (most of the time empty or not interesting)

    for tag_list in df["category"]:
        vvos.append([tag for tag in tag_list if tag in vvo_tags])
        info.append([tag for tag in tag_list if tag in non_vvo_tags])

        missed_tags = [tag for tag in tag_list if tag not in vvo_tags and tag not in non_vvo_tags]
        if missed_tags != []:
            print("Tag(s) where missed: ", missed_tags)
    return vvos, info
