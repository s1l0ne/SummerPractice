import tkinter as tk
import random
from tkinter import simpledialog as sd
from tkinter import messagebox as mb


def change_level():
    new_lvl = sd.askinteger(title='Выбор уровня', prompt='Введите номер уровня (от 1 до 50)')
    if new_lvl < 1 or new_lvl > 50:
        mb.showerror(title='Change level error',
                     message='Введен неверный номер уровня (автоматически установлено на 1)')
        new_lvl = 1

    prepare_and_start()

    for i in range(new_lvl - 1):
        next_level(0)


def change_difficulty():
    global difficulty
    difficulty += 1
    difficulty %= 2
    if difficulty:
        difficulty_button.configure(text='Понизить сложность ботов')
    else:
        difficulty_button.configure(text='Повысить сложность ботов')
    prepare_and_start()


def get_new_pos(add=True):
    while True:
        pos = (random.randint(0, N_X - 1) * step,
               random.randint(0, N_Y - 1) * step)
        if pos not in coords:
            if add:
                coords.append(pos)
            return pos


def to_player(c):
    p = canvas.coords(player)

    x = step
    if c[0] > p[0]:
        if c[0] - p[0] <= N_X * step - c[0] + p[0]:
            x = -step
    elif p[0] > c[0]:
        if N_X * step - p[0] + c[0] < p[0] - c[0]:
            x = -step
    else:
        x = 0

    y = step
    if c[1] > p[1]:
        if c[1] - p[1] <= N_Y * step - c[1] + p[1]:
            y = -step
    elif p[1] > c[1]:
        if N_Y * step - p[1] + c[1] < p[1] - c[1]:
            y = -step
    else:
        y = 0

    if difficulty == 0 and x != 0 and y != 0:
        if random.randint(0, 1):
            x = 0
        else:
            y = 0

    return x, y


def prepare_and_start():
    canvas.delete('all')
    global player, obj_exit, fires, enemies, level, coords

    coords = []

    level = 1

    player_pos = get_new_pos()

    exit_pos = get_new_pos()

    player = canvas.create_image(
        player_pos,
        image=player_pic,
        anchor='nw'
    )

    obj_exit = canvas.create_image(
        exit_pos,
        image=exit_pic,
        anchor='nw'
    )

    fires = []
    for i in range(N_FIRES):
        fire_pos = get_new_pos()
        fire = canvas.create_image(
            (fire_pos[0], fire_pos[1]),
            image=fire_pic,
            anchor='nw'
        )
        fires.append(fire)

    enemies = []
    for i in range(N_ENEMIES):
        enemy_pos = get_new_pos()

        enemy = canvas.create_image(
            enemy_pos,
            image=enemy_pic,
            anchor='nw'
        )

        enemies.append((enemy, random.choice([to_player])))

    label.configure(text='Найди выход (уровень 1)')
    master.bind('<KeyPress>', key_pressed)


def next_level(event):
    for i in range(N_ENEMIES):
        coords[2 + N_FIRES + i] = get_new_pos(add=False)
        canvas.moveto(enemies[i][0], *coords[2 + N_FIRES + i])

    coords[0] = get_new_pos(add=False)
    canvas.moveto(player, *coords[0])

    coords[1] = get_new_pos(add=False)
    canvas.moveto(obj_exit, *coords[1])

    if step == 15:
        for i in range(N_FIRES):
            fire_pos = get_new_pos()
            fire = canvas.create_image(
                (fire_pos[0], fire_pos[1]),
                image=fire_pic,
                anchor='nw'
            )
            fires.append(fire)
    else:
        for i in range(N_FIRES):
            fire_pos = get_new_pos()
            fire = canvas.create_oval(
                (fire_pos[0], fire_pos[1]),
                (fire_pos[0] + step, fire_pos[1] + step),
                fill='red'
            )
            fires.append(fire)

    global level
    level += 1
    if level == 51:
        canvas.delete('all')
        label.configure(text='Ты - легенда! Игра пройдена')
        mb.showinfo(title='Победа!', message='Игра пройдена! Ты - легенда Night-Petersburg!')
        master.bind('<KeyPress>', do_nothing)
    else:
        label.configure(text=f'Найди выход (уровень {level})')
        master.bind('<KeyPress>', key_pressed)


def move_wrap(obj, move):
    canvas.move(obj, move[0], move[1])
    if canvas.coords(obj)[0] >= step * N_X:
        canvas.move(obj, -step * N_X, 0)
    elif canvas.coords(obj)[1] >= step * N_Y:
        canvas.move(obj, 0, -step * N_Y)
    elif canvas.coords(obj)[0] + step <= 0:
        canvas.move(obj, step * N_X, 0)
    elif canvas.coords(obj)[1] + step <= 0:
        canvas.move(obj, 0, step * N_Y)


def do_nothing(event):
    pass


def check_move():
    if canvas.coords(player)[:2] == canvas.coords(obj_exit)[:2]:
        win()

    global fires
    for f in fires:
        if canvas.coords(player)[:2] == canvas.coords(f)[:2]:
            lose()

    global enemies
    for e in enemies:
        if canvas.coords(player)[:2] == canvas.coords(e[0])[:2]:
            lose()


def lose():
    label.config(text='Ты проиграл!')
    master.bind("<KeyPress>", do_nothing)


def win():
    label.config(text='Ты выиграл!')
    master.bind("<KeyPress>", next_level)


def key_pressed(event):
    if event.keysym == 'Up':
        move_wrap(player, (0, -step))
    elif event.keysym == 'Down':
        move_wrap(player, (0, step))
    elif event.keysym == 'Right':
        move_wrap(player, (step, 0))
    elif event.keysym == 'Left':
        move_wrap(player, (-step, 0))
    check_move()
    for enemy in enemies:
        move_wrap(enemy[0], enemy[1](canvas.coords(enemy[0])))
    check_move()


master = tk.Tk()
master.geometry("760x798")
master.title('Сбеги от грусти')

step = 15

player_pic = tk.PhotoImage(file="player.png")
exit_pic = tk.PhotoImage(file="exit.png")
fire_pic = tk.PhotoImage(file="fire.png")
enemy_pic = tk.PhotoImage(file="enemy.png")

N_X = 50
N_Y = 50
N_FIRES = 6
N_ENEMIES = 4

fires = []
enemies = []
coords = []

player: int
obj_exit: int

difficulty = 0
level = 1

canvas = tk.Canvas(master, bg='#969696',
                   width=step * N_X, height=step * N_Y)

label = tk.Label(master, text="Найди выход (уровень 1)")
label.place(relx=0.5, y=0, anchor='n')
canvas.place(relx=0.5, y=20, anchor='n')

restart = tk.Button(master, text='Начать заново', command=prepare_and_start)
restart.place(relx=1, y=772, anchor='ne')

difficulty_button = tk.Button(master, text='Повысить сложность ботов', command=change_difficulty)
difficulty_button.place(relx=0, y=772, anchor='nw')

choose_lvl = tk.Button(master, text='Выбрать уровень', command=change_level)
choose_lvl.place(relx=0.5, y=772, anchor='n')

prepare_and_start()

master.mainloop()
