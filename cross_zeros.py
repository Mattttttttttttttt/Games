import pandas as pd
from csv2pdf import convert
import fitz
import random
import os

col_names = ['A', 'B', 'C']
df = pd.DataFrame(columns = col_names, index = [1, 2, 3])
path = 'D:\Desktop\Программы Питон\Games\output'

def user_move(position, user_id):
    df.iloc[position[0]][position[1]] = 'X'
    save(df, user_id)


def save(df, user_id):
    df.to_csv(path + f'\output_{user_id}.csv')
    convert(path + f'\output_{user_id}.csv', path + f'\output_{user_id}.pdf', size = 60)
    doc = fitz.open(path + f'\output_{user_id}.pdf')
    pic = doc.load_page(0).get_pixmap()
    pic.save(path + f'\output_{user_id}.png')
    doc.close()
    os.remove(path + f'\output_{user_id}.csv')
    os.remove(path + f'\output_{user_id}.pdf')


def AI_move(df, user_id):
    lucky = 1
    position = [0, 0]
    pos = [0, 0]
    b = 0
    for i in range(3):
        for j in range(3):
            if df.iloc[i, j] == 'X':
                pos = [i, j]
                df.iloc[i, j] = 'x'
                if 'X' in str(df.iloc[i, :]):
                    df.iloc[pos[0], pos[1]] = 'X'
                    for z in range(3):
                        if df.iloc[i, z] != 'X' and df.iloc[i, z] != '0':
                            df.iloc[i, z] = '0'
                            save(df, user_id)
                            b = 1
                            lucky = 0
                            break
                elif 'X' in str(df.iloc[:, j]):
                    df.iloc[pos[0], pos[1]] = 'X'
                    for z in range(3):
                        if df.iloc[z, j] != 'X' and df.iloc[z, j] != '0':
                            df.iloc[z, j] = '0'
                            save(df, user_id)
                            b = 1
                            lucky = 0
                            break
                df.iloc[i, j] = 'X'
            if b == 1: break
        if b == 1: break
    for i in range(3):
        if df.iloc[i, i] == 'X':
            pos = [i, i]
            df.iloc[i, i] = 'x'

    while lucky == 1:
        print('Empty')
        position[0] = random.randint(0, 2)
        position[1] = random.randint(0, 2)
        if pd.isnull(df.iloc[position[0], position[1]]) == True:
            df.iloc[position[0], position[1]] = '0'
            save(df, user_id)
            lucky = 0


user_id = '1234'
#save(df, user_id)
df.iloc[0, 0] = 'X'
df.iloc[1, 0] = '0'
df.iloc[2, 0] = 'X'
#df.iloc[0, 1] = 'X'
AI_move(df, user_id)

