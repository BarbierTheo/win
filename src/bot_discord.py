import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from app import get_classement, get_match_today
from datetime import datetime, date
from zoneinfo import ZoneInfo


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def create_match_message(match, classement):
    
    match_time_utc = datetime.fromisoformat(match['utcDate'].replace('Z', '+00:00'))
    match_time_local = match_time_utc.astimezone(ZoneInfo("Europe/London"))
    time_str = match_time_local.strftime("%H:%M")

    home = match['homeTeam']['name']
    away = match['awayTeam']['name']
    
    table_str =""
    for position, name, points in classement:
        if position <= 5:
            table_str += f"{position} - {name} - {points} points \n"

    message = (
        f"**🔥 - JOUR DE MATCH - 🔥**"
        f"   {home} - {away} à {time_str}"
        
        f"```text\n{table_str}```"
        )

    return message


match = get_match_today()
if match:

    classement = get_classement()   
    message = create_match_message(match, classement)
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Connecté en tant que : {client.user}')
    
        channel_id = 1421204347676524544  
        channel = client.get_channel(channel_id)
    
        if channel:
            await channel.send(message)
            await client.close()
            
        else:
            print("Channel non trouvé.")
            await client.close()

    client.run(TOKEN)
    print("Match du jour envoyé -", datetime.now(ZoneInfo("Europe/London")))
else:
    print("Pas de match aujourd'hui -", datetime.now(ZoneInfo("Europe/London")))
    
    
# print(create_match_message(match, classement))
# print(get_match_today())