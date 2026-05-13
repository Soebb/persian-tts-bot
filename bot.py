import os, wave
from piper import PiperVoice as piper #Backbone of text to speech
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import preprocess_text, wav2mp3
from omnivoice import OmniVoice
import soundfile as sf
import torch

load_dotenv()

Bot = Client(
    "PersianT2SBot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

# global variable
text = "یک متن جدید به ربات بفرستید"

START_TXT = """
Hi {}, I'm Persian TTS Bot.

Just send me your text.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/soebb'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    txt = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=txt,
        disable_web_page_preview=True,
        reply_markup=reply_markup
)


@Bot.on_message(filters.private & filters.text)
async def t2s(bot, m):
    global text
    input = m.text.replace('\n', ' ').replace('  ', ' ')
    text = preprocess_text(input)
    await m.reply("by /omni or /piper ?")

@Bot.on_message(filters.command(["piper"]))
async def piperr(bot, update):
    msg = await m.reply("Processing..")
    voice = piper.load("fa_model/gyro_model.onnx")
    wav_filename = "output.wav"
    with wave.open(output_1, "wb") as wav_file:
        voice.synthesize_wav(str(text), wav_file)
    mp3_filename = "generated.mp3"
    wav2mp3(wav_filename, mp3_filename)
    await bot.send_audio(chat_id=m.chat.id, audio=mp3_filename)
    await msg.delete()

@Bot.on_message(filters.command(["omni"]))
async def omnii(bot, m):
    msg = await m.reply("Processing..")
    audio = model.generate(text=text, language="fa")
    wav_filename = "output.wav"
    sf.write(wav_filename, audio[0], 24000)
    mp3_filename = "generated.mp3"
    wav2mp3(wav_filename, mp3_filename)
    await bot.send_audio(chat_id=m.chat.id, audio=mp3_filename)
    await msg.delete()

Bot.run()
