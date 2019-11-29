# ERB-bot
 
 A bot designed for r/erb to comment the next lyric of a ERB song.


## Implementation

Uses Genius' API to fetch the artist Epic Rap Battles of History's songs, and then scrapes the HTML for lyrics. Saves the lyrics in a JSON that is loaded on each new instance, and then fetches comments from the sub and see if they fit an existing lyric using `re.search`.

## Relevant links

**Genius API:** https://docs.genius.com/

**How to get lyrics from Genius:** https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/

**Based partially on Hearthscan_Bot:** https://github.com/d-schmidt/hearthscan-bot
