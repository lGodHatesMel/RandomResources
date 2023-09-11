import os
from twitchio.ext import commands
import simpleaudio as sa

# Set up the bot
bot = commands.Bot(
    irc_token='your-irc-token-here',
    client_id='your-client-id-here',
    nick='',
    prefix='!',
    initial_channels=['your-channel']
)

# Set the path to the folder containing the sound files
sound_folder = ''

redemption_sounds = {
    'PikaPika': 'PikaPika.mp3',
    'Pikachu': "Pikachu.mp3"
}

# Listen for channel point redemptions
@bot.event
async def event_raw_data(self, data):
    print(f"Raw data: {data}")  # Print the raw data received from Twitch
    if 'type' in data.keys():
        if data['type'] == 'reward-redeemed':
            redemption_name = data['data']['redemption']['reward']['title']
            print(f"Redemption name: {redemption_name}")  # Print the redemption name
            print(f"Redemption sounds: {redemption_sounds}")  # Print the redemption sounds dictionary
            if redemption_name in redemption_sounds.keys():
                sound_file = os.path.join(sound_folder, redemption_sounds[redemption_name])
                wave_obj = sa.WaveObject.from_wave_file(sound_file)
                wave_obj.play()

bot.run()
