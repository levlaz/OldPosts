"""
old_posts

A script to figure out what blog post you wrote X years ago.
"""
import datetime
import os

import requests

import dateutil.parser
from dateutil.relativedelta import relativedelta

sites = {
    'tralev': 'https://tralev.net',
    'levlaz': 'https://levlaz.org'
}

today = datetime.date.today()

def get_buffer_profiles():
    """
    Return list of all connected profile ID's in Buffer Account
    """
    profiles = requests.get("https://api.bufferapp.com/1/profiles.json?access_token={0}".format(os.environ['BUFFER_TOKEN']))

    return [s['id'] for s in profiles.json()]

def create_buffer_update(update):

    payload = {
        'profile_ids[]': get_buffer_profiles(),
        'text': update,
        'top': 'True'
    }

    response = requests.post("https://api.bufferapp.com/1/updates/create.json?access_token={0}".format(os.environ['BUFFER_TOKEN']), data=payload)

    return response.json()

def get_all_posts(site):
    # Ignore posts less than 1 year old.
    before = (today - relativedelta(years=1) + relativedelta(days=1)).isoformat()
    response = requests.head("{0}/wp-json/wp/v2/posts?per_page=100&before={1}T00:00:00".format(site, before))

    pages = int(response.headers['X-WP-TotalPages'])
    posts = []

    # iterate over every page in response
    for i in range(1, pages+1):
        response = requests.get("{0}/wp-json/wp/v2/posts?per_page=100&page={1}&context=embed&before={2}T00:00:00".format(site, i, before))

        posts.extend(response.json())

    return posts

def get_date(date_string):
    """ Extract python date from WP API post date. """
    post_date = dateutil.parser.parse(date_string)
    date = datetime.date(post_date.year, post_date.month, post_date.day)
    return date

def get_years_ago(date):
    """ Return how many years ago a date was """
    return today.year - date.year

def main():
    messages = []
    for s in sites:
        posts = get_all_posts(sites[s])

        for p in posts:
            post_date = get_date(p['date'])

            if post_date.month == today.month and post_date.day == today.day:
                years_ago = get_years_ago(post_date)
                if years_ago == 1:
                    messages.append("1 year ago I wrote about {0} {1}".format(p['title']['rendered'], p['link']))
                if years_ago > 1:
                     messages.append("{0} years ago I wrote about {1} {2}".format(years_ago, p['title']['rendered'], p['link']))

    if len(messages) == 0:
        messages.append("No posts found for {0}".format(today))
    else:
        for message in messages:
            print(create_buffer_update(message))

    return messages

def handler(event, context):
    """
    AWS Lambda Handler
    https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
    """
    messages = main()
    return {
        'messages': messages
    }

if __name__ == '__main__':
    print(main())
