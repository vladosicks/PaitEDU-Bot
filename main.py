import asyncio

from app.database.database import Base, engine
from app.database import models

Base.metadata.create_all(bind=engine)

from aiogram import Bot, Dispatcher
from app.config.settings import BOT_TOKEN
from app.handlers.start import router as start_router
from app.handlers.services import router as services_router
from app.handlers.essay import router as essay_router
from app.handlers.essay_price import router as essay_price_router
from app.handlers.coursework import router as coursework_router
from app.handlers.coursework_price import router as coursework_price_router
from app.handlers.diploma import router as diploma_router
from app.handlers.diploma_price import router as diploma_price_router
from app.handlers.presentation_price import router as presentation_price_router
from app.handlers.presentation import router as presentation_router
from app.handlers.translation import router as translation_router
from app.handlers.translation_price import router as translation_price_router
from app.handlers.other import router as other_router
from app.handlers.order import router as order_router
from app.handlers.admin import router as admin_router
from app.handlers.admin_chat import router as admin_chat_router
from app.handlers.client_chat import router as client_chat_router


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(services_router)
dp.include_router(essay_router)
dp.include_router(essay_price_router)
dp.include_router(coursework_router)
dp.include_router(coursework_price_router)
dp.include_router(diploma_router)
dp.include_router(diploma_price_router)
dp.include_router(presentation_price_router)
dp.include_router(presentation_router)
dp.include_router(translation_router)
dp.include_router(translation_price_router)
dp.include_router(other_router)
dp.include_router(order_router)
dp.include_router(admin_router)
dp.include_router(admin_chat_router)
dp.include_router(client_chat_router)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())