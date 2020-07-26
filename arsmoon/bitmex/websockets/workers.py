import asyncio


class BitmexWorker:

    def __init__(self, *args, **kwargs):
        self.loop = asyncio.get_event_loop()

    async def task(self):
        while True:
            await asyncio.sleep(1)
            print("Task Executed")

    def shutdown(self):
        self.loop.stop()
        self.loop.close()

    def run(self):
        print('Start worker...')
        self.loop.run_until_complete(self.task())
        self.loop.run_forever()
