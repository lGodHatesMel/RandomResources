# Configuring the Bot

## config.json

If the config.json file doesn't exist, the bot will create it with default values when you run it for the first time.

Open config.json and edit it:

"token": Replace "YOUR_TOKEN_HERE" with your Discord Bot Token.
"prefix": Change "!" to your desired command prefix.
"enable_countdown": Set true to enable countdown functionality, or false to disable it. If not needed, leave it as false.
"countdown_channel_id": If "enable_countdown" is true, specify the Discord channel ID for countdown messages. If not needed, leave it as null.
"target_timestamp": If "enable_countdown" is true, specify the target UNIX timestamp for countdown events. If not needed, leave it as null.
Save config.json after making changes.

# Discord Bot Countdown

## Overview

The Countdown Bot is a feature for your Discord bot that allows you to set up countdown timers with customizable messages. This guide explains how to set up and configure the Countdown Cog for your bot.

## Configuration

To configure the Countdown Cog, follow these steps:

1. Open the `config.json` file in your bot's root directory.

2. Configure the countdown settings within the `config.json` file:

   - `"enable_countdown"`: Set this to `true` to enable the countdown feature or `false` to disable it.

   - `"countdown_channel_id"`: If `"enable_countdown"` is `true`, specify the Discord channel ID where countdown messages will be sent. You can find a channel's ID by right-clicking the channel and selecting "Copy ID." If you don't want to use this feature, leave it as `null`.

   - `"target_timestamp"`: If `"enable_countdown"` is `true`, specify the target UNIX timestamp for when the countdown should end. You can use an online timestamp converter to generate this value. If you don't want to use this feature, leave it as `null`.

3. Save the `config.json` file after making changes.

