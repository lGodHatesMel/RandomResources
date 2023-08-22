# Twitch Chat Bot

This is a simple Twitch Chat Bot script that sends timed messages in a Twitch chat room.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/lGodHatesMel/RandomResources.git

2. Install the required dependencies. You can use the following command:
   pip install irc

## Configuration

1. Rename the EXAMPLE-config.json file to config.json.

2. Edit the config.json file and provide your bot's information:
  
  Make sure for "channel_name": "#YOURCHANNELNAME" there is a # infront of YOURCHANNELNAME

3. Add your custom messages to the messages list. 
   Each message should have a `message`, `interval_minutes`, and `message_count` property.

## Usage

1. Run the script using the following command:
   ```bash
   python TwitchChatBot.py

   
The bot will connect to the Twitch chat using the provided credentials and start sending messages at the specified intervals.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.






