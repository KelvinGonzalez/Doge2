from doge_utils import doge_call_command

player_icons = ["X", "O"]


def display_board(board):
  return "```" + "\n".join([
      "|" + "|".join([col if col is not None else " " for col in row]) + "|"
      for row in board
  ]) + "\n|1|2|3|4|5|6|7|" + "```"


def perform_move(board, slot, icon):
  for i in range(5, -1, -1):
    if board[i][slot] is None:
      board[i][slot] = icon
      return
  raise Exception()


def count_direction(board, position, direction, icon):
  pos_i, pos_j = position
  dir_i, dir_j = direction

  if not (0 <= pos_i < len(board)) or not (0 <= pos_j < len(
      board[0])) or board[pos_i][pos_j] != icon:
    return 0
  return 1 + count_direction(board,
                             (pos_i + dir_i, pos_j + dir_j), direction, icon)


def validate_win(board, slot):
  directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
  for i in range(6):
    if board[i][slot] is not None:
      counts = [
          1 + count_direction(board, (i + dir_i, slot + dir_j),
                              (dir_i, dir_j), board[i][slot]) +
          count_direction(board, (i - dir_i, slot - dir_j),
                          (-dir_i, -dir_j), board[i][slot])
          for dir_i, dir_j in directions
      ]
      return any(count >= 4 for count in counts)
  return False


async def run(players, channel, client):
  if len(players) != 2:
    await channel.send("There must be only 2 players")
    return

  await channel.send(
      f"{players[0].display_name} and {players[1].display_name} are playing Connect 4. Send 'input #' to perform your move"
  )

  board: list[list[str | None]] = [[None for _ in range(7)] for _ in range(6)]
  p = 0
  game_over = False

  while not game_over:
    out_string = f"It is {players[p].display_name}'s turn\n"
    out_string += display_board(board)
    await channel.send(out_string)
    while True:
      response = await client.wait_for(
          "message", check=lambda msg: msg.channel == channel)
      response_content = response.content.lower().replace(" ", "")
      if response.author == players[p] and response_content.startswith(
          "input"):
        try:
          slot = int(response_content[len("input"):]) - 1
          perform_move(board, slot, player_icons[p])
          if validate_win(board, slot):
            out_string = display_board(board)
            out_string += f"{players[p].display_name} wins!"
            await channel.send(out_string)
            game_over = True
          p = (p + 1) % len(players)
          break
        except:
          await channel.send("Invalid input, please try again")
      elif response.author in players and doge_call_command(
          response_content, [["stop", "leave", "exit"], "connect4"]):
        await channel.send(
            f"{response.author.display_name} has stopped the game")
        game_over = True
        break
