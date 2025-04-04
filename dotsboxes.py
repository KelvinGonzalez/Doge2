from doge_utils import doge_call_command

N, S, W, E = "n", "s", "w", "e"

spaces = [" ", "   "]
line = ["|", "———"]
dot = "•"
offsets = {N: (-1, 0), S: (1, 0), W: (0, -1), E: (0, 1)}
size = 5
compass = ["    N", "  W + E", "    S"]
icons = [" X ", " O "]


def tuple_add(t1, t2):
  t1_1, t1_2 = t1
  t2_1, t2_2 = t2
  return (t1_1 + t2_1, t1_2 + t2_2)


def tuple_sub(t1, t2):
  t1_1, t1_2 = t1
  t2_1, t2_2 = t2
  return (t1_1 - t2_1, t1_2 - t2_2)


def find_box(position):
  i, j = 2 * (ord(position[0]) - ord('a')) + 1, 2 * (int(position[1]) - 1) + 1
  if not (0 <= i < 2 * size + 1) or not (0 <= j < 2 * size + 1):
    raise Exception()
  return (i, j)


def find_line(position):
  box = find_box(position)
  offset = offsets[position[2]]
  i, j = tuple_add(box, offset)
  if not (0 <= i < 2 * size + 1) or not (0 <= j < 2 * size + 1):
    raise Exception()
  return (i, j)


def find_mirror_box(position):
  box = find_box(position)
  line = find_line(position)
  i, j = tuple_add(line, tuple_sub(line, box))
  if not (0 <= i < 2 * size + 1) or not (0 <= j < 2 * size + 1):
    return None
  return (i, j)


def check_box(board, box):
  for offset in offsets.values():
    line_i, line_j = tuple_add(box, offset)
    if board[line_i][line_j] is None:
      return False
  return True


def display_board(board):
  return "```\n" + "\n".join([
      (chr(ord('A') + (i - 1) // 2) if i % 2 == 1 else " ") + "  " + "".join(
          [x if x is not None else spaces[j % 2] for j, x in enumerate(row)]) +
      (compass[i] if i < len(compass) else "") for i, row in enumerate(board)
  ]) + "\n     " + "   ".join([str(x) for x in range(1, size + 1)]) + "\n```"


def create_board():
  n = 2 * size + 1
  board: list[list[str | None]] = [[None] * n for _ in range(n)]
  for i in range(0, n, 2):
    for j in range(0, n, 2):
      board[i][j] = dot
  return board


def check_line(board, position, p):
  line_i, line_j = find_line(position)
  if board[line_i][line_j] is not None:
    return (False, False)
  board[line_i][line_j] = line[line_j % 2]

  box, mirror_box = find_box(position), find_mirror_box(position)
  scored = False
  if check_box(board, box):
    box_i, box_j = box
    board[box_i][box_j] = icons[p]
    scored = True
  if mirror_box is not None and check_box(board, mirror_box):
    box_i, box_j = mirror_box
    board[box_i][box_j] = icons[p]
    scored = True
  return (True, scored)


def check_game_end(board):
  scores = {icons[0]: 0, icons[1]: 0}
  total = 0
  for i in range(1, 2 * size, 2):
    for j in range(1, 2 * size, 2):
      if board[i][j] is not None:
        scores[board[i][j]] += 1
        total += 1
  if total != size * size:
    return None
  return 0 if scores[icons[0]] >= scores[icons[1]] else 1


async def run(players, channel, client):
  if len(players) != 2:
    await channel.send("There must be only 2 players")
    return

  await channel.send(
      f"{players[0].display_name} and {players[1].display_name} are playing Dots and Boxes. Send 'input L#D' to perform your move ('A1N' will place at the north of box in A1)"
  )

  board = create_board()
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
          position = response_content[len("input"):]
          placed, scored = check_line(board, position, p)
          if not placed:
            await channel.send("A line already was placed here")
            continue

          winner = check_game_end(board)
          if winner is not None:
            out_string = display_board(board)
            out_string += f"{players[winner].display_name} wins!"
            await channel.send(out_string)
            game_over = True

          if not scored:
            p = (p + 1) % len(players)

          break

        except:
          await channel.send("Invalid input, please try again")

      elif response.author in players and doge_call_command(
          response_content,
          [["stop", "leave", "exit"], ["dotsandboxes", "dotsboxes"]]):
        await channel.send(
            f"{response.author.display_name} has stopped the game")
        game_over = True
        break
