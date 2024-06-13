import telebot
from engine import query_engine
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from langsmith import traceable

API_TOKEN = 'telegram_api_key'

bot = telebot.TeleBot(API_TOKEN)
user_engines = {}

# Handle '/start'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_engines[message.chat.id] = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        verbose=True,
    )
    bot.reply_to(message, """\
Hi there, can i help you?\nJust type a message\
""")


@bot.message_handler(commands=['clear'])
def clear(message):
    if message.chat.id not in user_engines.keys():
        user_engines[message.chat.id].reset()
    bot.reply_to(message, """ Chat history was successfully deleted """)


@traceable
def get_response(chat_id, text):
    return user_engines[chat_id].chat(text)


@bot.message_handler(func=lambda message: True)
def answer_message(message):
    if message.chat.id not in user_engines.keys():
        user_engines[message.chat.id] = CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            verbose=True,
        )
    response = get_response(message.chat.id, message.text)
    print(response)
    bot.reply_to(message, response)


bot.infinity_polling()
