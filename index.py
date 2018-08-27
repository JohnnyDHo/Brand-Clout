import praw
import pandas as pd
import datetime as dt
import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent,
                     username=config.username,
                     password=config.password)

subreddit = reddit.subreddit('cars')
top_subreddit = subreddit.top()

topics_dict = {"title": [],
               "score": [],
               "id": [], "url": [],
               "comms_num": [],
               "created": []}


for submission in top_subreddit:
    topics_dict["title"].append(submission.title.encode('ascii', 'ignore').decode('ascii'))
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url.encode('ascii', 'ignore').decode('ascii'))
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
topics_data = pd.DataFrame(topics_dict)


def get_date(created):
    return dt.datetime.fromtimestamp(created)


_timestamp = topics_data["created"].apply(get_date)
topics_data = topics_data.assign(timestamp=_timestamp)

scope = 'https://www.googleapis.com/auth/drive'

credentials = ServiceAccountCredentials.from_json_keyfile_name("Brand Clout-7885e8400fd4.json", scope)

gc = gspread.authorize(credentials)

wks = gc.open('d').sheet1
i = 5
for title in topics_dict["title"]:
    wks.update_cell(i, 1, title)
    i += 1
#topics_data.to_csv('FILENAME.csv', index=False)
