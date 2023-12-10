import telebot
from telebot import types
import cross_zeros as cs
import cows_bulls as cb
import os


API_token = '6872564247:AAEj8KfaRdD0izD6w3-MYASgwlvmG33vMP8' if 'AMVERA' in os.environ else '6856931870:AAF7-5nOZXru_0Ebm5ae4yDjmOwfVvF3iI4'
bot = telebot.TeleBot(API_token)


cs_dic = {1: [0, 0],
          2: [0, 1],
          3: [0, 2],
          4: [1, 0],
          5: [1, 1],
          6: [1, 2],
          7: [2, 0],
          8: [2, 1],
          9: [2, 2]}
path = '/data' if 'AMVERA' in os.environ else 'D:/Desktop/Программы Питон/Games/data'


def move_cs(chat_id, l):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(1, 10, 3):
        btn1 = types.InlineKeyboardButton(text=f'{i}', callback_data=f'c&n{i}{l}')
        btn2 = types.InlineKeyboardButton(text=f'{i+1}', callback_data=f'c&n{i+1}{l}')
        btn3 = types.InlineKeyboardButton(text=f'{i+2}', callback_data=f'c&n{i+2}{l}')
        keyboard.add(btn1, btn2, btn3, row_width=3)

    bot.send_message(chat_id=chat_id, text='Выберите позицию для хода (1-9):', reply_markup=keyboard)


def erase(user_id): os.remove(path + f'/output/output_{user_id}.png')


def send_instr(user_id):
   keyboard = types.ReplyKeyboardMarkup()
   btn1 = types.KeyboardButton('/инструкция КН')
   btn2 = types.KeyboardButton('/инструкция БК')
   keyboard.add(btn1, btn2)
   bot.send_message(chat_id = user_id, text = 'Выберите инструкция к какой игре вам нужна.\n Краткие обозначения:\n КН - крестики нолики\n БК - быки и коровы', reply_markup = keyboard)


#главное меню
@bot.message_handler(commands = ['help', 'start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup(row_width = 1)
    btn1 = types.InlineKeyboardButton(text = 'Крестики нолики', callback_data = '/Крестики нолики')
    btn2 = types.InlineKeyboardButton(text = 'Быки и коровы', callback_data = '/Быки и коровы')
    btn3 = types.InlineKeyboardButton(text = '/инструкция', callback_data = '/инструкция')
    btn4 = types.InlineKeyboardButton(text = 'о приложении', callback_data = '/information')
    keyboard.add(btn1, btn2, btn3, btn4)
    bot.send_message(chat_id=message.chat.id, text='Привет! Хочешь поиграть в пару игр со мной?)', reply_markup = keyboard)


#крестики нолики
@bot.callback_query_handler(func = lambda c: c.data == '/Крестики нолики' or 'c&n' in c.data)
def callback_cs(c):
    bot.answer_callback_query(c.id, text='')
    if c.data == '/Крестики нолики':
        chat_id = c.message.chat.id
        bot.send_message(chat_id = chat_id, text=f'Давай сыграем в крестики нолики! (есди тебе нужна инструкция, напиши в чат\n /инструкция КН)')
        move_cs(chat_id, 0)
    if 'c&n' in c.data and c.data[4] == '0':
        chat_id = c.message.chat.id
        pos = cs_dic.get(int(c.data[3]))
        global df
        df = cs.create_field()
        df, err = cs.user_move(df, pos, chat_id)
        bot.send_document(chat_id = chat_id, caption = 'Ваш ход', document = open(path + f'/output/output_{chat_id}.png', 'rb'))
        df = cs.AI_move(df, chat_id)
        bot.send_document(chat_id = chat_id, caption = 'Ход бота', document = open(path + f'/output/output_{chat_id}.png', 'rb'))
        bot.send_message(chat_id = chat_id, text = 'Ваш ход!')
        move_cs(chat_id, 1)
    elif 'c&n' in c.data and c.data[4] != '0':
        chat_id = c.message.chat.id
        pos = cs_dic.get(int(c.data[3]))
        df, err = cs.user_move(df, pos, chat_id)
        if err == 0:
            bot.send_document(chat_id = chat_id, caption = 'Ваш ход', document = open(path + f'/output/output_{chat_id}.png', 'rb'))
            win = cs.check_win(df)
            if win != 1:
                bot.send_message(chat_id=chat_id, text=win)
                erase(chat_id)
                send_welcome(c.message)
            else:
                df = cs.AI_move(df, chat_id)
                bot.send_document(chat_id=chat_id, caption='Ход бота', document=open(path + f'/output/output_{chat_id}.png', 'rb'))
                win = cs.check_win(df)
                if win == 1:
                    bot.send_message(chat_id=chat_id, text='Ваш ход!')
                    move_cs(chat_id, 1)
                else:
                    bot.send_message(chat_id=chat_id, text = win)
                    erase(chat_id)
                    send_welcome(c.message)
        else:
            bot.send_message(chat_id=chat_id, text = err)
            bot.send_message(chat_id=chat_id, text = 'Попытайтесь снова')
            move_cs(chat_id, 1)

#быки и коровы
@bot.callback_query_handler(func = lambda c: c.data == '/Быки и коровы')
def callback_cb(c):
    bot.answer_callback_query(c.id, text='')
    chat_id = c.message.chat.id
    bot.send_message(chat_id, text = 'Давай сыграем в быков и коров! (если тебе нужна инструкция напиши в чат\n /инструкция БК)')
    global gen
    gen = cb.generate()
    bot.send_message(chat_id, text = 'Я загадал число, попробуйте его угадать')


#инструкции и информация
@bot.callback_query_handler(func = lambda c: c.data == '/инструкция' or c.data == '/information')
def s_i(c):
    bot.answer_callback_query(c.id, text='')
    if c.data == '/инструкция':
        send_instr(c.message.chat.id)
    if c.data == '/information':
        bot.send_message(c.message.chat.id, text = 'version alpha 1.0\n Разработчик:\n Рябчицкий Матвей Максимович')


@bot.message_handler(commands = ['инструкция', 'инструкция КН', 'инструкция БК'])
def send_ins(mess):
    chat_id = mess.chat.id
    if mess.text == '/инструкция КН':
        bot.send_message(chat_id, text = 'Принцип игры - составить три символа в ряд (по вертикали, горизонтали или по диагонали).\n Вы играете символом \'X\' и ходите первым.\n Против вас играю я, хожу - \'0\'\n Чтобы поставить символ вам нужно нажать кнопку (их вы увидите в процессе игры) с номером клетки в которую вы ходите поставить символ.')
        bot.send_document(chat_id, caption = 'Нумерация клеточек', document = open(path + '/Разметка КН.png', 'rb'))
        send_welcome(mess)
    if mess.text == '/инструкция': send_instr(chat_id)
    if mess.text == '/инструкция БК':
        bot.send_message(chat_id, text = 'Это простая логическая игра, цель которой - угадать четырёхзначное число. Цифры в числе не могут повторяться и число может начинаться с нуля (например: 0123).\n Я загадываю число, а вы должны попытаться его угадать. Вы пишите в чат четырёхзначное число, после чего я говорю вам количество коров и быков.\n Каждая корова - верно угаданная цифра, но не на своём месте. Каждый бык - верно угаданная цифра на своём месте.\n Таким образом вы побеждаете когда набираете 4 быков\n')
        bot.send_message(chat_id, text = 'Пример игры:')
        bot.send_message(chat_id, text = 'Я загадываю число 4231')
        bot.send_message(chat_id, text = 'Вы пишите мне: 1234')
        bot.send_message(chat_id, text = 'Я отвечаю вам: 2 коровы и 2 быка')
        send_welcome(mess)


@bot.message_handler(func = lambda message: message.text.isdigit())
def play_cb(message):
    chat_id = message.chat.id
    try:
        num = message.text
        if len(num) == 4:
            b,c = cb.check(gen, num)
            if b != 0:
                if b == 1: bot.send_message(chat_id, text = 'У вас 1 бык')
                else: bot.send_message(chat_id, text = f'У вас {b} быка')
            if c != 0:
                if c == 1: bot.send_message(chat_id, text = 'У вас 1 корова')
                else: bot.send_message(chat_id, text = f'У вас {c} коровы')
            if c == 0 and b == 0: bot.send_message(chat_id, text = 'У вас ни одного быка и ни одной коровы( Попытайтесь ещё!')
            if b == 4: bot.send_message(chat_id, text = f'Поздравляю! Вы угадали число {gen}!')
            elif b !=4: bot.send_message(chat_id, text = 'Почти, попытайтесь ещё!')
        else: bot.send_message(chat_id, text = 'Слово четырёхзначное состоит из двух корней, один из которых четыре. ЧЕТЫРЕ. Давайте я никому не скажу, а вы попробуете ещё раз?')
    except:
        bot.send_message(chat_id, text = 'Отлично! А теперь три цифры с обратной стороны карты')
        bot.send_message(chat_id, text = f'||Вы явно делаете что\-то не то\.\.\.||', parse_mode = 'MarkdownV2')





p = 0
while p ==0:
    print('Processing')
    p =1
bot.infinity_polling()