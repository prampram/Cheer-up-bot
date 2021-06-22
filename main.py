import os
import discord
import requests
import json
import random
from replit import db


client=discord.Client() 

sad_words = ["sad","depressed","unhappy"]
starter_encouragements=["cheer up",
"Hang in there",
"You are a great person"
]



def get_quote():
  response= requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+" -"+json_data[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.appen(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragement(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements


@client.event
async def on_ready():
  print ('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author==client.user:
    return

  msg=message.content

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
  if message.content.startswith('$inspire'):
    quote=get_quote()
    await message.channel.send(quote)

    options=starter_encouragements
    if "encouragements" in db.keys():
      options=options+db["encouragements"]


  if any (word in message.content for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

  if msg.startswith("$new"):
    encouraging_message=msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging_message added.")

    if msg.startswith("$del"):
      encouragemnts=[]
      if "encouragemnts" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_encouragement(index)
        encouragemnts=db["encouragemnts"]
      await message.channel.send(encouragements)



client.run(os.environ['TOKEN'])



