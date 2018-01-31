"""
old_posts

A script to figure out what blog post you wrote X years ago.
"""
import datetime

import requests

import dateutil.parser

sites = {
    'tralev': 'https://tralev.net',
    'levlaz': 'https://levlaz.org'
}

today = datetime.date.today()

def get_posts(site):
    response = requests.get("{0}/wp-json/wp/v2/posts?per_page=100".format(site))

    pages = int(response.headers['X-WP-TotalPages'])
    posts = []

    for i in range(1, pages+1):
        response = requests.get("{0}/wp-json/wp/v2/posts?page={1}".format(site, i))

        for i in response.json():
            posts.append(i)

    return posts

def get_date(date_string):
    post_date = dateutil.parser.parse(date_string)
    date = datetime.date(post_date.year, post_date.month, post_date.day)
    return date

def get_years_ago(date):
    return today.year - date.year

def main():
    messages = []
    for s in sites:
        print("today is", today)
        print("checking", s)
        posts = get_posts(sites[s])
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

    return messages

def handler(event, context):
    messages = main()
    return {
        'messages': messages
    }

if __name__ == '__main__':
    main()
