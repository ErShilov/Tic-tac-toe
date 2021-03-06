import tkinter as tk
from tkinter import messagebox
import random

window = tk.Tk()
window.title('Tic-tac-toe')
window.iconbitmap('icon.ico')
deck = []
pl_smb = 'X'
ai_smb = 'O'
buttons = []


def new_game():
  """ Create new deck and clear buttons """
    deck.clear()
    deck.extend(list(range(9)))
    for i_line in buttons:
        for i_button in i_line:
            i_button['text'] = ' '


def button_click(row, col):
  """ Cange text on button, check win for user and start pc move """
    if isinstance(deck[row * 3 + col], int):
        buttons[row][col]['text'] = pl_smb
        deck[row * 3 + col] = pl_smb
        if check_win(deck, pl_smb):
            message(win=1)
            new_game()
        else:
            pc_step()


def but_config():
    for i_row in range(3):
        buttons_line = []
        for i_col in range(3):
            button = tk.Button(window, text=' ', width=5, height=2, border=1, font=('Arial Black', 20),
                               command=lambda row=i_row, col=i_col: button_click(row, col))
            button.grid(row=i_row, column=i_col)
            buttons_line.append(button)
        buttons.append(buttons_line)


def message(win=0, lose=0):
    if win == 1:
        box_title = 'Победа!!!'
        box_message = 'Вы победили!!!'
    elif lose == 1:
        box_title = 'Поражение!'
        box_message = 'Вы проиграли.'
    else:
        box_title = 'Ничья!'
        box_message = 'Возможно стоит сыграть еще'
    messagebox.showinfo(title=box_title, message=box_message)


def check_win(i_deck, player):
    for idx in range(3):
        line = all([True if i_deck[idx * 3 + jdx] == player else False
                    for jdx in range(3)])
        column = all([True if i_deck[idx + jdx * 3] == player else False
                      for jdx in range(3)])
        if line or column:
            return True
    line_1 = all([True if i_deck[idx] == player else False
                  for idx in [0, 4, 8]])
    line_2 = all([True if i_deck[idx] == player else False
                  for idx in [2, 4, 6]])
    if line_1 or line_2:
        return True
    return False


def check_draw(board):
    available_steps = [idx for idx in board if isinstance(idx, int)]
    if len(available_steps) == 0:
        return True
    return False


def get_step(board):
    move_index = None
    new_board = board[:]
    best_score = -1000
    for index in range(9):
        if isinstance(new_board[index], int):
            value = new_board[index]
            new_board[index] = ai_smb
            score = minimax(new_board, False)
            new_board[index] = value
            if score > best_score:
                best_score = score
                move_index = index
    return move_index


def minimax(board, ai_step):
    if check_win(board, ai_smb):
        return 10
    if check_win(board, pl_smb):
        return -10
    if check_draw(board):
        return 0
    new_board = board[:]
    if ai_step:
        best_score = -1000
        for index in range(9):
            if isinstance(new_board[index], int):
                value = new_board[index]
                new_board[index] = ai_smb
                score = minimax(new_board, False)
                new_board[index] = value
                if score > best_score:
                    best_score = score
    else:
        best_score = 1000
        for index in range(9):
            if isinstance(new_board[index], int):
                value = new_board[index]
                new_board[index] = pl_smb
                score = minimax(new_board, True)
                new_board[index] = value
                if score < best_score:
                    best_score = score
    return best_score


def pc_step():
    if check_draw(deck):
        message()
        new_game()
        return
    step = get_step(deck)
    deck[step] = ai_smb
    buttons[step // 3][step % 3]['text'] = ai_smb
    if check_win(deck, ai_smb):
        message(lose=1)
        new_game()


but_config()
new_game()
window.mainloop()
