=import discord
import os
import requests
import json
import random
import praw
from abuse import get_abuser
from keep_alive import keep_alive

client = discord.Client()

def get_help():
  help='''
  Grandma is here to help you out because she is multitalented!
  
  **Commands**
  `Prefix` : **g**
  `g info` : Basic info about the bot 
  `g meme` : Grandma will show you a random meme
  `g wmeme` : Grandma will show you a random wholesomememes
  `g ameme` : Grandma will show you a random doggo/catto meme
  `g food` : Grandma will give some food 
  `g money` : If you need some cash then grandma is there for you 
  `g inspire` : Grandma will tell you a motivational quote 
  `g poem`    : Grandma will tell you a random poem within 20 lines
  `g abuse` : Grandma will abuse you in a funny way
  `g jokes` : Grandma will tell you a random joke
  `g pjokes` : Grandma will tell you a random programming joke

  **PS: Grandma says "I dont spoil my grandkids. I'm just very accmodating"**
  '''
  emb=discord.Embed(description=help, color=0xee82ee)
  return emb

def get_info():
  emb=discord.Embed(color=0x0000ff)
  emb.description='''
  **Gradma bot is loving and cool just like your grandma!
  This bot was built in python 
  By : `Prajwal Mani` 
  [HERE IS THE GITHUB REPO.](https://github.com/prajwalmani/grandma_bot)
  Have some suggestions or want to help me out to build still more bigger bot then do a PR for the repo and let me know!**
  '''
  
  return emb

def get_reddit(subreddit_name):

  reddit=praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('SECRET_KEY'),
    username=os.getenv('username'),
    user_agent=os.getenv('user_agent'),
    check_for_async=False
  )

  subreddit=reddit.subreddit(subreddit_name)

  top=subreddit.top(limit=50)
  allsubs=[]
  for submissions in top:
    allsubs.append(submissions)
  
  random_sub=random.choice(allsubs)

  title=random_sub.title
  url=random_sub.url

  emb=discord.Embed(title=title, color=0xff0000)

  emb.set_image(url=url)
  
  return emb

def get_quote():
      # a function to generate random quotes using API
      qresponse = requests.get("https://zenquotes.io/api/random")
      q_json_data = json.loads(qresponse.text)
      quote = '"' + q_json_data[0]['q'] + '"' + " \nBy " + q_json_data[0]['a']
      return (quote)


def get_poem(linescount):
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
          
def get_food():
    title=["Eat up I know you are hungry",
          "You gonna stop eating when i tell you to stop eating",
          "If nothing is going well...maybe this food can cure it",
          "While your here, grab some food and charge up"
    ]
    emb=discord.Embed(title=title[random.randrange(0,4)], color=0x00ff00)
    file = discord.File("foodimages/food{0}.png".format(random.randrange(1,21)), filename="image.png")
    emb.set_image(url="attachment://image.png")
    return file,emb

def get_money():
  list=[
    'Here is some cash \U0001F4B0 buy what ever you want',
    'Dont tell anybody that I gave you the cash \U0001F4B0',
    'Here you go \U0001F4B0 buy something to eat '
  ]

  return list[random.randrange(0,3)]


@client.event
async def on_ready():
      print("{0.user} is live!!".format(client))
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for grandma help"))


@client.event
async def on_message(message):
      if message.author == client.user:
          pass
      if message.content.startswith('g help'):
          help=get_help()
          await message.channel.send(embed=help)
      if message.content.startswith('g info'):
          info=get_info()
          await message.channel.send(embed=info)
      if message.content.startswith('g inspire'):
          quote = get_quote()
          await message.channel.send(quote)
      if message.content.startswith('g poem'):
          linescount = random.randrange(1, 21)
          poem = get_poem(linescount)
          await message.channel.send(poem)
      if message.content.startswith('g jokes'):
          joke = get_joke(0)
          await message.channel.send(joke)
      if message.content.startswith('g pjokes'):
          joke = get_joke(1)
          await message.channel.send(joke)
      if message.content.startswith('g abuse'):
          abuse = get_abuser()
          await message.channel.send(abuse)
      if message.content.startswith('g meme'):
          emb = get_reddit("memes")
          await message.channel.send(embed=emb)
      if message.content.startswith('g wmeme'):
          emb = get_reddit("wholesomememes")
          await message.channel.send(embed=emb)
      if message.content.startswith('g ameme'):
          emb = get_reddit("AnimalMemes")
          await message.channel.send(embed=emb)
      if message.content.startswith('g food'):
          file,emb = get_food()
          await message.channel.send(file=file,embed=emb)
      if message.content.startswith('g money'):
          money = get_money()
          await message.channel.send(money)

keep_alive()

client.run(os.getenv('TOKEN'))
