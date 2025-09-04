# 2bWikiScrape
A short and simple program made to scrape [The 2b2t Wiki](https://2b2t.miraheze.org). I started this project because I would like to scrape member lists from base/group/event pages for use in a 2b2t Discord bot I'm working on (name TBD).

*If you're interested, here's a little sneak peak of [QueuePeek v2](https://enby.pics/u/DVp9z9.png) I'm working on (QueuePeek was a 2b2t exploit allowing you to view/scrape the entirety of the 2b2t queue, I have found a very janky way to do this for about 35% of players in queue)*

## 'Devlog'
This is just sort of a blog-ish area for me to type out my thoughts as I work on this project. This is likely going to eventually turn into the first blog post on my website in a series I'm going to call 'flash projects' where I give myself ~24 hours from start to finish on a random project idea.
### Initial Thoughts (9:30am)
This doesn't seem too hard. The 2b2t wiki is hosted on miraheze.org and, like most wikis, is based on MediaWiki. This means we can simply get the API at https://2b2t.miraheze.org/w/api.php. My only wiki scraping experience is [The Hypixel Wiki](https://wiki.hypixel.net) (reference [my API](https://api.ragingenby.dev/#tag/Scraping/operation/GET_wiki_user))- and anyone who has attempted to get any usable data from that knows how annoying it is. That being said- the Hypixel wiki is quite complicated and I assume the 2b wiki will be easier since it doesn't require laying out complex templates such as crafting recipes. I have to head to work in a few minutes so I'll likely have to put this on pause for a while.
### Time to actually do stuff (7:17pm)
I just got some free time for the first time since this morning so I'm actually getting started on making this thing. I planned on making my own simple MediaWiki API parser. However, Python's main advantage is its massive selection of libraries for anything you could possibly imagine. This is the main reason I use it for flash projects like this. I did a little research and most libraries I found were either poorly made or did not support async- [async-mediawiki](https://pypi.org/project/async-mediawiki/) seems promising though.
### I got distracted (9:12pm-9:29pm)
Unforunately as a carbon based lifeform I require food to sustain myself so I got distracted making dinner but I am (hopefully) actually going to finish this now. NEXT COMMIT WILL HAVE ACTUAL WORK TRUST

**I LIED** Unfortunately, `async-mediawiki` does not have documentation so I am going to have to do some studying to figure out how I can use this, but I think that is worth it considering the alternatives. I am hoping it works because it is like 6-7 years old- but the most updated wrapper I could find is from 2021 and didn't seem as well made so I'm hoping this works.
### Finding a new library (9:30pm-9:46pm)
I honestly don't know why I had any faith that this random 7 year old package would still function. I should've at least slightly tested it before writing my code around it but that's my fault. Time to test a bunch of alternatives.

First I am looking at [aiomwclient](https://github.com/Wadu436/aiomwclient). I was originally turned away from this by the fact that it requires a setup script to run (in my experience a red flag when it comes to Python packages)- but as it turns out this is an optional step. A fun bonus is that aiomwclient is an async wrapper of [mwclient](https://github.com/mwclient/mwclient) which even ha [readthedocs page](https://mwclient.readthedocs.io/en/latest/user/connecting.html)!

**OK** so I got distracted overengineering user-agent generation but [this](https://enby.pics/u/SX9dSj.png) is beautiful and you can't argue otherwise.
### THE PACKAGES SUCK (11:22pm)
No offense to the authors of any of these MediaWiki packages, but they suck. I don't know why I bothered spending this much time finding a package when I have more experience scraping HTML than using MediaWiki but that's my fault for getting overexcited
### Basic Work Done (11:49pm)
Ok I have put together a simple little API script to get the ID and name of every page on the wiki. This would've taken me 5 minutes to do and I should've just done this from the start but you live and you learn. In the finaly blog post this entry will probably be the second paragraph but that also means this is where the project really starts!

For logging of data, I currently am just using `output/` directory. I have `output/all_pages.json` which has every page on the wiki in this format:
```json
{
    "title": "string",
    "pageid": 0, // integer
    "ns": 0 // this is the namespace, which is always 0 for the 2b wiki
}
```
And I am also logging the raw HTML sent by the API to `output/{pagename}.html`. Obviously this isn't efficient and just for temporary use, but I now need to come up with a more permanent solution. You may notice the fact that I establish an unused variable, `MONGO_URI`, in `constants.py`- I am of course using my favorite DB: MongoDB.

Quick side tangent: For those unaware of my MongoDB obsession, it was sparked by [TGWaffles](https://github.com/TGWaffles). He has a really cool project (which I am now involved in) called [iTEM](https://tem.cx). Very early on into my developer days I was interested in this project and asked him how it worked, he told me a bunch of stuff but importantly the fact that he used MongoDB. I decided to copy his project idea and now run my own copy of iTEM called [Skypixel](https://ragingenby.dev/skypixel). Anyway, I used MongoDB for this and ever since I have been obsessed with using it for any large scale storage application.

Now MongoDB **DEFINITELY** is not the most efficient way to store this data. I mean I am talking about documents that look roughly like:
```json
{
    "_id": 4097,
    "pageid": "Popbob",
    "ns": 0,
    "html": "BIG ASS HTML BLOB"
}
```
I __***KNOW***__ this is inefficient and not even a good use of MongoDB's storage system, but I am doing this temporarily. In the long term I don't even planning on storing the actual HTML (maybe).
### SCRAPING TIME (12:00am)
OK so now we have page ID's for every 2b wiki page so we can just use `action=parse` requests to the MediaWiki API to get all the data we want... right?

Well yes, technically, this is possible. This is always what I did for [Hypixel Wiki](https://hypixel.wiki) scraping. However, This time I want to do it the right way (BORINGGGG). Looking into the MediaWiki API a bit more, it seems smarter to do `action=query` requests. This spits out a slightly easier to parse string
<details>
<summary>"Easier to parse string"</summary>

```text
{{DISPLAYTITLE:popbob}}
{{Pp-pc}}
{{PlayerTemplate
|title=popbob
|quote="[She] hates you people" -jared2013, October 2018
|image=Popbob-skin.png
|caption=
|date_joined=early 2011
|status=Inactive - 2020
|playertype=Griefer, Exploiter
|bases=[[Ramiel's Watch]], [[Squid Base]], [[Plugin Town]], [[Imperator's Base]], [[700Base]], [[popbob's End base]], [[1095 365 Base]],  [[Kaamtown]], [[Imperator's Base 2]]
|griefs=[[Old Town]], [[Ravendel]], [[Space Valkyria]], 
|alts=OreMongerIsANig, OreMongerIsANigr, ImOnTenacity, sendGAYStoISIS, JIDF, RIDF (formerly RadicalHiccup), popbobYT,  _popbob, xXBR0NY_PR1D3Xx, Uiopopbob
|c_affls=[[Nerds Inc]]
|p_affls=[[4channers]], [[Facepunch Republic]], [[Guardsmen]], and [[0Neb Appreciation Group]]
}}'''popbob''' is a well-known player and prolific griefer who joined in early 2011 from 4chan. She<ref group="Notes">popbob has chosen to be referred to with female pronouns.</ref> is widely known, even beyond 2b2t, and has become a well-known cultural icon for minecraft players in general. 

==History==
===Beginnings===
popbob joined [[2b2t]] in early 2011 as a result of browsing 4chan, although she became associated with the [[Facepunchers]]. She participated in a limited number of bases, generally with [[Facepunchers]], (such as [[Ramiel's Watch]], [[Squid Base]], [[1095 365 Base]], and [[Kaamtown]]), but increasingly tended towards griefing. She become an especially prolific griefer over time after creating an early version of the newchunks module and also being an early adopter of [[Hacked Clients]] as a whole. As part of this, she later created [[nhack]] with [[iTristan]].

popbob successfully backdoored 2b2t twice in 2011, leading to the creation of a variety of [[Illegal items]], as well as the foundation of [[Plugin Town]]. Both backdoors were achieved through popbob's creation of software for [[Hausemaster]] to run the server. The majority of Illegal items available on the server were first introduced as a result of popbob's backdoors.

===Griefing===
[[File:Kek popbob.png|left|thumb|A screenshot of her solo base]]
popbob generally griefed bases alone, although she sometimes did so with other players that gradually formed [[Nerds Inc]]. She was able to determine other players' coordinates using methods including [[Coordinate exploit#Thunderhack|Thunderhack]], which worked as a result of an oversight in Minecraft's code that allowed the coordinates of thunder to be tracked down through packets, as the sound of thunder was global and would only strike where players were located. This information was used to triangulate other players' locations. Thunderhack was used to find locations such as [[Imperator's Base]].

Through use of (what was revealed to be backdoored) nhack among other 2b2t players, popbob discovered a rebuild of Kaamtown being conducted by [[xcc2]], [[taylo112]], [[iTristan]], [[Omaliymix]], and [[Kaameron]]. She used nhack to take screenshots of Omaliymix and Kaameron's desktops and send them to them, which resulted in both of them permanently quitting the server.

===Intermittent Involvement===
She played the server increasingly less as time moved on, although she contributed to the now-iconic grief of [[The Lands]] by re-connecting [[Brannilion|Branillion's]] bedchain, following a [[C4RTM4N#BedTP|scheme to grief the base]] by [[C4RTM4N]] and [[taylo112]]. This was later mentioned in a now-iconic YouTube video by FitMC that dramatized the event. 

Following [[TheCampingRusher|TheCampingRusher's]] video, she played 2b2t increasingly intermittently, although she came back temporarily in 2020 to join the [[Guardsmen]] and [[0Neb Appreciation Group|spread misinformation about Nocom]].

==Notes==
<references group="Notes"/>

[[Category:Players]]
[[Category:Griefers]]
[[Category:Backdoorers]]
[[Category:Facepunch]]
[[Category:4chan]]
[[Category:2011]]
[[Category:Protected Pages]]
```

</details>

Yeah it's not... fun to parse, but it is certainly possible! I'm sure it won't take me that long to do that thou-
### it took me a long time to do that (12:40am)
I spent way to long making some very shitty code to parse this data and it is... passable? It's definitely not readable and I refuse to comment my personal code (mostly because I'm lazy but I excuse it by saying it's to prevent people from mistaking my work as Ai slop). Anyway here's what I wrote up if you're curious, I promise you it is bad but you're free to attempt to read it:
<details>
<summary>Python jumpscare</summary>

```python
def mediawiki_to_markdown(wikitext: str) -> str:
    text = wikitext.replace("\r\n", "\n").replace("\r", "\n")

    title = None
    m = re.search(r"\{\{\s*DISPLAYTITLE\s*:\s*([^}]+)\}\}", text, flags=re.I)
    if m:
        title = m.group(1).strip()
    else:
        m = re.search(
            r"\{\{\s*PlayerTemplate\b.*?\|\s*title\s*=\s*([^\n|}]+)",
            text,
            flags=re.I | re.S,
        )
        if m:
            title = m.group(1).strip()

    text = re.sub(
        r"\{\{\s*DISPLAYTITLE\s*:[^}]+\}\}", "", text, flags=re.I
    )
    text = re.sub(r"\{\{\s*Pp-pc[^}]*\}\}", "", text, flags=re.I)
    text = re.sub(
        r"\{\{\s*PlayerTemplate\b.*?\}\}", "", text, flags=re.I | re.S
    )

    text = re.sub(r"<ref[^/>]*/>", "", text, flags=re.I)
    text = re.sub(
        r"<ref[^>]*>.*?</ref>", "", text, flags=re.I | re.S
    )
    text = re.sub(r"<references[^>]*/>", "", text, flags=re.I)

    text = re.sub(
        r"\[\[(?:File|Image):.*?\]\]", "", text, flags=re.I | re.S
    )
    text = re.sub(r"\[\[\s*Category:[^\]]+\]\]", "", text, flags=re.I)

    text = re.sub(r"'''''(.*?)'''''", r"***\1***", text, flags=re.S)
    text = re.sub(r"'''(.*?)'''", r"**\1**", text, flags=re.S)
    text = re.sub(r"''(.*?)''", r"*\1*", text, flags=re.S)

    def _heading(mh: re.Match) -> str:
        level = len(mh.group(1))
        content = mh.group(2).strip()
        return f"{'#' * level} {content}"

    text = re.sub(
        r"^(={1,6})\s*(.*?)\s*\1\s*$", _heading, text, flags=re.M
    )

    def _wikilink(mw: re.Match) -> str:
        inner = mw.group(1).strip()
        if inner.startswith(("Category:", "File:", "Image:")):
            return ""
        parts = inner.split("|", 1)
        target = parts[0].strip()
        label = parts[1].strip() if len(parts) > 1 else target

        if target.startswith(":"):
            target = target[1:]

        if "#" in target:
            page, anchor = target.split("#", 1)
        else:
            page, anchor = target, None

        page_path = quote(page.replace(" ", "_"), safe="()!~*._-:")
        if anchor:
            anchor_id = quote(anchor.replace(" ", "_"), safe="()!~*._-:")
            url = f"{constants.WIKI_BASE_URL}{page_path}#{anchor_id}"
        else:
            url = f"{constants.WIKI_BASE_URL}{page_path}"

        return f"[{label}]({url})"

    text = re.sub(r"\[\[([^[\]]+)\]\]", _wikilink, text)

    def _ext(mex: re.Match) -> str:
        url = mex.group(1)
        label = mex.group(2).strip() if mex.group(2) else url
        return f"[{label}]({url})"

    text = re.sub(
        r"\[(https?://[^\s\]]+)(?:\s+([^\]]+))?\]", _ext, text
    )

    text = unescape(text)
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    if title:
        if text:
            return f"# {title}\n\n{text}"
        return f"# {title}"
    return text
```

</details>

All this code does is transform the MediaWiki dump into markdown. I know that doesn't seem very helpful BUT I PROMISE IT IS TRUST ME (don't). Anyway this is probably pretty unstable because I only tested it with a few pages but its 12:45am now and I have work in the morning so that's for future me. LGTM
### back to the main idea (9:11am-9:36am)
I sorta lost sight of the original idea which was to scrape memberlists from wiki pages. The steps I've been doing certainly help with that but I need to get off my ass and actually do that. The first step is to honestly download all the wiki pages. The ground work for actually getting the playerlists is super easy considering we can just [check the markdown](https://enby.pics/u/dA2yBu.png). Luckily, MediaWiki allows you to request up to 50 pages at a timewhich means I can download the entire wiki in 28 API requests. I slopped together some code to send these bulk requests. After some slight edits (such as cleansing page names so that the file path isn't broken), it just... works. I'm going to remove output/pages/*.md from .gitignore so this will be committed to the repo in one sec.