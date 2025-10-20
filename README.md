# Ephemeral
A Multiplayer Pygame RPG Game.

A work in progress, multiplayer and serverside stuff is not up and running yet.

## How to run

### Dependencies

#### Pygame (Required)

Get the pygame module (Ephemeral is developed with pygame-ce, but pygame should work, if not look up how to install pygame-ce on your system)

In your terminal run `pip install pygame` follow any instructions (make sure pip is installed).

#### DiscordRPC (Optional)

This game has an optional dependency on the DiscordRPC module.

In your terminal run `pip install discordprc` follow any instructions (make sure pip is installed).

### Running the Game

To play, just run `menu.py` (this may break in the future, so hang on while I develop version 1).

#### Arguments

There are several command line arguments you can also pass in:

##### Options

--no-server: disables the use of server interaction (will render game unresponsive once everything is serverside)

##### Inputs

--port: force this port when joining a game
--address: what address to connect to when joining

## Running the Server

To run a server (singleplayer will start up it's own server so this is only for multiplayer) run the `server.py`

If you are running localhost you have to run the server with the `--localhost` option

The `--port` option specifies which port to use (overrides the default which is `2048`)

The `--client-max` option specifies how many connections can be waiting before they start being rejected

## Contributing

This game is not entirely ready for contributors.
Once a production structure is set up and the goals are more set in place, I plan to decide on how to move forward with the contribution side of things.
However at this point in time I will be developing this personally, anyone is free to give ideas and feedback, sending me code to try out also works if ideas aren't your thing.

## Discord Server

If you have ideas or want to talk about this game, there is a discord server.
You can also see updates and announcements on this server.
https://discord.gg/7HXHXJ8k9R

## Credits

Credit where credit is due...

Thanks to TX_Miner for tons of help with the serialization protocol and helping me code when my brain is dead.
Also thanks to everyone who did playtesting, network testing, etc. It's been a huge help.

Thanks for my Dad helping me think through some of the tough issues.
