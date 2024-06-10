import telebot

from config import CONFIG


bot = telebot.TeleBot(CONFIG["telegram_token"])
