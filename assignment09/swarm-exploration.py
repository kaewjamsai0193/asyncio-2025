import asyncio
import random
import matplotlib.pyplot as plt

N_AGENTS = 10
N_STEPS = 200

TARGET = (random.randint(-20,20),random.randint(-20,20))

traces = {i: [(0, 0)] for i in range(N_AGENTS)}
found_by = {}
target_found = False

async def explore(agent_id: int):
    global target_found
    x, y  = traces[agent_id][0]
    for step in range(1,N_STEPS+1):
        if target_found:
            break
        dx,dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        x, y = x + dx, y + dy
        traces[agent_id].append((x, y))

        if (x, y) == TARGET:
            found_by[agent_id] = step
            target_found = True
            print(f'Agent {agent_id} found the target at step {step}')
            break

        await asyncio.sleep(0.01)

async def main():
    print(f'Random target location: {TARGET}')
    tasks = [asyncio.create_task(explore(i)) for i in range(N_AGENTS)]
    await asyncio.gather(*tasks)

    for agent_id, path in traces.items():
        xs, ys = zip(*path)
        plt.plot(xs, ys, marker=".", alpha=0.6, label=f'Agent {agent_id}')
    plt.scatter(*TARGET, color='red', s=100, marker="X", label='Target')

    plt.title('Swarm Exploration (Stop ALL on Target Found)')
    plt.legend()
    plt.grid(True)
    plt.show()

    if found_by:
        print(f'Target found by:')
        for agent, step in found_by.items():
            print(f'Agent {agent} at step {step}')
        else:
            print('No agent found the target.')
if __name__ == "__main__":
    asyncio.run(main())