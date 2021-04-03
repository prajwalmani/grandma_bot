import discord
import os
import requests
import json
from keep_alive import keep_alive

client = discord.Client()


def get_quote():
    # a function to generate random quotes using API
    qresponse = requests.get("https://zenquotes.io/api/random")
    q_json_data = json.loads(qresponse.text)
    quote = '"' + q_json_data[0]['q'] + '"' + " \nBy " + q_json_data[0]['a']
    return (quote)


def get_poem(linescount):
    if linescount == 0:
        url = "https://poetrydb.org/random/1/title,author,lines.text"
    else:
        url = 'https://poetrydb.org/random,linecount/1;{0}/title,author,lines.text'.format(
            linescount)
    presponse = requests.get(url)
    strg = presponse.text
    s = strg.splitlines()
    title = s[1]
    author = s[3]
    url = "https://poetrydb.org/title,author/{0};{1}/lines.json".format(
        title, author)
    presponse = requests.get(url)
    p_json_data = json.loads(presponse.text)
    try:
        jlines = p_json_data[0]["lines"]
    except KeyError:
        get_poem(linescount)
    lines = "\n".join(jlines)

    poem = "**Title**:{0}\n**Author**:{1}\n**Poem**:\n{2}".format(
        title, author, lines)
    return poem


def get_joke(flag):
    if flag == 0:
        url = "https://official-joke-api.appspot.com/random_joke"
        jresponse = requests.get(url)
        jokes_data = json.loads(jresponse.text)
        joke="{0}\n{1}".format(jokes_data['setup'],jokes_data['punchline'])
        return joke 
    else:
        url = "https://official-joke-api.appspot.com/jokes/programming/random"
        jresponse = requests.get(url)
        jokes_data = json.loads(jresponse.text)
        jokes_data = json.loads(jresponse.text)
        joke="{0}\n{1}".format(jokes_data[0]['setup'],jokes_data[0]['punchline'])
        return joke 


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        pass
    if message.content.startswith('grandma inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    if message.content.startswith('grandma poem'):
        msg = str(message.content)
        if (any(chr.isdigit() for chr in msg)):
            linescount = msg[13]
        else:
            linescount = 0
        poem = get_poem(linescount)
        await message.channel.send(poem)
    if message.content.startswith('grandma jokes'):
        joke = get_joke(0)
        await message.channel.send(joke)
    if message.content.startswith('grandma pjokes'):
        joke = get_joke(1)
        await message.channel.send(joke)


keep_alive()


client.run(os.getenv('TOKEN'))
