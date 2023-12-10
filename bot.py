import telebot
from telebot import types
import cross_zeros as cs


API_token = '6872564247:AAEj8KfaRdD0izD6w3-MYASgwlvmG33vMP8'
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
#path_output = 'D:\Desktop\Программы Питон\Games\output'
#path_data = 'D:\Desktop\Программы Питон\Games\data'
def move_cs(chat_id, l):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(1, 10, 3):
        btn1 = types.InlineKeyboardButton(text=f'{i}', callback_data=f'c&n{i}{l}')
        btn2 = types.InlineKeyboardButton(text=f'{i+1}', callback_data=f'c&n{i+1}{l}')
        btn3 = types.InlineKeyboardButton(text=f'{i+2}', callback_data=f'c&n{i+2}{l}')
        keyboard.add(btn1, btn2, btn3, row_width=3)

    bot.send_message(chat_id=chat_id, text='Выберите позицию для хода (1-9):', reply_markup=keyboard)


def send_instr(user_id):
   keyboard = types.ReplyKeyboardMarkup()
   btn1 = types.KeyboardButton('/инструкция КН')
   keyboard.add(btn1)
   bot.send_message(chat_id = user_id, text = 'Выберите инструкция к какой игре вам нужна.\n Краткие обозначения:\n КН - крестики нолики', reply_markup = keyboard)


@bot.message_handler(commands = ['help', 'start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup(row_width = 1)
    btn1 = types.InlineKeyboardButton(text = 'Крестики нолики', callback_data = '/Крестики нолики')
    btn2 = types.InlineKeyboardButton(text = 'Быки и коровы (не активно)', callback_data = 'Nan')
    btn3 = types.InlineKeyboardButton(text = '/инструкция', callback_data = '/инструкция')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(chat_id=message.chat.id, text='Привет! Хочешь поиграть в пару игр со мной?)', reply_markup = keyboard)

#крестики нолики

@bot.callback_query_handler(func = lambda c: c.data == '/Крестики нолики' or 'c&n' in c.data)
def callback(c):
    bot.answer_callback_query(c.id, text='')
    if c.data == '/Крестики нолики':
        chat_id = c.message.chat.id
        bot.send_message(chat_id = chat_id, text=f'Давай сыграем в крестики нолики! (есди тебе нужна инструкция, напиши в чат /инструкцияКН)')
        move_cs(chat_id, 0)
    if 'c&n' in c.data and c.data[4] == '0':
        chat_id = c.message.chat.id
        pos = cs_dic.get(int(c.data[3]))
        global df
        df = cs.create_field()
        df, err = cs.user_move(df, pos, chat_id)
        bot.send_document(chat_id = chat_id, caption = 'Ваш ход', document = open(f'\output\output_{chat_id}.png', 'rb'))
        df = cs.AI_move(df, chat_id)
        bot.send_document(chat_id = chat_id, caption = 'Ход бота', document = open(f'\output\output_{chat_id}.png', 'rb'))
        bot.send_message(chat_id = chat_id, text = 'Ваш ход!')
        move_cs(chat_id, 1)
    elif 'c&n' in c.data and c.data[4] != '0':
        chat_id = c.message.chat.id
        pos = cs_dic.get(int(c.data[3]))
        df, err = cs.user_move(df, pos, chat_id)
        if err == 0:
            bot.send_document(chat_id = chat_id, caption = 'Ваш ход', document = open(f'\output\output_{chat_id}.png', 'rb'))
            win = cs.check_win(df)
            if win != 1:
                bot.send_message(chat_id=chat_id, text=win)
            else:
                df = cs.AI_move(df, chat_id)
                bot.send_document(chat_id=chat_id, caption='Ход бота', document=open(f'\output\output_{chat_id}.png', 'rb'))
                win = cs.check_win(df)
                if win == 1:
                    bot.send_message(chat_id=chat_id, text='Ваш ход!')
                    move_cs(chat_id, 1)
                else:
                    bot.send_message(chat_id=chat_id, text = win)
        else:
            bot.send_message(chat_id=chat_id, text = err)
            bot.send_message(chat_id=chat_id, text = 'Попытайтесь снова')
            move_cs(chat_id, 1)


@bot.callback_query_handler(func = lambda c: c.data == '/инструкция')
def s_i(c): send_instr(c.message.chat.id)

@bot.message_handler(commands = ['инструкция', 'инструкция КН'])
def send_ins(mess):
    chat_id = mess.chat.id
    if mess.text == '/инструкция КН':
        bot.send_message(chat_id, text = 'Принцип игры - составить три символа в ряд (по вертикали, горизонтали или по диагонали).\n Вы играете символом \'X\' и ходите первым.\n Против вас играю я, хожу - \'0\'\n Чтобы поставить символ вам нужно нажать кнопку (их вы увидите в процессе игры) с номером клетки в которую вы ходите поставить символ.')
        bot.send_document(chat_id, caption = 'Нумерация клеточек', document = open('/data/Разметка КН.png', 'rb'))
    if mess.text == '/инструкция': send_instr(chat_id)







p = 0
while p ==0:
    print('Processing')
    p =1
bot.infinity_polling()