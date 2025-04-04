import discord
import os
import random
import tictactoe
import hangmann
import connectt4
import dotsboxes
from doge_utils import *


class Doge(discord.Client):
  help = "Seems like you want some help, xx. I'm your friendly assistant Doge! To interact with me, call out to me by my name and I'll respond to you. If you greet me, I will greet you back. You can tell me how you feel about me. I can help you make a wish\n\nI also offer a variety of games for you to play with your friends! You can play Tic Tac Toe, Hangman, Connect 4, or Dots and Boxes. Simply call out to me and say that you want to play one of these games!"

  greetings = [
      "hello", "hi", "hey", "hola", "bonjour", "konnichiwa", "aloha", "howdy"
  ]

  doge_love = [
      "I love you too, xx. :)", "You do, xx? :0",
      "You are the best pal ever, xx! :)", "Can we be together forever, xx?",
      "No one's ever said that to me before, xx. :)",
      "I don't know what to say, xx.",
      "I... don't feel the same way, xx. I'm sorry.",
      "If I weren't a bot, xx, I would stay with you forever."
  ]

  doge_insults = [
      "Did you really mean that, xx? :(", "Well xx, if that's how you feel...",
      "Is this... something you've been wanting to tell me for a long time, xx?",
      "If that's how you feel, xx, then I don't think we should be together anymore.",
      "Did you really just say that, xx?",
      "Yeah? Well you suck even more, xx.", "Don't talk to me again, xx.",
      "It's alright. No matter what, I'll always love you, xx. :)",
      "Why do you always have to hurt me, xx? :(", "Yeah? So what, xx?",
      "You are so mean, xx. :(", "You wanna go, xx? Huh? HUH?",
      "I know you are just joking, xx. :)"
  ]

  doge_ball = [
      "DID YOU JUST SAY BALL!!!", "BALL BALL BALL!",
      "I DEMAND YOU TO GIVE ME THE BALL!", "BALLLLLLLLL!",
      "GIVE! *WOOF* BALL! *WOOF* PLS! *WOOF*", "pls give the ball pls.",
      "B-B-BALL?!?!?!?",
      "Ball? It's been a long time since I've heard that word...",
      "Ball? Last time I heard that word was back in the Pupper Wars. OH DOGELLA, WHY'D YOU LEAVE ME!"
  ]

  doge_wishes = [
      "a pony", "world peace", "a dragon", "happiness", "a waifu", "a life",
      "money", "a cent", "a doge", "minecraft-free-version.exe",
      "a #1 Victory Royale", "some V-Bucks", "some Robux", "some Minecoins",
      "diamonds", "Santa Clause to remove them from the Naughty list"
  ]

  games_start = ["start", "play", "game"]

  games_help = "I see you want to play a game, xx. I offer a variety of games like Tic Tac Toe, Hangman, Connect 4, Dots and Boxes. Just call out to me saying you want to play one of these games, or send 'play [game]' through the chat!"

  with open("words.txt") as file:
    words = [line.strip().lower() for line in file]

  async def on_ready(self):
    print(f'Logged on as {self.user}!')

  async def on_message(self, message):
    if message.author.bot:
      return

    message_content_lower = message.content.lower()
    message_content = message_content_lower.replace(" ", "")
    author_name = message.author.display_name

    if message_content == "ping":
      await message.channel.send("Pong!")

    if doge_call(message_content, [Doge.greetings]):
      await message.channel.send(
          f"{random.choice(Doge.greetings).capitalize()}, {author_name}!")
    elif doge_call(message_content, [["love", "like"]]):
      line = random.choice(Doge.doge_love).replace("xx", author_name)
      await message.channel.send(line)
    elif doge_call(message_content, [["hate", "suck"]]):
      line = random.choice(Doge.doge_insults).replace("xx", author_name)
      await message.channel.send(line)
    elif doge_call(message_content, ["make", "wish"]):
      wish = random.choice(Doge.doge_wishes)
      await message.channel.send(f"{author_name} made a wish! They got {wish}!"
                                 )
    elif doge_call(message_content, ["help"]):
      await message.channel.send(Doge.help.replace("xx", author_name))

    if ("ball" in message_content and random.choice([False] * 4 + [True])
        or doge_call(message_content, ["ball"])):
      line = random.choice(Doge.doge_ball).replace("xx", author_name)
      await message.channel.send(line)

    if doge_call_command(message_content, [Doge.games_start, "tictactoe"]):
      response = await wait_for_join("Tic Tac Toe", message, client)
      await tictactoe.run([message.author, response.author], message.channel,
                          client)

    elif doge_call_command(message_content, [Doge.games_start, "hangman"]):
      await hangmann.run(message, client, Doge.words)

    elif doge_call_command(message_content, [Doge.games_start, "connect4"]):
      response = await wait_for_join("Connect 4", message, client)
      await connectt4.run([message.author, response.author], message.channel,
                          client)

    elif doge_call_command(message_content,
                           [Doge.games_start, ["dotsandboxes", "dotsboxes"]]):
      response = await wait_for_join("Dots and Boxes", message, client)
      await dotsboxes.run([message.author, response.author], message.channel,
                          client)

    if message_content_lower.startswith("rolldice"):
      await message.channel.send(f"Rolled Dice, Total: " + str(
          eval(
              apply_regex(message_content_lower[len('rolldice'):], r'\d+d\d+',
                          lambda x: str(execute_roll(x))))))


intents = discord.Intents.default()
intents.message_content = True

client = Doge(intents=intents)
client.run(os.environ['BOT_KEY'])
