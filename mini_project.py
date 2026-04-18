# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 10:46:05 2025

@author: lenovo
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame
import sys
import os

# 🔧 Fix paths for EXE
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 🔊 Initialize sound
pygame.mixer.init()

# 🔊 Load sounds
start_sound = pygame.mixer.Sound(resource_path("sounds/start.wav"))
win_sound = pygame.mixer.Sound(resource_path("sounds/win.wav"))

window = None
entry_player1 = None
entry_player2 = None

def show_start_window():
    global window, entry_player1, entry_player2
    window = tk.Tk()
    window.title("Memory Hunt - Welcome")
    window.attributes('-fullscreen', True)
    window.config(bg="#ADD8E6")

    img = Image.open(resource_path("logo.png")).resize((300, 100))
    photo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(window, image=photo, bg="#ADD8E6")
    logo_label.image = photo
    logo_label.pack(pady=20)

    title_label = tk.Label(window, text="🌟 Welcome to Memory Hunt! 🌟", font=("Comic Sans MS", 26, "bold"), bg="#ADD8E6", fg="#FF4500")
    title_label.pack(pady=10)

    player1_label = tk.Label(window, text="Enter Player 1 Name:", font=("Comic Sans MS", 16), bg="#ADD8E6", fg="#3333CC")
    player1_label.pack(pady=5)
    entry_player1 = tk.Entry(window, font=("Comic Sans MS", 16))
    entry_player1.pack(pady=10)

    player2_label = tk.Label(window, text="Enter Player 2 Name:", font=("Comic Sans MS", 16), bg="#ADD8E6", fg="#FF1493")
    player2_label.pack(pady=5)
    entry_player2 = tk.Entry(window, font=("Comic Sans MS", 16))
    entry_player2.pack(pady=10)

    start_button = tk.Button(window, text="🎈 Let's Start! 🎈", font=("Comic Sans MS", 18, "bold"), bg="#32CD32", fg="white", command=start_game)
    start_button.pack(pady=40)

    window.mainloop()

def start_game():
    p1 = entry_player1.get()
    p2 = entry_player2.get()
    if p1 == "" or p2 == "":
        messagebox.showwarning("Oops!", "Please enter names for both players!")
        return
    window.destroy()
    create_game_window(p1, p2)

def create_game_window(p1, p2):
    game = tk.Tk()

    # 🔊 Play start sound
    start_sound.play()

    game.title("Memory Hunt")
    game.attributes('-fullscreen', True)
    game.config(bg="#FFF8DC")

    moves = [0]
    turn = [p1]
    scores = {p1: 0, p2: 0}
    selected = []
    matched = []

    images = []
    for i in range(1, 19):
        img = Image.open(resource_path("images/img_" + str(i) + ".png")).resize((80, 80))
        photo = ImageTk.PhotoImage(img)
        images.append(photo)
        images.append(photo)
    random.shuffle(images)

    info = tk.Frame(game, bg="#FFF8DC")
    info.pack(pady=10)

    move_lbl = tk.Label(info, text="Moves: 0", font=("Comic Sans MS", 16, "bold"), bg="#FFF8DC")
    move_lbl.grid(row=0, column=0, padx=20)

    turn_lbl = tk.Label(info, text="Turn: " + turn[0], font=("Comic Sans MS", 16, "bold"), bg="#FFF8DC")
    turn_lbl.grid(row=0, column=1, padx=20)

    score_lbl = tk.Label(info, text=p1 + ": 0  |  " + p2 + ": 0", font=("Comic Sans MS", 16, "bold"), bg="#FFF8DC")
    score_lbl.grid(row=0, column=2, padx=20)

    blank_img = ImageTk.PhotoImage(Image.new("RGB", (80, 80), color="#87CEEB"))
    board = tk.Frame(game, bg="#FFF8DC")
    board.pack()

    buttons = []

    def update_info():
        move_lbl.config(text="Moves: " + str(moves[0]))
        turn_lbl.config(text="Turn: " + turn[0])
        score_lbl.config(text=p1 + ": " + str(scores[p1]) + "  |  " + p2 + ": " + str(scores[p2]))

    def tile_click(i):
        if i in matched or i in [x[0] for x in selected]:
            return
        buttons[i].config(image=images[i])
        selected.append((i, images[i]))
        if len(selected) == 2:
            game.after(500, check_match)

    def check_match():
        i1, img1 = selected[0]
        i2, img2 = selected[1]
        if img1 == img2:
            matched.append(i1)
            matched.append(i2)
            scores[turn[0]] += 1
        else:
            buttons[i1].config(image=blank_img)
            buttons[i2].config(image=blank_img)
            if turn[0] == p1:
                turn[0] = p2
            else:
                turn[0] = p1
        selected.clear()
        moves[0] += 1
        update_info()
        if len(matched) == 36:
            game.destroy()
            show_result(scores, p1, p2)

    for i in range(36):
        btn = tk.Button(board, image=blank_img, width=80, height=80, command=lambda i=i: tile_click(i))
        btn.grid(row=i // 6, column=i % 6, padx=5, pady=5)
        btn.image = blank_img
        buttons.append(btn)

    update_info()
    game.mainloop()

def show_result(scores, p1, p2):
    # 🔊 Play win sound
    win_sound.play()

    result = tk.Tk()
    result.title("Game Over")
    result.attributes('-fullscreen', True)
    result.config(bg="#FFF8DC")

    if scores[p1] > scores[p2]:
        msg = "🏆 " + p1 + " Wins! 🏆"
    elif scores[p2] > scores[p1]:
        msg = "🏆 " + p2 + " Wins! 🏆"
    else:
        msg = "🤝 It's a Draw! 🤝"

    result_label = tk.Label(result, text=msg, font=("Comic Sans MS", 28, "bold"), bg="#FFF8DC", fg="green")
    result_label.pack(pady=30)

    fig, ax = plt.subplots()
    ax.bar([p1, p2], [scores[p1], scores[p2]], color=['blue', 'green'])
    ax.set_title("Player Matches")
    ax.set_ylabel("Matches")
    ax.set_xlabel("Players")

    canvas = FigureCanvasTkAgg(fig, master=result)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    tk.Button(result, text="Play Again", font=("Comic Sans MS", 18, "bold"),
              bg="green", fg="white", command=lambda: [result.destroy(), show_start_window()]).pack(pady=30)

    result.mainloop()

# Start the game
show_start_window()
