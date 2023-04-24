from dash import Dash, html, Input, Output, dcc, ctx
import numpy as np
import pygame as pg
import time

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
    #resetKeyBoard()

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

pg.mixer.init()
pg.init()

keys = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
pitch_levels = range(1, 8)
notes, notes_freq = [], []
num_total = num_right = 0
note_index = -1
pitch_base = "None"

def getNoteSelectors():
    return html.Tr(
        children = 
            [
                html.Td("")
            ] +
            [
                html.Td(
                    children=[
                        dcc.Checklist(
                            [
                                {
                                    "label": html.Span(""),
                                    "value": keys[i]
                                }
                            ],
                            value=[],
                            id=f"chk_{keys[i]}"
                        )
                    ]
                ) for i in range(len(keys))
            ]
        )

def getNotes():
    return (
        html.Tbody(
            children = [
                html.Tr(
                    children = 
                        [
                            dcc.Checklist(
                                [
                                    {
                                        "label": html.Span(""),
                                        "value": pitch_levels[i]
                                    }
                                ],
                                value=[],
                                id=f"chk_{pitch_levels[i]}"
                            )
                        ] +
                        [
                            html.Td(
                                children=[
                                    html.Button(
                                        f"{keys[j]}{pitch_levels[i]}",
                                        id=f"btn_{keys[j]}{pitch_levels[i]}",
                                        disabled=True
                                    )
                                ]
                            ) for j in range(len(keys))
                        ]
                ) for i in range(len(pitch_levels))
            ]
        )
    )

app = Dash(__name__)
app.title = "Music By Ear"

app.layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                keys,
                                placeholder="Select a node base (Optional)",
                                style={
                                    "width":"300px"
                                }
                            ),
                        ],
                        style={
                            "width": "100%",
                            "display": "flex",
                            "justifyContent": "center"
                        }
                    ),
                    html.Div(
                        children=[
                            html.Table(
                                children=[
                                    html.Thead(
                                        children=[
                                            getNoteSelectors()
                                        ]
                                    ),
                                    getNotes()
                                ]
                            )
                        ],
                        style={
                            "width": "100%",
                            "display": "flex",
                            "justifyContent": "center"
                        }
                    ),
                    html.Div(
                        children=[
                            html.Button(
                                "Play Note",
                                id=f"btn_play_note",
                            )
                        ]
                    ),
                     html.P(id='placeholder')
                ],
                style={
                    "width": "100%",
                    "display": "flex",
                    "flexDirection": "column",
                    "width": "80%",
                    "height": "80%",
                    "border": "1px solid"
                }
            )
        ],
        style = {
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "padding": "20px"
        }
)

@app.callback(
    Output("placeholder", "children"),
    Input("btn_play_note", "n_clicks"),
    prevent_initial_call = True
)
def playNoteCallback(play_btn):
    global notes, note_index
    if ctx.triggered_id == "btn_play_note": 
        notes = [f'{k}{p}' for k in keys for p in pitch_levels]
        note_index = 0
        for _ in range(10):
            playNote()


if __name__ == '__main__':
    app.run_server(debug=True)