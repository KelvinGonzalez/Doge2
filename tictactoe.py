from doge_utils import doge_call_command

player_icons = ["X", "O"]


def display_board(board_list):
  return "```" + "\n-+-+-\n".join([
      "|".join([
          str(i + j + 1) if board_list[i + j] is None else board_list[i + j]
          for j in range(3)
      ]) for i in range(0, 9, 3)
  ]) + "```"


def validate_win(board_list):
  board_list = [x if x is not None else "" for x in board_list]
  for icon in player_icons:
    for i in range(3):
      if board_list[i * 3] + board_list[i * 3 + 1] + board_list[
          i * 3 + 2] == icon * 3 or board_list[i] + board_list[
              i + 3] + board_list[i + 6] == icon * 3:
        return True
    if board_list[0] + board_list[4] + board_list[8] == icon * 3 or board_list[
        2] + board_list[4] + board_list[6] == icon * 3:
      return True
  return False


async def run(players, channel, client):
  if len(players) != 2:
    await channel.send("There must be only 2 players")
    return

  await channel.send(
      f"{players[0].display_name} and {players[1].display_name} are playing Tic Tac Toe. Send 'input #' to perform your move"
  )

  board_list: list[str | None] = [None] * 9
  p = 0
  game_over = False

  while not game_over:
    out_string = f"It is {players[p].display_name}'s turn\n"
    out_string += display_board(board_list)
    await channel.send(out_string)
    while True:
      response = await client.wait_for(
          "message", check=lambda msg: msg.channel == channel)
      response_content = response.content.lower().replace(" ", "")
      if response.author == players[p] and response_content.startswith(
          "input"):
        try:
          slot = int(response_content[len("input"):]) - 1
          if board_list[slot] is not None:
            raise Exception()
          board_list[slot] = player_icons[p]
          if validate_win(board_list):
            out_string = display_board(board_list)
            out_string += f"{players[p].display_name} wins!"
            await channel.send(out_string)
            game_over = True
          p = (p + 1) % len(players)
          break
        except:
          await channel.send("Invalid input, please try again")
      elif response.author in players and doge_call_command(
          response_content, [["stop", "leave", "exit"], "tictactoe"]):
        await channel.send(
            f"{response.author.display_name} has stopped the game")
        game_over = True
        break
