import asyncio
import time

customer = {
    "Alice": ["Apple", "Banana", "Milk"],
    "Bob": ["Bread", "cheese"],
    "Charlie": ["Eggs", "Juice", "Butter"],
    "A": ["Apple", "Milk"],
    "B": ["Bread", "cheese"],
    "C": ["Juice", "Butter"],
    "D": ["Apple", "Milk"],
    "E": ["Bread", "cheese"],
    "F": ["Juice", "Butter"],
    "G": ["Butter", "Juice"],
}

cashiers = {f"Cashier-{i}": i for i in range(1, 3)}

async def customers(queue):
    for name, items in customer.items():
        print(f"[{time.ctime()}] [{name}] finished shopping: {items}")
        await queue.put((name, items))

async def cashier(name, queue, per_item):
    total = 0
    while True:
        task = await queue.get()
        if task is None:

            print(f"[{time.ctime()}] [{name}] closed have {total} customers")
            queue.task_done()
            break

        cust_name, items = task
        print(f"[{time.ctime()}] [{name}] processing {cust_name} with order {items}")
        await asyncio.sleep(len(items) * per_item)
        print(f"[{time.ctime()}] [{name}] finished {cust_name}")
        total += 1
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=5)
    # สร้าง Cashier
    cashier_tasks = [
        asyncio.create_task(cashier(name, queue, per_item))
        for name, per_item in cashiers.items()
    ]
    # สร้าง Customer
    customer_task = asyncio.create_task(customers(queue))
    await customer_task
    # รอให้ queue ว่าง
    await queue.join()

    # ส่งสัญญาณปิด Cashier
    for _ in cashier_tasks:
        await queue.put(None)

    # รอ Cashier ปิด
    await asyncio.gather(*cashier_tasks)

    print(f"[{time.ctime()}] Supermarket is closed!")

asyncio.run(main())
