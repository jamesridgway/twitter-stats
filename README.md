# Twitter Stats

A basic playground for generating twitter statistics.

## Setup

    cp .env.example .env

You will need an app in the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)

`TWITTER_BEARER_TOKEN` is the _Bearer Token_ value for your given apps _Keys and Tokens_ page.

## Example Usage

The following will generate a heatmap of the 1000 most recent tweets for the given user.

    main.py tweet-heatmap --username=james_ridgway

