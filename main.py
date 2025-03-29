import discord
import os
import psutil
import time
import datetime
import socket
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Get CPU info
def get_cpu_info():
    cpu_info = {}
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if "model name" in line:
                cpu_info["name"] = line.split(":")[1].strip()
            elif "cpu MHz" in line:
                cpu_info["clock_speed"] = line.split(":")[1].strip() + " MHz"
            elif "vendor_id" in line:
                cpu_info["brand"] = line.split(":")[1].strip()
    return cpu_info
#THIS STUPID SHIT HAS TO BE HERE OR ELSE THE
#INDENTATION BREAKS IT, TRYING TO FIX THAT
#BREAKS ANOTHER FUNCTION, DO NOT TOUCH THIS
cpu_info = get_cpu_info()

# Calculate uptime and last reboot time
def get_uptime():
    elapsed = int(time.time() - psutil.boot_time())
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"

def get_last_reboot():
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

# Fetch system stats
def get_system_stats():
    ram = psutil.virtual_memory()
    hdd = psutil.disk_usage('/')
    cpu_usage = psutil.cpu_percent(interval=0.4, percpu=False)


    return {
        "uptime": get_uptime(),
        "last_reboot": get_last_reboot(),
        "hostname": socket.gethostname(),
        "cpu_usage": f"{cpu_usage}%",
        "ram_usage": f"{ram.percent}% ({ram.used / 1_073_741_824:.2f}GB / {ram.total / 1_073_741_824:.2f}GB)",
        "hdd_usage": f"{hdd.used / 1_073_741_824:.2f}GB",
        "hdd_total": f"{hdd.total / 1_073_741_824:.2f}GB"
    }

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        stats = get_system_stats()

        embed = discord.Embed(title="MarkMon - System Stats")
        embed.add_field(name="System", value=f"Uptime: {stats['uptime']}\nLast Reboot: {stats['last_reboot']}\nHostname: {stats['hostname']}", inline=False)
        embed.add_field(name="CPU", value=f"Usage: {stats['cpu_usage']}\n Model: {cpu_info.get('name')}\n Clock speed: {cpu_info.get('clock_speed')}", inline=False)
        embed.add_field(name="RAM", value=f"Usage: {stats['ram_usage']}", inline=False)
        embed.add_field(name="Storage", value=f"Used: {stats['hdd_usage']}\nTotal: {stats['hdd_total']}", inline=False)

        await message.reply(embed=embed)

client.run(TOKEN)
