from dash import Dash, html, Input, Output, dcc, callback, ctx, ALL
import numpy as np
import pygame as pg
import time

pg.mixer.init()
pg.init()

keys = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
pitch_levels = range(3, 6)
notes, notes_freq = [], []
num_total = num_right = 0
note_index = -1
note_count = 1
note_base = ""

def selectNewNote():
    global note_index
    p = np.array(notes_freq)/np.sum(notes_freq)
    note_index = np.random.choice(len(notes), 1, p=p)[0]

def playNote():
    if note_index < 0: selectNewNote()
    if note_base != '':
        note_path = f'assets/notes/{note_base}.mp3'
        pg.mixer.Sound(note_path).play()
        time.sleep(1)
    note_path = f'assets/notes/{notes[note_index]}.mp3'
    pg.mixer.Sound(note_path).play()
    time.sleep(2)
    pg.mixer.stop()

def playNewNote():
    if not notes: return
    for _ in range(note_count):
        selectNewNote()
        playNote()

def getNoteColSelectors():
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
                            id={
                                'type': f"chk_k",
                                'index': keys[i]
                            }
                        )
                    ]
                ) for i in range(len(keys))
            ]
        )

def getNotes(rows={}, cols={}):
    return (
        [
            html.Tr(
                children = 
                    [
                        html.Td(
                            children=[
                                dcc.Checklist(
                                    [
                                        {
                                            "label": html.Span(""),
                                            "value": pitch_levels[i]
                                        }
                                    ],
                                    value=[pitch_levels[i]] if pitch_levels[i] in rows else [],
                                    id={
                                        'type': f"chk_p",
                                        'index': pitch_levels[i]
                                    }
                                )
                            ]
                        )
                    ] +
                    [
                        html.Td(
                            children=[
                                html.Button(
                                    f"{keys[j]}{pitch_levels[i]}",
                                    id={
                                        "type":"btn_note",
                                        "index": f"{keys[j]}{pitch_levels[i]}"
                                    },
                                    disabled= (f"{keys[j]}{pitch_levels[i]}" not in notes),
                                    n_clicks=0
                                )
                            ]
                        ) for j in range(len(keys))
                    ]
            ) for i in range(len(pitch_levels))
        ]
    )

app = Dash(__name__)
app.title = "Ear Training"

app.layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                options=notes,
                                id='node_base_selector',
                                placeholder="Select a node base (Optional)",
                                style={
                                    "width":"250px"
                                }
                            ),
                            dcc.Dropdown(
                                options=list(range(1, len(notes)+int(note_base==""))),
                                id='node_count_selector',
                                placeholder="Select number of notes (Optional)",
                                style={
                                    "width":"250px"
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
                                            getNoteColSelectors()
                                        ]
                                    ),
                                    html.Tbody(
                                        id = 'btn_container',
                                        children=getNotes()
                                    )
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
                        children=[html.Button(
                                    'Play',
                                    id=f"btn_play",
                                    n_clicks=0
                                )
                        ],
                        style={"display":"flex", "justifyContent": "center"}
                    ),
                    html.Div(
                        children=[
                            html.P(
                                id='placeholder'
                            )
                        ],
                        style={"display":"flex", "justifyContent": "center"}
                    ),
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

@callback(
    Output("placeholder", "children", allow_duplicate=True),
    Input('node_base_selector', 'value'),
    prevent_initial_call = True
)
def select_note_base(value):
    global note_base
    note_base = value
    return ''

@callback(
    Output("placeholder", "children", allow_duplicate=True),
    Input('node_count_selector', 'value'),
    prevent_initial_call = True
)
def select_note_count(value):
    global note_count
    note_count = value
    return ''

@callback(
    Output('btn_container', 'children'),
    Output('node_base_selector', 'options'),
    Output('node_count_selector', 'options'),
    Input({'type': 'chk_p', 'index': ALL}, 'value'),
    Input({'type': 'chk_k', 'index': ALL}, 'value'),
    prevent_initial_call = True
)
def check_columns(rows, cols):
    global notes, notes_freq
    rows = {item[0] for item in rows if len(item) > 0}
    cols = {item[0] for item in cols if len(item) > 0}
    if rows and cols:
        notes = [f'{k}{p}' for p in pitch_levels for k in keys if k in cols and p in rows]
    elif rows:
        notes = [f'{k}{p}' for p in pitch_levels for k in keys if p in rows]
    elif cols:
        notes = [f'{k}{p}' for p in pitch_levels for k in keys if k in cols]
    else:
        notes = []
    notes_freq = [1]*len(notes)
    return getNotes(rows=rows, cols=cols), notes, list(range(1, max(2, len(notes)+int(note_base==""))))

@callback(
    Output("placeholder", "children", allow_duplicate=True),
    Input('btn_play', 'n_clicks'),
    prevent_initial_call = True
)
def play(value):
    if ctx.triggered_id == 'btn_play' and value > 0:
        playNewNote()

@callback(
    Output("placeholder", "children"),
    Input({'type':'btn_note', 'index':ALL}, 'n_clicks'),
    prevent_initial_call = True
)
def match(n_clicks):
    if len(ctx.triggered_prop_ids) == 1 and -1 < note_index < len(notes): return "Matched !!" if ctx.triggered_id['index'] == notes[note_index] else "Wrong !!"

if __name__ == '__main__':
    app.run_server(debug=True)