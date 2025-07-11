
import asyncio
import loguru
from aiogram import Bot, Dispatcher
from routers import router


TOKEN = '7724580209:AAGezlmoKVKAVra_aEgTfnZGNbhvKhCcYGM'

bot = Bot(token=TOKEN)
dp = Dispatcher()



async def main():
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        loguru.logger.info('started bot')
        asyncio.run(main())
    except KeyboardInterrupt:
        loguru.logger.info('stopping bot')