# transmission-rss
RSS TV episode downloader for transmission

# Installation
```
git clone https://github.com/asayles/transmission-rss.git
```

# Usage
## Add details to the script
There are a few varialbles you'll need to add in the beginning of the script
```
vim transmission-rss.py
```
Fill in these settings
```
FEED_URL = ''
TRACKER_FILE = 'transmission-rss-tracker.json'
TRANSMISSION_HOST = ''
TRANSMISSION_PORT = 9091
TRANSMISSION_USER = ''
TRANMISSION_PASSWORD = ''
```

## Set shows to track in tracking file
You'll need to create or modify the tracker file to include shows you would like to track. 
<aside class="notice">
You only need to add the 'show title' and 'directory'. The episodes will be added as they are downloaded.
</aside>

```
vim ./transmission-rss-tracker.json
```
Ex
```
{
    "big bang theory": {
        "11": [
            "21"
        ], 
        "directory": "/tv/the_big_bang_theory"
    }, 
    "greys anatomy": {
        "directory": "/tv/greys_anatomy"
    }, 
    "the walking dead": {
        "directory": "/tv/the_walking_dead"
    }
}
```

## Run the script (probably from a cron)
```
./transmission-rss.py
```