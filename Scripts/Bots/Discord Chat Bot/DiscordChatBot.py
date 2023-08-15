import discord
import asyncio
import json

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

config = load_config()
bot_token = config['token']
command_prefix = config['command_prefix']
target_channels = config['target_channels']

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    await send_messages()

async def send_messages():
    while True:
        for channel_name, channel_data in target_channels.items():
            channel_id = channel_data['id']
            messages = channel_data['messages']
            channel = client.get_channel(int(channel_id))
            if channel:
                for msg_data in messages:
                    await channel.send(msg_data['message'])
                    await asyncio.sleep(msg_data['interval'])
            total_interval = sum(msg_data['interval'] for msg_data in messages)
            await asyncio.sleep(total_interval)  # Sleep for the total interval

            # Sleep for an additional interval before restarting the sequence
            restart_interval = 10  # Adjust this interval as needed
            await asyncio.sleep(restart_interval)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_prefix):
        await handle_command(message)

async def handle_command(message):
    command = message.content[len(command_prefix):].lower()

    if command == 'help':
        await message.channel.send('Available commands: !help, !about, !ping, !announcement')

    elif command == 'about':
        await message.channel.send('I am a Discord bot. Feel free to ask questions!')

    elif command == 'ping':
        await message.channel.send('Pong!')

    elif command.startswith('announcement '):
        command_args = command.split(maxsplit=2)
        if len(command_args) >= 3:
            announcement_text = command_args[2]
            channel_name = command_args[1].lower()

            target_channel_data = next((channel for channel in target_channels.values() if channel['id'] == channel_name), None)
            if target_channel_data:
                target_channel_id = int(target_channel_data['id'])
                await send_announcement(target_channel_id, announcement_text)
            else:
                await message.channel.send('Invalid announcement channel. Use !announcement <channel_name> <message>')
        else:
            await message.channel.send('Invalid announcement command. Use !announcement <channel_name> <message>')


async def send_announcement(target_channel_id, announcement_text):
    channel = client.get_channel(target_channel_id)
    if channel:
        await channel.send(f'**{announcement_text}**')

def main():
    client.run(bot_token)

if __name__ == "__main__":
    main()