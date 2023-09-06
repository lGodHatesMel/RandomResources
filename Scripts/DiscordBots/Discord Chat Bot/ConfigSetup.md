# Configuring the Bot

Before you can run the bot, you'll need to configure it by editing the config.json file. If you haven't already, you can start by renaming the `Example-config.json` file to `config.json` to ensure it's properly recognized by the bot.

## config.json Structure
The config.json file follows a specific structure that you should adhere to when customizing it for your bot. Below, we'll explain each section and what you should add or modify:

## token
Replace "YOUR_BOT_TOKEN_HERE" with your bot's Discord token. You can obtain a bot token by creating a bot on the Discord Developer Portal.

## command_prefix
Set the desired command prefix for your bot. By default, it is set to "!". This is the character that users will use to invoke commands (e.g., !help).

## target_channels
Under this section, you can configure the channels where the bot will send messages at specified intervals. You can add or modify channels and their corresponding messages as needed.

"channel_1" and "channel_2": These are examples of channels. Replace "CHANNEL_ID_1" and "CHANNEL_ID_2" with the actual channel IDs where you want messages to be sent.

"server_announcements": This is an example of a server announcements channel. Replace "YOUR_SERVER_ANNOUNCEMENTS_CHANNEL_ID" with the actual channel ID where you want server announcements to be sent.

For each channel, you can define an array of messages. Each message should have a "message" (the content of the message) and an "interval" (the time in seconds between sending each message).

## target_timestamp
Set the target_timestamp to the Unix timestamp of a specific date and time. The bot will display a countdown to this timestamp in the designated countdown channel.

## countdown_channel_id
Replace "CHANNEL_ID_FOR_COUNTDOWN" with the actual channel ID where you want the countdown timer to be displayed.

## Save Your Changes
After customizing the config.json file, save your changes. These configurations will be used by the bot when you run it.