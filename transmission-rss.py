#!/usr/bin/python

import sys
import re
import feedparser
import transmissionrpc
import json

FEED_URL = ''
TRACKER_FILE = 'transmission-rss-tracker.json'
TRANSMISSION_HOST = ''
TRANSMISSION_PORT = 9091
TRANSMISSION_USER = ''
TRANMISSION_PASSWORD = ''

if __name__ == "__main__":
    # load tracker
    tracker = json.load(open(TRACKER_FILE))
    # load RSS feed
    feed = feedparser.parse(FEED_URL)
    if feed.bozo and feed.bozo_exception:
        sys.stderr.write("Error reading feed \'{0}\': ".format(FEED_URL) + str(feed.bozo_exception).strip())
        sys.exit(1)
    # connect to transmission
    try:
        tc = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT,
                                    user=TRANSMISSION_USER, password=TRANMISSION_PASSWORD)
    except transmissionrpc.error.TransmissionError as te:
        sys.stderr.write("Error connecting to Transmission: {}\n".format(str(te).strip()))
        exit(0)
    except:
        sys.stderr.write("Error connecting to Transmission: {}\n".format((sys.exc_info()[0]).strip()))
        exit(0)
    # match feed entries to tracked shows
    for show in tracker.keys():
        # make the show all lower case for easier matching
        if show != show.lower():
            tracker[show.lower()] = tracker.pop(show)
            show = show.lower()
        # see if the show from the tracker...
        for tor in feed.entries:
            # ...matches a tor from the feed
            if show in tor.title.lower():
                # parse the episode
                match = re.search('s[0-9][0-9]e[0-9][0-9] ', tor.title.lower()) # see if you need this episode
                if match:
                    season, episode = match.group(0).strip('s ').split('e')
                    # see if this episode is needed
                    if season not in tracker[show].keys():
                        tracker[show][season] = [episode]
                    elif episode not in tracker[show][season]:
                        tracker[show][season].append(episode)
                    else:
                        break
                    tc.add_torrent(tor.link, download_dir=tracker[show]['directory'], paused=True)
    with open(TRACKER_FILE, 'w') as tracker_file:
        json.dump(tracker, tracker_file, sort_keys = True, indent = 4,
                  ensure_ascii = False)
