{{ExploitInfobox
|title=nocom
|type=Coordinate exploit
|date_first_used=July 2018
|date_leaked=July 2021
|date_patched=July 2021
|discoverer=[0x22](https://2b2t.miraheze.org/wiki/0x22) and [Babbaj](https://2b2t.miraheze.org/wiki/Babbaj)
|image=File:2b2t_Nocom_Overworld_Heatmap.png
|caption=Nocom heatmap of the overworld, from -245k to +245k, from early 2020 to mid-2021
}}
{{Nocom}}
**Nocom** was an exploit used by [Nerds Inc](https://2b2t.miraheze.org/wiki/Nerds_Inc) from 2018 to 2021. Considered to be the most severe exploit in [2b2t](https://2b2t.miraheze.org/wiki/2b2t) history, it began when a server lagging/crashing exploit was patched in [PaperMC](https://papermc.io/), a *Minecraft* server software used on 2b2t. The exploit allowed Nerds Inc to observe the player movements of every player on 2b2t.

The initial exploit allowed a player to force the server to load arbitrary chunks with packet with no rate limit, causing the main thread of the server to block until all of the packets were processed. By varying the number of packets the server could freeze for just a few seconds, or until the [watchdog](https://en.wikipedia.org/wiki/Watchdog_timer) thread killed the whole server. In the [queue](https://2b2t.miraheze.org/wiki/queue) server, it was possible to send enough packets to keep the network thread busy with the exploiter's packets for so long that the server thought the connection for every other player in the queue was dead and disconnected them, thus allowing the queue to be skipped. [0x22](https://2b2t.miraheze.org/wiki/0x22) and [Babbaj](https://2b2t.miraheze.org/wiki/Babbaj) would utilize the exploit to intentionally crash the server, expecting that [Hausemaster](https://2b2t.miraheze.org/wiki/Hausemaster) would report the exploit to Paper.

The exploit was fixed in July 2018. However, the fix allowed for the ability to check if any chunk in the world was currently loaded. Nerds Inc exploited this new vulnerability by scanning the world in a spiral pattern, sending thousands of packets per second. Although the approach was primitive, it was effective up to about 1 million blocks. In 2019, Hausemaster, in response to off-hand switch sound lag exploit, added a rate limit that severely limited the effectiveness of the packet spamming approach and usage of the exploit temporarily stopped. In 2020, Nerds Inc enlisted [Leijurv](https://2b2t.miraheze.org/wiki/Leijurv), the lead developer of [Baritone](https://2b2t.miraheze.org/wiki/Baritone), to create a new system that was effective with the strict rate limit by tracking players as they move. In addition to tracking players, nocom was able to slowly remotely download bases.

Nerds Inc employed a disinformation campaign to downplay coordinate exploits in an effort to ensure nocom's secrecy. Other exploits, such as the pet teleportation exploit, were used as covers for nocom. Nocom has been attributed to the destruction of [Space Valkyria 3 V2](https://2b2t.miraheze.org/wiki/Space_Valkyria_3_V2), as well as [Niflheim](https://2b2t.miraheze.org/wiki/Niflheim), [Acheron](https://2b2t.miraheze.org/wiki/Acheron), [Avalonia](https://2b2t.miraheze.org/wiki/Avalonia), and [Yggdrasil](https://2b2t.miraheze.org/wiki/Yggdrasil); several other bases were destroyed under the guise of the "Dipper Nation", a series of images and memes. Nocom was also used to fund several projects started by the [SpawnMasons](https://2b2t.miraheze.org/wiki/SpawnMasons) using stashes located through the exploit. Nocom's existence was threatened by [0Neb](https://2b2t.miraheze.org/wiki/0Neb), who attempted to raise suspicion of Nerds Inc, and the [Infinity Incursion](https://2b2t.miraheze.org/wiki/Infinity_Incursion), who recreated a less powerful version of the exploit and used it against [Fit](https://2b2t.miraheze.org/wiki/Fit).

In July 2021, [Hausemaster](https://2b2t.miraheze.org/wiki/Hausemaster) implemented a fix to nocom—and similar exploits—limiting the range the server would return chunk information for. Several days later, Nerds Inc released information on nocom, including its existence and statistics. The source code for nocom was released in February 2022 dating back to Leijurv's involvement in March 2020.

## Overview and flaw of exploit
Nocom utilizes a flaw in [PaperMC](https://papermc.io/) for *Minecraft* 1.12.2, introduced in a [patch](https://github.com/PaperMC/Paper/blob/ver/1.12.2/Spigot-Server-Patches/0196-Fix-block-break-desync.patch). As it is a flaw within the PaperMC server software, said flaw does not exist in vanilla *Minecraft*. The patch, titled "Fix block break desync" , was implemented in July 2018 by Paper team member electronicboy, and added the following line of code:

<syntaxhighlight lang="java">
if (worldserver.isChunkLoaded(blockposition.getX() >> 4, blockposition.getZ() >> 4, true)) // Paper - Fix block break desync - Don't send for unloaded chunks
</syntaxhighlight>

The patch changes the behavior of *Minecraft* servers running Paper; when a player sends a packet mining a block that is in an unloaded chunk, a packet is not sent back to the player. This could, in turn, allow a player to determine if a chunk is loaded or not, dependent on if the server returns a response.

### Initial ghost block patch and lag exploit
]]
In vanilla *Minecraft*, a <code>CPacketPlayerDigging</code> packet is simply ignored entirely when it is over six blocks away from the player. However, due to lag, the server and client can disagree on where the player is. It is possible, then, for some good-faith block digging packets to be discarded by this policy. Since the server simply ignores the client, a "ghost block" is created, where the block exists on the server's end, but not the client's.

In January 2017, a user known as prplz submitted [a pull request](https://github.com/PaperMC/Paper/pull/575) to fix this issue, by sending a <code>PacketPlayOutBlockChange</code> packet when a player attempts to mine a block more than six blocks away, resolving the server-client ghost block dispute. The pull request adds the following line to the <code>PlayerConnection.java</code> file:{{CiteGeneral |url=https://github.com/PaperMC/Paper/pull/575 |title=Fix block break desync |author=prplz |publisher=GitHub |date=January 8, 2017}}

<syntaxhighlight lang="java">
this.sendPacket(new PacketPlayOutBlockChange(worldserver, blockposition)); // Paper - Fix block break desync
</syntaxhighlight>

By sending a packet for each block change, the patch created a vulnerability within Paper. To send the <code>PacketPlayOutBlockChange</code> packet back to the user, the server needs to load the chunk at the block position specified by the constructor. As loading chunks increases the computational load of a *Minecraft* server, sending continuous <code>CPacketPlayerDigging</code> packets to blocks at unloaded chunks creates immense server lag.

### Coordinate exploit
In July 2018, [0x22](https://2b2t.miraheze.org/wiki/0x22) and [Babbaj](https://2b2t.miraheze.org/wiki/Babbaj) created a coordinate exploit, using the groundwork laid out in the lag exploit. The two theorized that, if the server didn't return a response for unloaded chunks, but returned a response for loaded chunks, the rough location of players in 2b2t could be approximated. However, prplz's patch returned a response regardless of whether a chunk was loaded or unloaded, requiring a second patch to Paper that would only return a response if the chunk was loaded.

Knowing that the issue would be resolved if Hausemaster reported it to Paper, likely through the method they laid out, 0x22 and Babbaj began intentionally, repeatedly, and blatantly sending <code>CPacketPlayerDigging</code> packets, causing the Paper watchdog process to output a stack trace, which included the line added by prplz. Hausemaster reported the issue on July 11, 2017,{{CiteGeneral |url=https://github.com/PaperMC/Paper/issues/1203 |title=odd crash/hang |author=ghost |publisher=GitHub |date=July 11, 2018}} and the issue was fixed by electronicboy the following day by only returning a response for loaded chunks.{{CiteGeneral |url=https://github.com/PaperMC/Paper/commit/73b214a51571490249c92b8518758d66c8983743 |title= Don't send digged block updates for unloaded chunks |author=electronicboy |publisher=GitHub |date=July 12, 2018}} The commit added a check—{{#tag:syntaxhighlight|if (worldserver.isChunkLoaded(blockposition.getX() >> 4, blockposition.getZ() >> 4, true))|lang=rust|inline=1}}—if a player is in a loaded chunk.

Following the patch, a player could obtain the status of a chunk by attempting to break a block within the chunk. If the chunk is unloaded, the server returns nothing; if the chunk is loaded, the server returns a <code>SPacketBlockChange</code> packet and the block type of the block the player attempted to break, regardless of if the player loaded that chunk themselves.

{| class="wikitable"
|+ Summary of responses returned by <code>CPacketPlayerDigging</code>
|-
!
! Vanilla *Minecraft* server
! January 2017 patch
! July 2018 patch
|-
! Less than 6 blocks away
| colspan="3" | The block is broken and the <code>PacketPlayOutBlockChange</code> packet is sent.
|-
! More than 6 blocks away and in a currently loaded chunk
| rowspan="2" | No response is sent.
| colspan="2" | The server returns the block at that coordinate, but does not break the block.
|-
! More than 6 blocks away and not in a currently loaded chunk
| The server loads the chunk or generates it from the seed and returns the block at that coordinate, but does not break the block.
| No response is sent.
|}
The block detection mechanism of nocom was not a novel approach; [Orebfuscator](https://www.spigotmc.org/resources/orebfuscator-anti-x-ray.82710/), a server plugin designed to combat X-ray techniques, obscures the contents of a block until a player approaches it, and used this technique before electronicboy's patch.{{CiteGeneral |url=https://github.com/lishid/Orebfuscator/blob/dc9fb65c9e5ad65dae06fd5545554691461f445a/v1_12_R1/src/main/java/com/lishid/orebfuscator/nms/v1_12_R1/ChunkManager.java |title=Orebfuscator/ChunkManager.java |publisher=GitHub |date=May 15, 2017}}

### Initial implementation
 created the initial nocom exploit]]
On July 13, 2018, [Hausemaster](https://2b2t.miraheze.org/wiki/Hausemaster) implemented electronicboy's patch into 2b2t. [Fr1kin](https://2b2t.miraheze.org/wiki/Fr1kin), a member of [Nerds Inc](https://2b2t.miraheze.org/wiki/Nerds_Inc), created a [ForgeHax](https://github.com/fr1kin/ForgeHax) exploit to search chunks in 2b2t in a spiral pattern, writing down coordinates to a file and in chat. The contents of this file were uploaded to a website visible to members of Nerds Inc. A bot using [Baritone](https://2b2t.miraheze.org/wiki/Baritone) was set up, and chunks could be downloaded for remote viewing. Using mixin to alter chunk rendering in freecam, a module could remotely load a base using nocom.{{CiteGeneral |url=https://www.youtube.com/watch?v=HVxfxq_OQBY |title=The Fast Cast - NOCOM Exploit |author=The Fast Cast |publisher=YouTube |date=July 26, 2021 |name=Podcast}} This technique was used until late 2019, when Hausemaster implemented a packet rate limit, preventing brute force attempts to calculate coordinates.{{CiteGeneral |url=https://github.com/nerdsinspace/nocom-explanation/blob/main/README.md |title=nocom-explanation/README.md |author=[Leijurv](https://2b2t.miraheze.org/wiki/Leijurv) |publisher=GitHub |date=July 23, 2021 |name=Explanation}} In addition, the spiral technique had several drawbacks; most notably, large bases were indistinguishable from dirt huts.{{CiteGeneral |url=https://www.youtube.com/watch?v=elqAh3GWRpA |title=The Fall of Minecraft's 2b2t |author=[FitMC](https://2b2t.miraheze.org/wiki/FitMC) |publisher=YouTube |date=July 24, 2021 |name=Fit}}

### Leijurv's additions
[Leijurv](https://2b2t.miraheze.org/wiki/Leijurv), the lead developer of Baritone, joined the project in March 2020. Leijurv implemented an adaptive tracking system to tactfully determine precise coordinates for a player. To achieve this, dozens of bots were used in the overworld and the [Nether](https://2b2t.miraheze.org/wiki/Nether), with offset shift schedules to ensure uptime. Bots in the Nether mainly observed the [Nether highways](https://2b2t.miraheze.org/wiki/Nether_highways), tracking players and coordinating with the overworld bots. nocom tracked the time a player spent in one location; this was used to mark chunks where a player had spent more than 90 minutes at. These statistics were tracked in a [PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL) database and analyzed through direct queries and a web UI.

Players were located through straight-line checks on every axis and diagonal highway in the Nether, in a process that would take 33 minutes.{{CiteGeneral |url=https://github.com/nerdsinspace/nocomment-master/blob/master/src/main/java/nocomment/master/scanners/HighwayScanner.java |title=nocomment-master/HighwayScanner.java |publisher=GitHub}} After being located, a [Monte Carlo particle filter](https://en.wikipedia.org/wiki/Particle_filter#Monte_Carlo_filter_and_bootstrap_filter) was used to keep up with the player. nocom's implementation of a Monte Carlo particle filter simulates 1,000 different potential player positions and velocities, referred to as "particles". As players traveled in the Nether, the Monte Carlo particle filter improved, furthered by the low-degree in variance in player movement. To guess a location, sequential importance sampling was used.{{CiteGeneral |url=https://github.com/nerdsinspace/nocomment-master/blob/master/src/main/java/nocomment/master/tracking/MonteCarloParticleFilterMode.java#L335-L362 |title=nocomment-master/MonteCarloParticleFilterMode.java |publisher=GitHub}} The adaptive tracking system works using the following equation.

: <math> \int f(x_k) p(x_k|y_0,\dots,y_k) dx_k \approx \sum_{i=1}^N w_k^{(i)} f(x_k^{(i)}).</math>

Four main scanners were used: a Nether highway scanner, a ring scanner, a spiral scanner, and a cluster retry scanner. These scanners were assigned different priorities; the Nether highway scanner, for instance, was given mid-priority, while the spiral scanner received the lowest priority, with each bot running through each scanner in priority order.{{CiteGeneral |url=https://github.com/nerdsinspace/nocomment-master/blob/master/src/main/java/nocomment/master/tracking/TrackyTrackyManager.java#L35-L67 |title=nocomment-master/TrackyTrackyManager.java |publisher=GitHub}} Priorities were used to handle Hausemaster's packet limit. A central manager, dubbed the "tracky tracky manager", coordinated these scanners, and implemented a Monte Carlo particle filter for each new player. The cluster retry scanner rechecked bases at random.

To analyze the data from nocom, an aggregator analyzed the hits (loaded chunks). Once a chunk was loaded for more than five minutes, it was added to a GiST index and labeled as a node. High-activity areas were labeled as "core" nodes, and core nodes created clusters that could be combined with other clusters, creating a [disjoint-set data structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure). Path compression and unions were implemented by rank. Simultaneously, an associator used this data with player log-offs. Clusters were also used by a "slurper", which allowed Nerds Inc to download bases. Using "chunk seeding", a base could be determined in a chunk. Blocks, such as shulker boxes, stained glass, beacons, and chests, were used to determine if a chunk is a base, and nocom would then recreate the chunk in a separate instance of *Minecraft*.

nocom was deployed on a [DigitalOcean](https://en.wikipedia.org/wiki/DigitalOcean) droplet located in New York to ensure the lowest amount of latency between the bots and 2b2t's servers. A version of *Minecraft* was deployed on the servers using a single instance of Java. Bots were coordinated in a network. The status of the bots was visible in [Grafana](https://en.wikipedia.org/wiki/Grafana) in a [Docker container](https://en.wikipedia.org/wiki/Docker_(software)) with [WireGuard](https://en.wikipedia.org/wiki/WireGuard).

### Imitations
The [Infinity Incursion](https://2b2t.miraheze.org/wiki/Infinity_Incursion) were able to recreate nocom and implemented it within their cheating clients. The Infinity Incursion would use their exploit against [Fit](https://2b2t.miraheze.org/wiki/Fit), and attempted to sell his logout coordinates for real-world money.

## Impact
's coordinates were exposed through nocom]]
nocom observed 3,250,000 player sessions and 300,000 unique players. Using its definition of a base, 15,000 bases were tracked, of which two thirds had a world download. These world downloads have the full block-by-block timeline of the base's history at 30 minute intervals. This was only done for bases hundreds of thousands of blocks away from spawn. 400,000 "association events" were tracked, where a player logged out at a tracked base. The table of blocks has over 10,000,000,000 rows, and took up over a terabyte for the table and its associated indexes. The table of hits, has 3,000,000,000 rows, while the table of tracks, which is a grouping of hits into which ones were collected as a part of one continuous track, has 10,000,000 rows.

### Use in griefing
nocom has been attributed to the destruction of multiple bases and structures, including [Space Valkyria 3 V2](https://2b2t.miraheze.org/wiki/Space_Valkyria_3_V2), [Valerian](https://2b2t.miraheze.org/wiki/Valerian), [Hopen](https://2b2t.miraheze.org/wiki/Hopen), [Avalonia](https://2b2t.miraheze.org/wiki/Avalonia), [Yggdrasil](https://2b2t.miraheze.org/wiki/Yggdrasil), [Niflheim](https://2b2t.miraheze.org/wiki/Niflheim), [Acheron](https://2b2t.miraheze.org/wiki/Acheron), and [Victoria](https://2b2t.miraheze.org/wiki/Victoria). Coordinates for certain bases were leaked on [r/2b2t](https://2b2t.miraheze.org/wiki/r%2F2b2t) under the guise of the "Dipper Nation", a facetious redneck group.

### Spawnmasons
0x22, Babbaj, and Leijurv used their access to nocom to find stashes, the locations of which would be shared with the [Spawnmasons](https://2b2t.miraheze.org/wiki/Spawnmasons). Notably, [Dectonic](https://2b2t.miraheze.org/wiki/Dectonic) obtained hundreds of coordinates through Leijurv.

### Use on other anarchy servers
nocom was used on other anarchy servers, including [Constantiam](https://2b2t.miraheze.org/wiki/Constantiam) and 9b9t.

## Legacy
]]
nocom was patched in July 2021, and Nerds Inc released a write-up of nocom several days later. The source code for nocom was released on February 8, 2022.

The release of nocom's heatmap allowed [MAC_TONIGHT_](https://2b2t.miraheze.org/wiki/MAC_TONIGHT_), a base hunter, to locate various bases detected by nocom and archive them.{{CiteGeneral |url=https://www.youtube.com/watch?v=oCYRzF4rBRI |title=How This Public Image was Used to Find 1000s of 2b2t Bases |author=[SalC1](https://2b2t.miraheze.org/wiki/SalC1) |publisher=YouTube |date=September 9, 2021}}

## Notes
## References