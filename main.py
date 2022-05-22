import argparse
import calendar
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import tweepy
from dateutil import tz
from dotenv import load_dotenv

from follow_locations import twitter_followers


def tweet_heatmap(username):
    to_zone = tz.gettz('Europe/London')

    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    client = tweepy.Client(bearer_token=bearer_token)

    user = client.get_user(username=username)

    date_times = []
    for tweet in tweepy.Paginator(client.get_users_tweets, user.data.id,
                                  tweet_fields='created_at',
                                  max_results=100).flatten(limit=1000):
        date_times.append(tweet.created_at.astimezone(to_zone))

    df = pd.DataFrame(date_times, columns=['date'])
    df['day_of_week'] = df.apply(lambda row: row['date'].weekday(), axis=1)
    df['hour'] = df.apply(lambda row: row['date'].hour, axis=1)
    df = df.groupby(['day_of_week', 'hour']).size().reset_index(name='counts')
    df = df.pivot(index='hour', columns='day_of_week', values='counts')

    fig, ax = plt.subplots(figsize=(16, 9))
    sb.heatmap(df, ax=ax, cmap="Blues", linewidth=0.3, cbar_kws={"shrink": .8})
    xticks_labels = [calendar.day_name[day_of_week_idx] for day_of_week_idx in df.columns.values]
    ax.set_xticks(np.arange(len(xticks_labels)) + .5, labels=xticks_labels)
    # xticks
    ax.xaxis.tick_top()
    # axis labels
    ax.set_xlabel('Days')
    ax.set_ylabel('Hour of Day')
    ax.set_title(f'{username} Tweet Heatmap')

    plt.show()


if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser(prog='main.py')
    subparsers = parser.add_subparsers(dest='command')

    # Tweet Heetmap Parser
    TWEET_HEATMAP = 'tweet-heatmap'
    data_cleanser_parser = subparsers.add_parser(TWEET_HEATMAP, help='produce a heatmap of most recent tweets')
    data_cleanser_parser.add_argument('--username', type=str, help='twitter username')

    # Followers Parser
    FOLLOWERS = 'followers'
    data_cleanser_parser = subparsers.add_parser(FOLLOWERS,
                                                 help='produce a list of information about twitter followers')
    data_cleanser_parser.add_argument('--username', type=str, help='twitter username')

    parsed_args = parser.parse_args(sys.argv[1:])
    if parsed_args.command == TWEET_HEATMAP:
        tweet_heatmap(parsed_args.username)
    if parsed_args.command == FOLLOWERS:
        twitter_followers(parsed_args.username)
    else:
        print('Command not recognised')
