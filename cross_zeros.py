import pandas as pd
from csv2pdf import convert
import fitz
import random
import os

#path = 'D:\Desktop\Программы Питон\Games\output'

def create_field():
    col_names = ['A', 'B', 'C']
    df = pd.DataFrame(columns = col_names, index = [1, 2, 3])
    return(df)

def user_move(df, position, user_id):
    if df.iloc[position[0]][position[1]] == '0':
        return(df, 'Ошибка, это место уже занято')
    elif df.iloc[position[0]][position[1]] == 'X':
        return(df, 'Ошибка, вы уже ходили сюда')
    else:
        df.iloc[position[0]][position[1]] = 'X'
        save(df, user_id)
        return(df, 0)


def save(df, user_id):
    df.to_csv(f'/data/output/output_{user_id}.csv')
    convert(f'/data/output/output_{user_id}.csv', f'/data/output_{user_id}.pdf', size = 60)
    doc = fitz.open(f'/data/output/output_{user_id}.pdf')
    pic = doc.load_page(0).get_pixmap()
    pic.save(f'/data/output/output_{user_id}.png')
    doc.close()
    os.remove(f'/data/output/output_{user_id}.csv')
    os.remove(f'/data/output/output_{user_id}.pdf')


def AI_move(df, user_id):
    lucky = 1
    c_1 = 0
    c_2 = 0
    position = [0, 0]
    for i in range(3):
        c_rows = 0
        c_col = 0
        for j in range(3):
            if df.iloc[i][j] == 'X': c_col += 1
            if df.iloc[j][i] == 'X': c_rows += 1
            if c_col == 2:
                for z in range(3):
                    if df.iloc[i, z] != 'X' and df.iloc[i, z] != '0':
                        df.iloc[i, z] = '0'
                        save(df, user_id)
                        return(df)
            elif c_rows == 2:
                for z in range(3):
                    if df.iloc[z, i] != 'X' and df.iloc[z, i] != '0':
                        df.iloc[z, i] = '0'
                        save(df, user_id)
                        return(df)
        if df.iloc[i, i] == 'X': c_1 += 1
        if df.iloc[i, 2 - i] == 'X': c_2 += 1
        if c_1 == 2:
            for z in range(3):
                if df.iloc[z, z] != 'X' and df.iloc[z, z] != '0':
                    df.iloc[z, z] = '0'
                    save(df, user_id)
                    return(df)
        elif c_2 == 2:
            for z in range(3):
                if df.iloc[z, 2 - z] != 'X' and df.iloc[z, 2 - z] != '0':
                    df.iloc[z, 2 - z] = '0'
                    save(df, user_id)
                    return(df)

    while lucky == 1:
        position[0] = random.randint(0, 2)
        position[1] = random.randint(0, 2)
        if pd.isnull(df.iloc[position[0], position[1]]):
            df.iloc[position[0], position[1]] = '0'
            save(df, user_id)
            return (df)
            lucky = 0


def check_win(df):
    AI_win = [0, 0, 0, 0]
    user_win = [0, 0, 0, 0]
    nol = 0
    for i in range(3):
        AI_win[0] = 0
        AI_win[1] = 0
        user_win[0] = 0
        user_win[1] = 0
        for j in range(3):
            if df.iloc[i, j] == 'X': user_win[0] += 1
            if df.iloc[i, j] == '0': AI_win[0] += 1
            if df.iloc[j, i] == 'X': user_win[1] += 1
            if df.iloc[j, i] == '0': AI_win[1] += 1
            if AI_win[0] == 3 or AI_win[1] == 3: return('Компьютер выиграл!')
            if user_win[0] == 3 or user_win[1] == 3: return('Пользователь выиграл!')
            if pd.isnull(df.iloc[i, j]): nol += 1
        if df.iloc[i, i] == 'X': user_win[2] += 1
        if df.iloc[i, i] == '0': AI_win[2] += 1
        if df.iloc[i, 2 - i] == 'X': user_win[3] += 1
        if df.iloc[i, 2 - i] == '0': AI_win[3] += 1
        if AI_win[2] == 3 or AI_win[3] == 3: return ('Компьютер выиграл!')
        if user_win[2] == 3 or user_win[3] == 3: return ('Пользователь выиграл!')
    if nol == 0: return('Ничья! Место для ходов закончилось!')
    return(1)