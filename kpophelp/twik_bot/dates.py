from datetime import date, timedelta

sub_link = "https://reddit.com/r/kpop"
sub_wiki = "{}/wiki/".format(sub_link)

class Show():
    def __init__(self, name, show_link, date):
        self.name = name
        self.show_link = show_link
        self.date = date
        self.url = "{}{}{}".format(sub_wiki, show_link, date)
        self.praw_url = "{}{}".format(show_link, date)
        self.discussion_url = ""
        self.winner = ""

def get_shows():
    show_links = [
        "music-shows/music-bank/",
        "music-shows/m-countdown/",
        "music-shows/show-champion/",
        "music-shows/the-show/",
        "music-shows/inkigayo/",
        "music-shows/show-music-core/",
    ]

    shows = {
        0: "Music Bank",
        1: "M!Countdown",
        2: "Show Champion",
        3: "The Show",
        5: "Inkigayo",
        6: "Music Core",
    }

    result = [] # List of shows in order
    today = date.today() - timedelta(days=3)
    for i, (k,v) in enumerate(shows.items()):
        diff = timedelta(days=k)
        show_date = intl_fmt(today-diff)
        tmp_show = Show(v, show_links[i], show_date)
        result.append(tmp_show)

    result.reverse() # Reverse returns none -_-
    return result

def intl_fmt(date):
    return date.strftime("%Y%m%d")

def main():
    return get_shows()

if __name__ == "__main__":
    import praw # I know I know I know
    import re
    shows = get_shows()

    r = praw.Reddit(client_id='k_bjeF902375gw',
                    client_secret='-_-a5vT8UlEVv68SVX6hQcTwm9I',
                    user_agent='TWIK Bot')

    for show in shows:
        wiki = r.subreddit('kpop').wiki[show.praw_url]
        markdown = wiki.content_md
        # Get Winner
        before_winner, winner, after_winner = markdown.partition('## WINNER')
        show.winner = \
            re.search(
                '###\s\[(.*?)(?:\s-\s.*)*\]',
                after_winner
            ).group(1)
        # Get Discussion URL
        before_etc, etc, after_etc = after_winner.partition('## ETC')
        show.discussion_url = \
            re.search(
                '(http?s://?(www\.)reddit.com/r/kpop/comments/[^)]*)',
                after_etc
            ).group(0)

    print("Date | Performances | Discussion Thread | Winner")
    print("--- | --- | --- | ---")
    for show in shows:
        print("{} | [{}]({}) | [Thread]({}) | [{}](/spoiler)".format(
            show.date,
            show.name,
            show.url,
            show.discussion_url,
            show.winner
        ))
