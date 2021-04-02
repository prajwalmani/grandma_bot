import discord 
import os 
import requests
import json 
from keep_alive import keep_alive
import io

client=discord.Client()


def get_quote():
    # a function to generate random quotes using API
    qresponse=requests.get("https://zenquotes.io/api/random")
    q_json_data=json.loads(qresponse.text)
    quote='"'+q_json_data[0]['q']+'"'+" \nBy "+q_json_data[0]['a']
    return (quote)


def get_poem(linescount):
    if linescount == 0:
        url= "https://poetrydb.org/random/1/title,author,lines.text"
    else:
        url='https://poetrydb.org/random,linecount/1;{0}/title,author,lines.text'.format(linescount)
    presponse=requests.get(url)
    strg=presponse.text
    s=strg.splitlines()
    title=s[1]
    author=s[3]
    url= "https://poetrydb.org/title,author/{0};{1}/lines.json".format(title,author)
    presponse=requests.get(url)
    p_json_data=json.loads(presponse.text)
    jlines=p_json_data[0]["lines"]
    lines="\n".join(jlines)
    
    poem="Title:{0}\nAuthor:{1}\nPoem:\n{2}".format(title,author,lines)
    return poem

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        pass
    if message.content.startswith('grandma inspire'):
        quote=get_quote()
        await message.channel.send(quote)
    if message.content.startswith('grandma poem'):
        msg=str(message.content)
        if (any(chr.isdigit() for chr in msg)):
             linescount=msg[13]
        else:
            linescount=0
        poem=get_poem(linescount)
        await message.channel.send(poem)
        
keep_alive()


client.run(os.getenv('TOKEN'))