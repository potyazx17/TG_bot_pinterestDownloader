from aiogram import Router, F

from projects.pin8.src.tg_bot.load_media.pinterest.pintrest_dowloading import download_pinterest_media
from aiogram.types import Message, FSInputFile, CallbackQuery, InputFile
from aiogram.filters import Command
from aiogram.enums import ChatAction
import os
from kb.inline import keyboard_inline
import moviepy as mp

comands_router = Router()

@comands_router.message(Command('start'))
async def start(message: Message):
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    hello_user = f"Hello {message.chat.first_name}\n please give me url of pinterest"
    await message.answer_photo(FSInputFile('pinintro.png'), caption=hello_user)


@comands_router.message(F.text)
async def download(message: Message):
    if 'pin.it' in message.text:
        await message.answer(text='load please wait')
        filename = download_pinterest_media(message.text)
        if os.listdir('downloads')[0].endswith('.mp4'):
          await message.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)
          video = FSInputFile(filename)
          await message.answer_video(video, caption='video downloaded', reply_markup=keyboard_inline)



        elif os.listdir('downloads')[0].endswith('.jpg'):
            await message.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
            await message.reply_photo(FSInputFile(path=filename), caption='photo downloaded')
            os.remove(filename)


    else:
        await message.answer(text='incorect url')



@comands_router.callback_query(F.data == "audio")
async def download(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('wait when downloading audio')
    video_file = mp.VideoFileClip('downloads/pinterest_video.mp4')
    video_file.audio.write_audiofile('downloads/z_pinterest_audio.mp3')
    await callback.message.bot.send_chat_action(callback.message.chat.id, ChatAction.UPLOAD_VOICE)
    await callback.message.answer_audio(FSInputFile('downloads/z_pinterest_audio.mp3'), caption='audio downloaded')



