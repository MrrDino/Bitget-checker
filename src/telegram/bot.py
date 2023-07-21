import os

from loguru import logger
from aiogram import Bot, Dispatcher, executor, types

from api.bitget import get_info


TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
print(TOKEN, CHAT_ID)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(lambda msg: msg.text == '/check')
async def self_check(message: types.Message):
    """Функция проверки по просьбе пользователя"""

    deposit = await get_info()
    await send_message(is_open=deposit, message=message)


async def send_message(is_open: bool = True, message: types.Message = False):
    """Функция отправки сигнала в чат"""

    attempts = 0
    done = False

    if is_open:
        msg = 'Deposit open 🟢'
    else:
        msg = 'Deposit closed 🔴'

    while not done:
        attempts += 1

        if attempts == 5:
            done = True
            continue

        try:
            if message:
                await message.answer(text=msg)
            else:
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=msg,
                    # parse_mode=types.ParseMode.HTML, <- для стилей
                    # disable_web_page_preview=True   <- для ссылок
                )

            done = True
        except Exception as err:
            logger.error(err)
            continue


def start_bot():
    """Функция старта бота"""

    executor.start_polling(dp, skip_updates=False)
