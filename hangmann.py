import random
from doge_utils import doge_call_command


def print_man(misses):
  output_strings = [""] * 3
  if misses >= 1:
    output_strings[0] = " O "
  if misses >= 2:
    output_strings[1] = " | "
  if misses >= 3:
    output_strings[1] = "/| "
  if misses >= 4:
    output_strings[1] = "/|\\"
  if misses >= 5:
    output_strings[2] = "/  "
  if misses >= 6:
    output_strings[2] = "/ \\"
  return output_strings


def print_word(letters, word):
  output_string = ""
  for c in word:
    if c not in letters:
      output_string += "\\_ "
    else:
      output_string += f"{c} "
  return output_string


def print_alphabet(letters):
  output_string = ""
  for i in range(26):
    if i % 9 == 0:
      output_string += "\n"
    c = chr(ord('A') + i)
    output_string += (f"~~{c}~~" if c.lower() in letters else c) + " "
  return output_string


def print_game(letters, word, misses):
  man_strings: list[str] = print_man(misses)
  output_strings = [
      "_____", "|   |", "|  " + man_strings[0], "|  " + man_strings[1],
      "|  " + man_strings[2], "--------"
  ]
  output_string = "```\n" + "\n".join(output_strings) + "\n```" + "\n"
  output_string += "Word: " + print_word(letters, word) + "\n"
  output_string += print_alphabet(letters)
  return output_string


def check_win(letters, word):
  return all(c in letters for c in word)


async def run(message, client, words):
  players = [message.author]
  channel = message.channel
  turn = 0
  stop_game = False
  await channel.send(
      "A game of hangman has begun. Send 'guess x' to guess a letter")

  while not stop_game:
    letters = []
    word = random.choice(words)
    misses = 0
    await channel.send(
        f"New Round: It is {players[turn].display_name}'s turn\n" +
        print_game(letters, word, misses))
    while True:
      print_string = ""

      response = await client.wait_for(
          "message",
          check=lambda msg: msg.channel == channel and not msg.author.bot)
      response_content = response.content.lower().replace(" ", "")
      if response.author == players[turn] and response_content.startswith(
          "guess"):
        letter = response_content[len("guess"):]
        if letter.isalpha() and len(letter) == 1:
          if letter not in letters:
            letters.append(letter)
            if letter not in word:
              print_string += "Missed!\n"
              misses += 1
            print_string += print_game(letters, word, misses) + "\n"
          else:
            print_string += "Letter has already been guessed\n"
        else:
          print_string += "Invalid input, please try again\n"

      if response.author in players and doge_call_command(
          response_content, ["stop", "hangman"]):
        await channel.send(f"{response.author.display_name} stopped the game")
        stop_game = True
        break

      if response.author == players[turn] and doge_call_command(
          response_content, ["skip", "turn"]):
        await channel.send(f"{players[turn].display_name} skipped their turn")
        turn = (turn + 1) % len(players)
        break

      if doge_call_command(
          response_content,
          ["join", "hangman"]) and response.author not in players:
        await channel.send(
            f"{response.author.display_name} joined the Hangman game")
        players.append(response.author)

      if response.author in players and doge_call_command(
          response_content, [["leave", "exit"], "hangman"]):
        await channel.send(
            f"{response.author.display_name} left the Hangman game")
        if len(players) == 1:
          await channel.send(
              "The game has ended since there are no more players")
          stop_game = True
          break
        if response.author == players[turn]:
          players.remove(response.author)
          turn %= len(players)
          break
        players.remove(response.author)

      if check_win(letters, word):
        print_string += f"\n{players[turn].display_name} finished their word!"
        await channel.send(print_string)
        turn = (turn + 1) % len(players)
        break

      if misses >= 6:
        print_string += f"\n{players[turn].display_name} was hung! The word was '{word}'"
        await channel.send(print_string)
        turn = (turn + 1) % len(players)
        break

      if print_string != "":
        await channel.send(print_string)
