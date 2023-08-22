import irc.bot
import json
import datetime
import threading

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, oauth_token, bot_username, messages):
        self.channel = channel
        self.oauth_token = oauth_token
        self.bot_username = bot_username
        self.messages = messages
        self.current_message = 0
        self.message_count = 0
        server = 'irc.chat.twitch.tv'
        port = 6667
        super().__init__([(server, port, f'oauth:{oauth_token}')], bot_username, bot_username)

    def on_welcome(self, connection, event):
        self.send_message(connection, "Chat Bot Connected")
        self.schedule_messages(connection)

    def send_message(self, connection, message):
        connection.privmsg(self.channel, message)

    def send_scheduled_messages(self):
        while True:
            msg_data = self.messages[self.current_message]
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Sending message: {msg_data['message']}")
            self.connection.privmsg(self.channel, msg_data['message'])
            self.message_count += 1
            if self.message_count >= msg_data['message_count']:
                self.message_count = 0
                self.current_message = (self.current_message + 1) % len(self.messages)
            interval_seconds = msg_data['interval_minutes'] * 60
            threading.Event().wait(interval_seconds)

    def schedule_messages(self, connection):
        self.connection = connection
        threading.Thread(target=self.send_scheduled_messages).start()

def main():
    print("Shiny Ditto Chat Bot is starting...")
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    bot_username = config['bot_username']
    oauth_token = config['oauth_token']
    channel_name = config['channel_name']
    messages = config['messages']
    bot = TwitchBot(channel_name, oauth_token, bot_username, messages)
    bot.start()

if __name__ == "__main__":
    main()