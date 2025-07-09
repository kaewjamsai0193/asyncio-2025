import time
from datetime import timedelta
import asyncio

speed = 100
judit_time = 5/speed
Opponent_time = 55/speed
opponents = 24
move_pairs = 30

async def game(x):
    start = time.perf_counter()
    for i in range(move_pairs):
        time.sleep(judit_time)
        print(f"Board-{x+1} {i+1} Judit made a move with {int(judit_time*speed)} seconds")

        await asyncio.sleep(Opponent_time)
        print(f"Board-{x+1} {i+1} Opponent made a move with {int(Opponent_time*speed)} seconds")

    print(f"BOARD-{x+1} >>>>>>>>> Finished move in {(time.perf_counter() - start)*speed:.1f} seconds\n")
    #print(f"BOARD {x+1} >>>>>>>>> Finished move in {cal_start_time*speed:.1f} seconds(Calculated)\n")

    return {
        'cal_board_time': (time.perf_counter() - start) * speed
    }

async def main():
    task = []
    for i in range(opponents):
        task += [game(i)]
    await asyncio.gather(*task)
    print(f"Board exhisbition finished for {opponents} opponent in {timedelta(seconds=speed*round(time.perf_counter() - start ))} hr.")


if __name__ == '__main__':
    print(f"Number of games: {opponents} games")
    print(f"Number of move: {move_pairs} pairs")
    start = time.perf_counter()
    asyncio.run(main())
    print(f"Finished in {round(time.perf_counter() - start)} seconds")


