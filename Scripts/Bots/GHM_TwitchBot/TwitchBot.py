import json
import asyncio
import datetime
from twitchio.ext import commands

bot_token = "hbanqkp81rzfi4tuny6j3esvspth9k"
joinChannel = "lgodhatesmel"
prefix = "!"

example_messages = [
    {
        "message": "Hello, everyone!",
        "pause": 5
    },
    {
        "message": "I hope you're enjoying the stream.",
        "pause": 3
    }
]

example_commands = {
    "ping": "Pong!",
    "requestlist": "Here is the link to the request list: "
}

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=bot_token, prefix=prefix, initial_channels=[joinChannel.lower()],case_insensitive=True,)

    async def send_messages(self):
        while True:
            try:
                with open('messages.json', 'r') as f:
                    messages_data = json.load(f)
            except FileNotFoundError:
                with open('messages.json', 'w') as f:
                    json.dump(example_messages, f, indent=4)
                print("messages.json created with example data.")
            else:
                print("messages.json already exists.")
    
            for data in messages_data:
                message = data.get('message', '')
                pause_minutes = data.get('pause', 0)
                if message:
                    channel = bot.get_channel(joinChannel)
                    await channel.send(message)
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{current_time}] Message sent:", message)
        
                if pause_minutes > 0:
                    await asyncio.sleep(pause_minutes * 60)
    
            await asyncio.sleep(1)

    async def send_commands(self):
        try:
            with open('commands.json', 'r') as f:
                commands_data = json.load(f)
        except FileNotFoundError:
            with open('commands.json', 'w') as f:
                json.dump(example_commands, f, indent=4)
            print("commands.json created with example data.")
            commands_data = example_commands  # Use example_commands if file doesn't exist
        else:
            print("commands.json already exists.")
        defined_commands = set()
        for command, response in commands_data.items():
            if response and command not in defined_commands:
                @self.command(name=command)
                async def dynamic_command(ctx, response=response):  # Pass response as a default argument
                    await ctx.send(response)
                defined_commands.add(command)
    
        await asyncio.sleep(1)
    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        await asyncio.gather(
            self.send_messages(),
            self.send_commands()
        )
bot = Bot()
bot.run()