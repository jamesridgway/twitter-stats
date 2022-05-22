import csv
import os

import tweepy


def twitter_followers(username):
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    user = client.get_user(username=username)

    with open(f'{username}_followers.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['username', 'location'])
        writer.writeheader()

        for follower in tweepy.Paginator(client.get_users_followers, user.data.id,
                                         user_fields='location',
                                         max_results=1000).flatten():
            writer.writerow({
                'username': follower.username,
                'location': follower.location
            })
