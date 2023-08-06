import pandas as pd
import os
import datetime

USER_DATA = "data/user_data.txt"

def saveUserData(email, password, keywords):
    with open(USER_DATA, "w") as file:
        file.write(f"Email: {email}\n")
        file.write(f"Password: {password}\n")
        file.write(f"Keywords: {keywords}\n")

def getUserData():
    try:
        with open(USER_DATA, "r") as file:
            lines = file.readlines()
            email = lines[0].split(": ")[1].strip()
            password = lines[1].split(": ")[1].strip()
            keywords = lines[2].split(": ")[1].strip()
            return email, password, keywords
    except:
        return "", "" , ""
    
def saveStories(stories, year, month, date):
    df = pd.DataFrame.from_records([s.toDict() for s in stories])
    df = df.drop_duplicates(subset='title', keep="last")

    output_path = f"data/stories/{year}/{month:02d}/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    df.to_csv(f'{output_path}/{date:02d}.csv', index=False)
    return output_path

def getStories(date:datetime.date):
    path = f"data/stories/{date.year}/{date.month:02d}/{date.day:02d}.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df
    return None

def getPrefetchUrls(date:datetime.date):
    df = getStories(date)
    prefetched_url = df.dropna(subset=['content'])['url'].tolist()
    return prefetched_url