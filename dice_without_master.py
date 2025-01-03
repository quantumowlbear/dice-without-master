# Instruction for use:
# First install the python libraries:
#	pip3 install discord
# 	pip3 install dotenv
# Then put in your discord token:
# 	open/create the .env file in the same directory as this file and put in your discord token, e.g. DISCORD_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
# To use in discord channel:
#   !overtone - roll for the overtone
#   !rogue  - normal roll

# dice_wihtout_master.py
import os
import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

overtone = "Jovial"

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

def flip_overtone():
    global overtone

    # we flip the overtone
    if overtone == "Jovial":
        overtone = "Glum"
    else:
        overtone = "Jovial"


@client.event
async def on_message(message):
    global overtone

    if message.author == client.user:
        return

    if message.content == '!overtone':
        jovial = random.randint(1, 6)
        glum = random.randint(1, 6)

        dice_image = 'dice_images/g%dj%d.gif' % (glum, jovial)
        await message.channel.send(file=discord.File(dice_image))

        if jovial > glum:
            overtone = "Jovial"
        elif jovial < glum:
            overtone = "Glum"
        else:
            flip_overtone()
        response = "The **Overtone** is **%s**\n" % overtone
        await message.channel.send(response)

    elif message.content == '!demo':
        await read_the_bones(message, 5, 4)
        await read_the_bones(message, 2, 6)
        await read_the_bones(message, 4, 4)
        await read_the_bones(message, 2, 2)
        await read_the_bones(message, 3, 1)

    elif message.content == '!rogue':
        jovial = random.randint(1, 6)
        glum = random.randint(1, 6)

        await read_the_bones(message, jovial, glum)


async def read_the_bones(message, jovial, glum):
    global overtone

    dice_image = 'dice_images/g%dj%d.gif' % (glum, jovial)
    await message.channel.send(file=discord.File(dice_image))

    response = ""
    # response += "Jovial: %d, Glum: %d\n" % (jovial, glum)
    if jovial > glum:
        tone = "Jovial"
        response += "The **Tone** is **Jovial**.\n"
        if jovial <=3 and glum <= 3:
            response += "In addition, a **Moral** is made! There is an unintended consequence and a lesson\n"
    elif jovial < glum:
        tone = "Glum"
        response += "The **Tone** is **Glum**.\n"
        if jovial <=3 and glum <= 3:
            response += "In addition, a **Moral** is made! There is an unintended consequence and a lesson\n"
    else:
        # we have a Stymie
        response += "A **Stymie**! There is an escalation. You are temporarily unable to you goal: this can be a setback, a tactical slip, or momentary oversight or an outright failure. The Overtone is flipped, and the change in tone is part of the escalation.\n"
        flip_overtone()

        if jovial <= 3:
            # we have a mystery
            response += "In addition, this is a **Mystery**! The reasons you are thwarted is of unknown or of supernatural origin.\n"

    response += "The **Overtone** is **%s**\n" % overtone
    await message.channel.send(response)


client.run(TOKEN)


