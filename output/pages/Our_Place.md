*Our/Place was a ten day-long event held by the [Ancients](https://2b2t.miraheze.org/wiki/Ancients) from the 16th of May, 22 through the 25th of May that was inspired by Reddit's r/Place.*
## History
### Functionality & Setup
Our/Place connected a website interface to baritone bots that allowed players to create a collective mapart in real time. Within the 10 days the system was active, over a quarter-million pixels were placed by 847 players. 25GB of data transmitted throughout the project with a maximum of 12 bots running at one time.

The website was coded by [minecraft_simon](https://2b2t.miraheze.org/wiki/minecraft_simon) and the baritone bots were coded by [Rules_Off](https://2b2t.miraheze.org/wiki/Rules_Off). Once a bot starts it connects to the our/place website (server) and will start sharing information like its location, rotation, and inventory. When someone places a pixel on the website, that action will be added as a job on the server. The connected bots will constantly fetch the latest jobs based on their positioning and inventory. As long as there are jobs available the bots will keep on working. For every job the following logic is being executed: - Navigate to the specified pixel - Break the old block - Place the new block - Verify the placement and color - Pick up the old item that dropped on the ground Once the job queue is empty they will move off the map-art and wait in the corner until a new job is available. This process can be interrupted when the inventory gets too full or too many different colors are missing. The bot will then move to the closest chest area to deposit/grab items and balance its inventory.

#### Construction
As for the surrounding build, an entire chunk from the overworld was built in the end to allow streaming. That way, no one could successfully hunt for the project, and throw off players that tried to locate it. The Overworld chunk was located at -14202100, -14202100 based on the original date of r/Place. Built largely by [Hovecs](https://2b2t.miraheze.org/wiki/Hovecs) and [chiekn](https://2b2t.miraheze.org/wiki/chiekn), assisted by [xrayessay](https://2b2t.miraheze.org/wiki/xrayessay), [Rules_Off](https://2b2t.miraheze.org/wiki/Rules_Off), and [YoMoBoYo](https://2b2t.miraheze.org/wiki/YoMoBoYo). Our/Place was located a thousand blocks away from the -10 Million, -10 Million Ancient monument. [Harrissssonn](https://2b2t.miraheze.org/wiki/Harrissssonn) traveled there, using the boat tp exploit to transport the remaining [Ancients](https://2b2t.miraheze.org/wiki/Ancients).

## Community Involvement
Active community involvement was an integral component of Our/Place. The interactive website offered a simple and engaging way of placing pixels and contributing to the event.

This design choice attracted notable communities to made contributions. Many 2b2t groups like [SBA](https://2b2t.miraheze.org/wiki/Spawn_Builders_Association), The [Spawnmasons](https://2b2t.miraheze.org/wiki/SpawnMasons), and [Astral Brotherhood](https://2b2t.miraheze.org/wiki/Astral_Brotherhood) placed their logos, but the strongest force was the Hungarian Twitch Streamer [VBence](https://2b2t.miraheze.org/wiki/VBence) and his community.

With the launch of the project, people started working on scripts to automate pixel-placement on our/place. After a few days, the user ElectroY Modz succeeded by modifying a script that he previously used for botting reddit.com/r/place. This way, he was able to bring 48 alt-accounts online to place pixels and dominate any area he wanted to. [minecraft_simon](https://2b2t.miraheze.org/wiki/minecraft_simon) stayed in contact with him and made sure the bots would only be active in a limited area, so as to not disturb the other players.

The event concluded where every pixel converted into a custom mapart. This final mapart displayed the top 5 players who placed the most pixels.

<gallery>
File:Ourplace1.png|The Builders of Our/Place
File:TheEndOurPlace.png|Our/Place in The End
</gallery>