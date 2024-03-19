from collections import Counter
import pandas as pd

data = pd.read_csv("Data/german-canteens(filtered).csv", sep="@", infer_datetime_format=True)
# evaluates tag_list as list (from string)
data["tags"] = list(map(eval, data["tags"]))

merged_tag_lists = [tag for tag_list in data["tags"] for tag in tag_list]
tag_count = Counter(merged_tag_lists)

print(len(tag_count))

for tag, count in tag_count.items()
    if count > 4

