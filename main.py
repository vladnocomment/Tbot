from telebot import TeleBot, types
from random import randint
import config
bot = TeleBot(config.TOKEN)

pictures = {
    0: "https://funart.pro/uploads/posts/2021-04/1618615259_13-funart_pro-p-oboi-fon-temnii-les-anime-13.jpg",
    1: "https://w0.peakpx.com/wallpaper/215/27/HD-wallpaper-dark-spooky-house-on-the-water-gray-halloween-houses-eerie-sky-clouds-water-spooky-dark.jpg",
    2: "https://st2.depositphotos.com/1909225/5528/i/600/depositphotos_55288803-stock-photo-small-cemetery.jpg",
    3: "https://stihi.ru/pics/2016/12/10/6101.jpg",
    4: "https://avatars.mds.yandex.net/get-zen_doc/1911932/pub_5d879fdf35ca3100ac341b1d_5d87a297b5e99200ae5f8d01/scale_1200"
}
states = {}#Состояние
inventories = {}#Инвентарь нашего героя
@bot.message_handler(commands=["start"])    
def start_game(message):
    """"Функция отвечает за определение чата в котором происходит общение и приветствие с пользователем"""
    user = message.chat.id#Определение чата в котором идет общение
    states[user] = 0#Состояние героя пользователя
    inventories[user] = []#Инвентарь героя пользователя

    bot.send_message(user, "Добро пожаловать в игру!")#Приветствующее сообщение

    process_state(user, states[user], inventories[user])

@bot.callback_query_handler(func=lambda call: True)
def user_answer(call):#Переводчик из одной ф-ии в другую
    """"Функция отвечает за перевод параметров в другую функцию"""
    user = call.message.chat.id
    process_answer(user, call.data)

def process_state(user, state, inventory):
    """"Функция отвечает за назначения кнопок,а также дальнейшее продвижение по сюжету игры """
    kb = types.InlineKeyboardMarkup()#Кнопки к которым мы в дальнейшем присвоим значение ответа

    bot.send_photo(user, pictures[state])

    if state == 0:
        kb.add(types.InlineKeyboardButton(text="пойти направо", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="пойти налево", callback_data="2"))

        bot.send_message(user, "Вы очутились среди темного леса , перед вами две развилки .", reply_markup=kb)

    if state == 1:
        kb.add(types.InlineKeyboardButton(text="зайти в него ", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="вернуться", callback_data="2"))

        bot.send_message(user, "Вы наткнулись на старый заброшенный дом, но почему-то в одном окошке видно мерцание огонька", reply_markup=kb)

    if state == 3:
        kb.add(types.InlineKeyboardButton(text="подняться наверх ", callback_data="4"))
        kb.add(types.InlineKeyboardButton(text="вернуться", callback_data="3"))

        bot.send_message(user,
                         "Зайдя в дом вы увидели перед собой лестницу ведущую на второй этаж дома",
                         reply_markup=kb)
    if state == 4:
        kb.add(types.InlineKeyboardButton(text="забрать его ", callback_data="5"))
        kb.add(types.InlineKeyboardButton(text="вернуться", callback_data="3"))

        bot.send_message(user,
                         "Вы увидели на столе золотой ключ",
                         reply_markup=kb)

    if state == 2:
        bot.send_message(user, "Вы выиграли.")

def process_answer(user, answer):
    """"Функция принимает значение которые выбрал игрок, и продвигает его дальше относительно его состояния"""
    if states[user] == 0:
        if answer == "1":
            states[user] = 1
        else:
            if "key" in inventories[user]:
                bot.send_message(user,
                                 "Перед вами закрытая калитка. Вы пробуете открыть ее ключем, и дверь поддается. Кажется, это выход.")
                states[user] = 2
            else:
                bot.send_message(user, "Перед вами закрытая калитка, и, кажется, без ключа ее не открыть. Придется вернуться обратно.")
                states[user] = 0

    elif states[user] == 1:
        if answer == "2":
            bot.send_message(user,
                             "Вы не решились идти в неизвестный дом, и вернулись обратно")
            states[user] = 0
        else:
            bot.send_message(user,
                             "Вы заходите в дом")
            states[user] = 3
    elif states[user] == 3:
        if answer == "3":
            bot.send_message(user,
                             "Вы решили не подниматься на второй этаж, и просто вышли наружу")
            states[user] = 1
        else:
            bot.send_message(user,
                             "На втором этаже стоял письменный стол,а на нем лежал ключ")
            states[user] = 4

    elif states[user] == 4:
        if answer == "3":
            bot.send_message(user,
                             "Вы решили не брать ключ, и вышли к дверному проему")
            states[user] = 3
        else:
            bot.send_message(user,
                             "вы взяли ключ, и вас отправило в начало леса")
            inventories[user].append("key")
            states[user] = 0



    process_state(user, states[user], inventories[user])

bot.polling(none_stop=True)