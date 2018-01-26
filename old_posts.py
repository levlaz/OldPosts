import requests
import dateutil.parser
import datetime

sites = {
    'tralev': 'https://tralev.net',
    'levlaz': 'https://levlaz.org'
}

today = datetime.date.today()

def get_posts(site):
    response = requests.get("{0}/wp-json/wp/v2/posts".format(site))

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
    for s in sites:
        posts = get_posts(sites[s])
        for p in posts:
            post_date = get_date(p['date'])

            if post_date.month == today.month and post_date.day == today.day:
                years_ago = get_years_ago(post_date)
                if years_ago == 1:
                    print("1 year ago I wrote about {0} {1}".format(p['title']['rendered'], p['link']))
                if years_ago > 1:
                    print("{0} years ago I wrote about {1} {2}".format(years_ago, p['title']['rendered'], p['link']))

if __name__ == '__main__':
    main()