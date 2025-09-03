# 2bWikiScrape
A short and simple program made to scrape [The 2b2t Wiki](https://2b2t.miraheze.org). I started this project because I would like to scrape member lists from base/group/event pages for use in a 2b2t Discord bot I'm working on (name TBD).

*If you're interested, here's a little sneak peak of [QueuePeek v2](https://enby.pics/u/DVp9z9.png) I'm working on (QueuePeek was a 2b2t exploit allowing you to view/scrape the entirety of the 2b2t queue, I have found a very janky way to do this for about 35% of players in queue)*

## 'Devlog'
This is just sort of a blog-ish area for me to type out my thoughts as I work on this project. This is likely going to eventually turn into the first blog post on my website in a series I'm going to call 'flash projects' where I give myself ~24 hours from start to finish on a random project idea.
### Initial Thoughts (9:30am)
This doesn't seem too hard. The 2b2t wiki is hosted on miraheze.org and, like most wikis, is based on MediaWiki. This means we can simply get the API at https://2b2t.miraheze.org/w/api.php. My only wiki scraping experience is [The Hypixel Wiki](https://wiki.hypixel.net) (reference [my API](https://api.ragingenby.dev/#tag/Scraping/operation/GET_wiki_user))- and anyone who has attempted to get any usable data from that knows how annoying it is. That being said- the Hypixel wiki is quite complicated and I assume the 2b wiki will be easier since it doesn't require laying out complex templates such as crafting recipes. I have to head to work in a few minutes so I'll likely have to put this on pause for a while.