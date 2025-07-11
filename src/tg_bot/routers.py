from aiogram import Router
from comands import comands_router

router = Router()
router.include_router(comands_router)