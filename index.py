#! python3
import praw
import pandas as pd
import datetime as dt

reddit = praw.Reddit() #Hidden keys

subreddit = reddit.subreddit('cars')
top_subreddit = subreddit.top()

topics_dict = { "title":[], \
                "score":[], \
                "id":[], "url":[], \
                "comms_num": [], \
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
topics_data = topics_data.assign(timestamp = _timestamp)
topics_data.to_csv('FILENAME.csv', index=False)
