import pygame as pg
import time, pdb
import numpy as np
import tkinter as tk

def selectNewNote():
    global note_index
    p = np.array(notes_freq)/np.sum(notes_freq)
    note_index = np.random.choice(len(notes), 1, p=p)[0]
    #print(notes[note_index])
    #print(notes_freq, p)

def playNote():
    if note_index < 0: selectNewNote()
    if pitch_base != 'None':
        note_path = f'assets/notes/Piano.ff.{pitch_base}.aiff'
        pg.mixer.Sound(note_path).play()
        time.sleep(1)
    note_path = f'assets/notes/Piano.ff.{notes[note_index]}.aiff'
    pg.mixer.Sound(note_path).play()
    time.sleep(2)
    pg.mixer.stop()
    resetKeyBoard()

def playNewNote():
    selectNewNote()
    playNote()

def selectNotesAndPitches():
    global notes, notes_freq
    notes = [f'{k}{p}' for i, k in enumerate(keys) for j, p in enumerate(pitch_levels) if note_select[i][1].get()==1 and pitch_select[j][1].get()==1]
    notes_freq = [1]*len(notes)
    resetKeyBoard() 

def resetKeyBoard():
    for i, keyboard_panel in enumerate(keyboard):
        pitch_select[i][0]['state'] = 'normal'
        for j, button in enumerate(keyboard_panel):
            note_select[j][0]['state'] = 'normal'
            button["state"] = "normal" if pitch_select[i][1].get() == 1 and note_select[j][1].get() == 1 else "disabled"

    play_button["state"] = "normal" if len(notes) else "disabled"

def disableKeyboard():
    for i, keyboard_panel in enumerate(keyboard):
        pitch_select[i][0]['state'] = 'disabled'
        for j, button in enumerate(keyboard_panel):
            note_select[j][0]['state'] = 'disabled'
            button["state"] = 'disabled'

def matchNote(note_clicked):
    global num_right, num_total
    num_total += 1
    #print(note_clicked)
    disableKeyboard()
    if notes[note_index].lower() != note_clicked.lower():
        keyboard_frame.config(bg="red")
        message_box.config(text=f'Wrong !!! {notes[note_index]} [{num_right} of {num_total}]')
        notes_freq[note_index] += 1
    else:
        num_right += 1
        keyboard_frame.config(bg="green")
        message_box.config(text=f'Matched !!! [{num_right} of {num_total}]')
    message_box.config(bg=message_box.master['bg'])
    root.update()
    time.sleep(2)
    playNewNote()

def setPitchBase(evt):
    global pitch_base
    pitch_base = pitch_base_value.get()

keys = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
pitch_levels = range(1, 8)
notes, notes_freq = [], []
num_total = num_right = 0
note_index = -1
pitch_base = 'None'

if __name__ == "__main__":

    root = tk.Tk()
    root.title('Learn note sound and pitch')

    pitch_base_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    pitch_base_frame.pack()
    tk.Label(pitch_base_frame, text="Select a pitch base (optional):").pack(side=tk.LEFT, padx=5, pady=5)
    pitches = ['None'] + [f'{key}{level}' for key in keys for level in pitch_levels]
    pitch_base_value = tk.StringVar(pitch_base_frame)
    pitch_base_value.set("None") # default value
    pitch_base_selector = tk.OptionMenu(pitch_base_frame, pitch_base_value, *pitches, command=setPitchBase)
    pitch_base_selector.pack(side=tk.RIGHT)
    #pitch_base_selector.bind('<<ComboboxSelected>>', setPitchBase)

    keyboard_frame = tk.Frame(root, bg='white', padx=10, pady=10)
    keyboard_frame.pack()

    row_index = 0

    message_box = tk.Label(keyboard_frame, font=("Courier", 40), height=5, bg='white')
    message_box.grid(row=row_index, columnspan=len(keys)+1)

    row_index += 1

    keyboard, note_select, pitch_select = [], [], []

    for i in range(len(keys)):
        var = tk.IntVar()
        var.set(0)
        note_select.append([tk.Checkbutton(keyboard_frame, onvalue=1, offvalue=0, variable=var, command=selectNotesAndPitches), var])
        note_select[-1][0].grid(row=row_index, column=i+1)

    row_index += 1

    for i, p in enumerate(pitch_levels):

        var = tk.IntVar()
        var.set(0)
        pitch_select.append([tk.Checkbutton(keyboard_frame, onvalue=1, offvalue=0, variable=var, command=selectNotesAndPitches), var])
        pitch_select[-1][0].grid(row=i+2, column=0)
        keyboard_panel = []
        for j, k in enumerate(keys):
            note = f'{k}{p}'
            keyboard_panel.append(tk.Button(keyboard_frame, state="disabled", text=note, bg='white', width=3, height=2, cursor='hand', command=lambda n=note:matchNote(n)))
            keyboard_panel[-1].grid(row=row_index, column=j+1)
        keyboard.append(keyboard_panel)
        row_index += 1

    play_button = tk.Button(keyboard_frame, text="Play", state="disabled", command=playNote)
    play_button.grid(row=row_index, columnspan=len(keys)+1, sticky='NS')

    pg.mixer.init()
    pg.init()

    w = root.winfo_width() # width for the Tk root
    h = root.winfo_height() # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    root.mainloop()