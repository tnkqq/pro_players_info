import telebot
import sqlite3
import string
from telebot import types
from data_based import player_info,get_team_list



token = "5944466869:AAGIeaFwFrns78oBwO6vQrJwWohyiPsVq2U"
bot =telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    continue_button = types.InlineKeyboardButton(text = " Продолжить ",callback_data="continue")
    markup.add(continue_button)
    bot.send_message(message.chat.id,"Привет! Этот бот позволяет найти информацию про игроков с сайта prosettings.net",reply_markup=markup)
    bot.register_next_step_handler(message,button_message)

@bot.message_handler(content_types="Text")
def button_message(message):
    player_list = get_team_list(message.text)
    markup = types.InlineKeyboardMarkup()
    if len(player_list) > 0:   
        for player in player_list:
            player_bttn = types.InlineKeyboardButton(text = f"{player}", callback_data= f"{player}")
            markup.add(player_bttn)
        
        bot.send_message(message.from_user.id ,text="Выбери игрока :",reply_markup=markup)
        bot.register_next_step_handler(message,button_message)
    else:
        continue_button = types.InlineKeyboardButton(text = " Продолжить ",callback_data="continue")
        markup.add(continue_button)
        bot.send_message(message.from_user.id ,text="Коанда не найдена 😰",reply_markup=markup)
        bot.register_next_step_handler(message,button_message)
    

@bot.callback_query_handler(func=lambda call:True)
def handle_callback(call):
    if call.data == "continue":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Введи название команды:")   
    else:
        bot.answer_callback_query(call.id)
        text = player_info_list(call.data)
        markup = types.InlineKeyboardMarkup()
        continue_button = types.InlineKeyboardButton(text = " Продолжить ",callback_data="continue")
        markup.add(continue_button)
        bot.send_message(call.message.chat.id, text = text,reply_markup=markup)


"""return player info like KEY : VALUE"""
def player_info_list(player):
    line = "-"*30
    text = f"ℹ️ {player.upper()} BIO ℹ️ :\n {line} \n"
    for key,value in player_info(f"{player}")[0].items():
        if value != None and key != "id":
            text += f"{key} : {value} \n"
    text += f"\n🖱 {player.upper()} GEAR ⌨️: \n {line} \n"
    for key,value in player_info(f"{player}")[1].items():
        if value != None and key != "player_id":
            text += f"{key} : {value} \n"
    text += f"\n 🖥 {player.upper()} SPECS 🖥: \n {line} \n"
    for key,value in player_info(f"{player}")[2].items():
        if value != None and key != "player_id":
            text += f"{key} : {value} \n"
    return text

bot.infinity_polling(none_stop = True)