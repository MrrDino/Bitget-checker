import asyncio

from loguru import logger
from multiprocessing import Process

from api.bitget import get_info
from telegram.bot import start_bot, send_message


async def listener():
    """Функция бесконечного прослушивания информации"""

    while True:
        try:
            deposit = await get_info()

            if deposit:
                await send_message()
                await asyncio.sleep(60)  # ожидание, когда Deposit= True
            else:
                await asyncio.sleep(7) # каждые 10 секунд приходит результат
        except Exception as err:
            logger.error(err)


def start_listen():
    """Функиця запуска бесконечного прослушивания"""

    asyncio.run(listener())


def start():
    """Функция запуска скрипта"""

    p1 = Process(target=start_bot, args=())
    p2 = Process(target=start_listen, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()


if __name__ == '__main__':
    start()
