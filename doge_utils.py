from discord import Message, Client
import re
import random


def doge_call(line, words):
  if "doge" not in line:
    return False

  for word in words:
    if type(word) is not list:
      if word not in line:
        return False
    else:
      if all(w not in line for w in word):
        return False

  return True


def doge_command(line, words):

  def doge_command_aux(line, words, index, string):
    if index >= len(words):
      return string == line

    if type(words[index]) is not list:
      return doge_command_aux(line, words, index + 1, string + words[index])

    return any(
        doge_command_aux(line, words, index + 1, string + word)
        for word in words[index])

  return doge_command_aux(line, words, 0, "")


def doge_call_command(line, words):
  return doge_command(line, words) if "doge" not in line else doge_call(
      line, words)


async def wait_for_join(game: str, message: Message, client: Client):
  await message.channel.send(
      f"{message.author.display_name} wants to play {game}. Say 'I do' if you want to play!"
  )
  return await client.wait_for(
      "message",
      check=lambda msg: msg.channel == message.channel and msg.author !=
      message.author and msg.content.lower() == "i do")


def execute_roll(dice_roll):
  count, sides = tuple(dice_roll.split("d", 1))
  count, sides = int(count), int(sides)
  return sum([random.randint(1, sides) for _ in range(count)])


def apply_regex(string, regex, funct):
  result = string

  delta = 0
  for match in re.finditer(regex, string):
    i, j = match.span()
    i, j = i + delta, j + delta
    temp = len(result)
    result = result[:i] + funct(result[i:j]) + result[j:]
    delta += len(result) - temp

  return result
