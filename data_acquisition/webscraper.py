# Credits to Lia Lenckowski <3

import requests as r
from bs4 import BeautifulSoup
import json
import urllib.parse
import os
import threading

def try_exec(l, msg=None):
    try:
        return l()
    except Exception as e:
        print("[WARN] " + str(e) + (" at " + msg if msg else ""))
        return None

def get_week(ort, mensa): # -> [(date, [(mensa/cafeteria, text, preis(e), sachen)])]
    url = f"https://studentenwerk.sh/de/mensen-in-kiel?ort={ort}&mensa={mensa}#mensaplan"
    soup = BeautifulSoup(r.get(url).content, "html.parser")
    days = soup.select("div[class*='tag_headline']")
    days = filter(lambda d: not "tab_nicht_sichtbar" in d["class"], days)

    ret = []

    for day in days:
        day_ret = []

        date = day["data-day"]
        menu = day.select_one("div[class*='mensa_menu']")

        try:
            for item in menu.select("div[class*='mensa_menu_detail']"):
                text = list(item.select_one("div[class*='menu_name']").stripped_strings)
                ims = item.select_one("div[class*='element_2']").select("img")
                tags = [img["alt"] for img in ims]
                mensa_type = list(item.select_one("div[class*='menu_art']").stripped_strings)[0]

                prices = try_exec(
                    lambda: list(item.select_one("div[class*='menu_preis']").stripped_strings)[0].split(" / "),
                    msg=f"{ort_names[ort]}, {mensa_names[(ort, mensa)]}"
                )

                day_ret.append((mensa_type, text, prices, tags))

        except Exception as e:
            raise type(e)(str(e) + " at " + str(date))

        ret.append((date, day_ret))

    return ret

ort_names = {
    "1": "Kiel",
    "2": "Flensburg",
    "3": "Lübeck",
    "4": "Heide"
}

mensa_names = {
    ("1",  "1"): "Mensa I",
    ("1",  "2"): "Mensa II",
    ("1",  "3"): "Mensa Gaarden",
    ("1",  "4"): "Mensa Kesselhaus mit Cafeteria",
    ("2",  "7"): "Mensa Flensburg",
    ("2", "14"): "Cafeteria B-Gebäude",
    ("3",  "8"): "Mensa Lübeck mit Cafeteria",
    ("3",  "9"): "Cafeteria Musikhochschule",
    ("4",  "7"): "Mensa Heide mit Cafeteria"
}

def get_one(k, v):
    res = get_week(*k)

    filename = urllib.parse.quote(f"{ort_names[k[0]]}, {v}.json-lines", safe=", ")
    open(filename, "a").close()
    with open(filename, "r+b") as f:
        f.seek(0, os.SEEK_END)

        if f.tell() == 0:
            print(f"[INFO] {filename} empty, not searching for last line")
            f.write(bytes(json.dumps(res), encoding="ascii") + b"\n")
            return

        # file not empty; figure out whether we want to append, or replace
        # the last line.

        # seek right before last newline
        f.seek(-2, os.SEEK_CUR)

        # search backwards for the beginning of the last line
        while True:
            if f.tell() == 0 or f.read(1) == b"\n":
                break
            # undo the read, and seek backwards one more
            f.seek(-2, os.SEEK_CUR)

        # read a line in, and check whether we want to replace it,
        # by checking the date of the first day
        pos = f.tell()
        l = json.loads(f.readline())
        f.seek(pos)

        if l[0][0] == res[0][0]:
            # remove the last line
            print(f"[INFO] truncating {filename}")
            f.truncate()
        else:
            # keep the last line
            print(f"[INFO] keeping all of {filename}")
            f.seek(0, os.SEEK_END)

        f.write(bytes(json.dumps(res), encoding="ascii") + b"\n")

if __name__ == "__main__":
    threads = [
        threading.Thread(target=get_one, args=(k, v)) for k, v in mensa_names.items()
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
