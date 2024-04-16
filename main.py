import asyncio
from datetime import datetime
from time import monotonic

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TestResponse(BaseModel):
    elapsed: float


async def work():
    await asyncio.sleep(3)
    print('done')


@app.get('/test', response_model=TestResponse)
async def handler():

    ts1 = monotonic()
    current_tasks = asyncio.all_tasks()
    working_tasks = []
    for task in current_tasks:
        if task.get_name().startswith('work'):
            working_tasks.append(task)
    if working_tasks:
        await asyncio.wait(working_tasks)
    await asyncio.create_task(work(), name=f'work_{datetime.now()}')
    ts2 = monotonic()
    return TestResponse(elapsed=ts2 - ts1)
