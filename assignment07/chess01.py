import time
from datetime import timedelta
import asyncio

speed = 1000
judit_time = 5/speed
Opponent_time = 55/speed
opponents = 24
move_pairs = 30

def game(x):
    start = time.perf_counter()
    cal_start_time = 0
    for i in range(move_pairs):
        time.sleep(judit_time)
        cal_start_time += judit_time
        print(f"Board{x+1} {i+1} Judit made a move with {int(judit_time*speed)} seconds")

        time.sleep(Opponent_time)
        print(f"Board{x+1} {i+1} Opponent made a move with {int(Opponent_time*speed)} seconds")
        cal_start_time += Opponent_time

    print(f"BOARD {x+1} >>>>>>>>> Finished move in {(time.perf_counter() - start)*speed:.1f} seconds")
    print(f"BOARD {x+1} >>>>>>>>> Finished move in {cal_start_time*speed:.1f} seconds(Calculated)")

    return {
        'board_time': (time.perf_counter() - start) * speed,
        'cal_start_time': cal_start_time * speed,
    }

if __name__ == '__main__':
    print(f"Number of games: {opponents} games")
    print(f"Number of move: {move_pairs} pairs")
    start = time.perf_counter()
    board_time = 0
    cal_board_time = 0

    for i in range(opponents):
        result = game(i)
        board_time += result['board_time']
        cal_board_time += result['cal_start_time']

    print(f"Board exhisbition finished for {opponents} opponent in {timedelta(seconds=round(board_time))} hr.")
    print(f"Board exhisbition finished for {opponents} opponent in {timedelta(seconds=round(cal_board_time))} hr. (calculated)")
    print(f"Finished in {round(time.perf_counter() - start)} seconds")