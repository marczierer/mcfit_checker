import requests
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime

class McFit:
    def __init__(self):
        self.webhook_url = "INPUT_DISCORD_WEBHOOK_HERE"
        self.studio_id = "1832288610"

    def run(self):
        while True:
            current_time = datetime.now().strftime("%H:%M")
            print(f'Status-Poll: Checking McFit Frequentation at {current_time}...')
            self.check_frequentation()
            time.sleep(1800)  # Sleep for 30 minutes (1800 seconds)

    def check_frequentation(self):
        url = f'https://www.mcfit.com/de/auslastung/antwort/request.json?tx_brastudioprofilesmcfitcom_brastudioprofiles%5BstudioId%5D={self.studio_id}'
        response = requests.get(url)
        data = json.loads(response.text)

        now = datetime.now()
        current_hour = now.strftime("%H")

        for item in data['items']:
            if item['startTime'][:2] == current_hour:
                current_percentage = item['percentage']
                if current_percentage <= 50:
                    self.occupancy_status = "Frei :green_square:"
                elif current_percentage < 80:
                    self.occupancy_status = "Teilweise belegt :yellow_square:"
                else:
                    self.occupancy_status = "Voll belegt :red_square:"

                break

        print(f"Status-Poll: Aktuelle Auslastung von McFit: {current_percentage}%")
        self.send_webhook(current_percentage)
        print('Status-Update: User got notified via Discord.')

    def send_webhook(self, current_percentage):
        TITLE = 'McFit Auslastung'

        now = datetime.now()
        current_time = now.strftime("%H:%M")
        opening_time = '00:00:00'
        closing_time = '00:00:00'
        
        status = 'Geöffnet :white_check_mark: '

        embed = DiscordEmbed(title=TITLE, color='ffff00 ')
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/6/6b/McFit_Logo.png')
        embed.set_footer(text="McFit GmbH", icon_url="https://cdn.discordapp.com/attachments/1073359084843192381/1086087563716083792/McFIT_App_Logo.png")
        embed.set_timestamp()
        embed.add_embed_field(name='Auslastung', value=f"{current_percentage}%")
        embed.add_embed_field(name='Status', value=self.occupancy_status)
        embed.add_embed_field(name='Verfügbarkeit', value=status)
        embed.add_embed_field(name='Aktuelle Zeit', value=current_time)
        embed.add_embed_field(name='Öffnungzeiten', value='Mo-So: 0:00 - 0:00')

        webhook = DiscordWebhook(url=self.webhook_url, rate_limit_retry=True)
        webhook.add_embed(embed)
        webhook.execute()

if __name__ == '__main__':
    mcfit = McFit()
    mcfit.run()
