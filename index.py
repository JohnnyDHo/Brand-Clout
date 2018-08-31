import praw
import pandas as pd
import datetime as dt
import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Start reddit API, change these with your own parameters
reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent,
                     username=config.username,
                     password=config.password)


# Choose subreddit
subreddit = reddit.subreddit('cars')

# Look at top posts
top_subreddit = subreddit.top()

# Dictionary of data to be found
topics_dict = {"title": [],
               "score": [],
               "id": [], "url": [],
               "comms_num": [],
               "created": []}

# For all top posts, do this
for submission in top_subreddit:
    topics_dict["title"].append(submission.title.encode('ascii', 'ignore').decode('ascii'))
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url.encode('ascii', 'ignore').decode('ascii'))
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)

# Brands dict
brands = {"Toyota": 0, "Tesla": 0}
for titl in topics_dict["title"]:
    for brand, coun in brands.items():
        if brand in titl:
            coun += 1

# Viewable as pandas DataFrame
topics_data = pd.DataFrame(topics_dict)

# Fixes reddit's date formatting (optional)
def get_date(created):
    return dt.datetime.fromtimestamp(created)

# Calls the function to fix the date formatting
_timestamp = topics_data["created"].apply(get_date)
topics_data = topics_data.assign(timestamp=_timestamp)

# Google API scope
scope = 'https://www.googleapis.com/auth/drive'

# Google credentials, use your own with Drive and Sheets API
credentials = ServiceAccountCredentials.from_json_keyfile_name("Brand Clout-7885e8400fd4.json", scope)
gc = gspread.authorize(credentials)

# Open sheets file
wks = gc.open('d').sheet1


# Loop to update cells in Sheets
i = 5
for title in topics_dict["title"]:
    wks.update_cell(i, 1, title)
    i += 1

j = 5
for name, count in brands.items():
    wks.update_cell(j, 2, name)
    wks.update_cell(j, 3, count)
    j += 1

# Save as a CSV file, uncomment to use
#topics_data.to_csv('FILENAME.csv', index=False)
