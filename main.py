import discord
import os
import psutil
import time
import math
import datetime
import socket
from dotenv import load_dotenv

# used for uptime
def seconds_elapsed():
    return time.time() - psutil.boot_time()

uptime = math.trunc(seconds_elapsed())

last_reboot = psutil.boot_time()

last_reboot = datetime.datetime.fromtimestamp(last_reboot)

last_reboot = last_reboot.strftime("%Y-%m-%d %H:%M:%S")

#this basically runs the ram thing, it then uses it to convert it into the string it needs
ram = psutil.virtual_memory()
hdd = psutil.disk_usage('/')
cpu = psutil.cpu_percent(interval=0.4, percpu=False)

# may god forgive me for what you are about to witness
ram_embed = str(ram.percent) + "% " +  str('%.2f'%(ram.used/1073741824)) + "GB/" + str('%.2f'%(ram.total/1073741824)) + "GB"
hdd_embed = str('%.2f'%(hdd.used/1073741824)) + "GB"
hdd_embed_2 = str('%.2f'%(hdd.total/1073741824)) + "GB"

hostname = socket.gethostname()

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

uptime = str(convert(uptime))

load_dotenv()

#
TOKEN = os.getenv("TOKEN")

#i dont think i even needs this anymore but better safe than sorry
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
'''
cpu_usage = str(psutil.cpu_percent())

cpu = psutil.cpu_times_percent(interval=0.4, percpu=False)
print(cpu)'''

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    '''
    if message.content.startswith('$hello'):
     await message.reply('Hello!')

   elif message.content.startswith('$goodbye'):
     await message.reply('no') 
     '''

    if client.user in message.mentions:

        embed = discord.Embed(title="MarkMon - System stats")

        embed.add_field(name="Stats",
                        value="Uptime: " + uptime +"\nLast reboot: " + last_reboot + "\nHostname: " + hostname,
                        inline=False)
        embed.add_field(name="CPU",
                        value="Usage: " + str(cpu) + "%",
                        inline=False)
        embed.add_field(name="RAM",
                        value="Usage: " + ram_embed,
                        inline=False)
        embed.add_field(name="Storage",
                        value="Usage: " + hdd_embed + "\nMaximum storage: " + hdd_embed_2,
                        inline=False)
        '''
        embed.add_field(name="Network",
                        value="Upload: " + str(upload_speed) + "MB" + "\nDownload: " + str(download_speed) + "MB",
                        inline=False)
                        
                        will be added at a later date'''

        await message.reply(embed=embed)


client.run(TOKEN)