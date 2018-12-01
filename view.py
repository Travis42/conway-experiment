from tkinter import *

from coin_flip import coin_flip
from markov_model import markovModelNormalized
from patterns import glider_pattern, glider_gun_pattern
from tradmodel import tradModel

cell_size: int = 5
is_running: bool = False
model_name = "Traditional"
model = None
height = 100
width = 100


def setup():
    global root, grid_view, cell_size, start_button, clear_button, choice

    root = Tk()
    root.title('The Game of Life')

    grid_view = Canvas(root, width=width * cell_size, height=height * cell_size,
                       borderwidth=0, highlightthickness=0, bg='white')

    start_button = Button(root, text='Start', width=12)
    clear_button = Button(root, text='Clear', width=12)

    # tk object that stores a string.
    choice = StringVar(root)
    choice.set('Choose a Pattern')
    # OptionMenu takes the root window, the choice object, and we can write
    # in our various options:
    option = OptionMenu(root, choice, 'Choose a Pattern', 'glider',
                        'glider gun', 'random', command=option_handler())
    option.config(width=20)

    # tk object that stores a string.
    ruleset = StringVar(root)
    ruleset.set('Choose a Rule Set')
    # OptionMenu takes the root window, the ruleset object, and we can write
    # in our various options:
    rules = OptionMenu(root, ruleset, 'Traditional',
                       "Markov Neighbors Normalized", "Coin Flip Traditional",
                       command=ruleset_handler()
                       # for binding to functions in menu
                       )
    rules.config(width=30)

    # makes the play area clickable to toggle cells:
    grid_view.grid(row=0, columnspan=3, padx=20, pady=20)
    grid_view.bind('<Button-1>', grid_handler)

    start_button.grid(row=1, column=0, sticky=W, padx=20, pady=20)
    start_button.bind('<Button-1>', start_handler)
    option.grid(row=1, column=1, padx=20)
    rules.grid(row=2, column=1, padx=20)
    clear_button.grid(row=1, column=2, sticky=E, padx=20, pady=20)
    clear_button.bind('<Button-1>', clear_handler)


def ruleset_handler():
    global is_running, start_button, grid_model, next_grid_model, model, \
        model_name

    is_running = False
    start_button.configure(text='Start')

    if model == "Markov Neighbors Normalized":
        model = markovModelNormalized(grid_model, next_grid_model)
    elif model == "Coin Flip Traditional":
        model = coin_flip(grid_model, next_grid_model)
    else:
        model = tradModel(grid_model, next_grid_model)
    update()


def option_handler():
    global is_running, start_button, choice, model

    is_running = False
    start_button.configure(text='Start')

    # whatever the user selects is within the object choice.
    selection = choice.get()

    # select the var
    if selection == 'glider':
        model.load_pattern(glider_pattern, 10, 10)
    elif selection == 'glider gun':
        model.load_pattern(glider_gun_pattern, 10, 10)
    elif selection == 'random':
        model.randomize(model.grid_model, width, height)

    update()


def start_handler():
    """
    Changes state based on condition of button press.
    """
    global is_running, start_button

    if is_running:
        is_running = False
        start_button.configure(text='Start')
    else:
        is_running = True
        start_button.configure(text='Pause')
        update()


def clear_handler():
    global is_running, start_button, model

    is_running = False
    # change all cells to 0 to clear the slate:
    for i in range(0, height):
        for j in range(0, width):
            model.grid_model[i][j] = 0

    start_button.configure(text='Start')
    update()


def grid_handler(event):
    global grid_view, cell_size

    x = int(event.x / cell_size)
    y = int(event.y / cell_size)

    # based on a click, change the state of the cell (binary flip)
    if model.grid_model[x][y] == 1:
        model.grid_model[x][y] = 0
        draw_cell(x, y, 'white')
    else:
        model.grid_model[x][y] = 1
        draw_cell(x, y, 'black')


def update():
    global grid_view, root, is_running, model, grid_model, next_grid_model, \
        height, width

    grid_view.delete(ALL)
    grid_model, next_grid_model = model.next_gen()  # was model.next_gen()
    for i in range(0, height):
        for j in range(0, width):
            if model.grid_model[i][j] == 1:
                draw_cell(i, j, 'black')
    if is_running:
        root.after(50, update)


def draw_cell(row, col, color):
    global grid_view, cell_size

    if color == 'black':
        outline = 'grey'
    else:
        outline = 'white'

    grid_view.create_rectangle(row * cell_size, col * cell_size,
                               row * cell_size + cell_size,
                               col * cell_size + cell_size, fill=color,
                               outline=outline)


grid_model = [0] * height
next_grid_model = [0] * height
for n in range(height):
    grid_model[n] = [0] * width
    next_grid_model[n] = [1] * width

if __name__ == '__main__':
    setup()
    update()
    # tk function for monitoring for state change in buttons.
    mainloop()
