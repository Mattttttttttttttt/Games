import random

def generate():
    while True:
        err = 0
        num = str(random.randint(99,10000))
        if len(num) ==3: num = '0' +num
        for i in range(3):
            for j in range(i+1, 4):
                if num[i] == num[j]: err = 1
        if err == 0: break

    return(num)


def check(gen, num):
    c, b = 0, 0
    for i in range(4):
        if gen[i] == num[i]:
            b += 1
            c-=1
        if num[i] in gen: c+=1
    return b, c


