#!/usr/bin/env python3
"""Generuje projekt Scratcha (.sb3) rysujacy symetryczny wzor z luków.

Jedna figura (jeden ciagly slad pisaka):
  - duzy luk 180 stopni ("kopula"),
  - zawrot o 180 stopni,
  - dwa male luki 180 stopni spotykajace sie w ostrym dziobku na srodku.

Program w Scratchu:
  - po kliknieciu zielonej flagi pyta "Ile figur mam narysowac?",
  - rysuje tyle figur, ile podal uzytkownik, obracajac kazda
    o (360 / liczba figur) stopni wokol srodka sceny,
  - kazda kolejna figura jest bardziej przezroczysta (pen transparency).
"""
import hashlib
import json
import zipfile
from pathlib import Path

OUT = Path(__file__).parent / "wirujace_spirale.sb3"

# --- identyfikatory zmiennych -------------------------------------------------
VAR_FIGURY = ("figury", "var_figury")
VAR_KIERUNEK = ("kierunek", "var_kierunek")


def var_input(var, shadow=(4, "10")):
    """Zmienna wstawiona w okienko bloku (z domyslnym cieniem)."""
    return [3, [12, var[0], var[1]], list(shadow)]


def block(opcode, nxt=None, parent=None, inputs=None, fields=None,
          shadow=False, top=False):
    b = {
        "opcode": opcode,
        "next": nxt,
        "parent": parent,
        "inputs": inputs or {},
        "fields": fields or {},
        "shadow": shadow,
        "topLevel": top,
    }
    if top:
        b["x"], b["y"] = 60, 60
    return b


def num(value):
    return [1, [4, str(value)]]


BLOCKS = {
    # --- start ---
    "b01": block("event_whenflagclicked", nxt="b02", top=True),
    "b02": block("pen_clear", nxt="b03", parent="b01"),
    "b03": block("looks_hide", nxt="b04", parent="b02"),
    "b04": block("pen_penUp", nxt="b05", parent="b03"),
    "b05": block("pen_setPenSizeTo", nxt="b06", parent="b04",
                 inputs={"SIZE": num(2)}),
    "b06": block("pen_setPenColorToColor", nxt="b07", parent="b05",
                 inputs={"COLOR": [1, [9, "#a03c3c"]]}),
    "b07": block("pen_setPenColorParamTo", nxt="b08", parent="b06",
                 inputs={"COLOR_PARAM": [1, "m01"], "VALUE": num(0)}),
    "m01": block("pen_menu_colorParam", parent="b07", shadow=True,
                 fields={"colorParam": ["transparency", None]}),
    "b08": block("sensing_askandwait", nxt="b09", parent="b07",
                 inputs={"QUESTION": [1, [10, "Ile figur mam narysować?"]]}),
    "b09": block("data_setvariableto", nxt="b11", parent="b08",
                 inputs={"VALUE": [3, "b10", [10, ""]]},
                 fields={"VARIABLE": list(VAR_FIGURY)}),
    "b10": block("sensing_answer", parent="b09"),
    "b11": block("data_setvariableto", nxt="b12", parent="b09",
                 inputs={"VALUE": [1, [10, "0"]]},
                 fields={"VARIABLE": list(VAR_KIERUNEK)}),

    # --- petla glowna: jedna iteracja = jedna figura ---
    "b12": block("control_repeat", parent="b11",
                 inputs={"TIMES": var_input(VAR_FIGURY, (6, "10")),
                         "SUBSTACK": [2, "c01"]}),
    "c01": block("motion_gotoxy", nxt="c02", parent="b12",
                 inputs={"X": num(0), "Y": num(0)}),
    "c02": block("motion_pointindirection", nxt="c03", parent="c01",
                 inputs={"DIRECTION": var_input(VAR_KIERUNEK, (8, "90"))}),
    "c03": block("pen_penDown", nxt="c04", parent="c02"),

    # duzy luk 180 stopni (kopula)
    "c04": block("control_repeat", nxt="c05", parent="c03",
                 inputs={"TIMES": [1, [6, "36"]], "SUBSTACK": [2, "d01"]}),
    "d01": block("motion_movesteps", nxt="d02", parent="c04",
                 inputs={"STEPS": num(6)}),
    "d02": block("motion_turnright", parent="d01",
                 inputs={"DEGREES": num(5)}),

    # zawrot i pierwszy maly luk (prawy garb, do dziobka na srodku)
    "c05": block("motion_turnright", nxt="c06", parent="c04",
                 inputs={"DEGREES": num(180)}),
    "c06": block("control_repeat", nxt="c07", parent="c05",
                 inputs={"TIMES": [1, [6, "36"]], "SUBSTACK": [2, "d03"]}),
    "d03": block("motion_movesteps", nxt="d04", parent="c06",
                 inputs={"STEPS": num(3)}),
    "d04": block("motion_turnleft", parent="d03",
                 inputs={"DEGREES": num(5)}),

    # zawrot w dziobku i drugi maly luk (lewy garb)
    "c07": block("motion_turnright", nxt="c08", parent="c06",
                 inputs={"DEGREES": num(180)}),
    "c08": block("control_repeat", nxt="c09", parent="c07",
                 inputs={"TIMES": [1, [6, "36"]], "SUBSTACK": [2, "d05"]}),
    "d05": block("motion_movesteps", nxt="d06", parent="c08",
                 inputs={"STEPS": num(3)}),
    "d06": block("motion_turnleft", parent="d05",
                 inputs={"DEGREES": num(5)}),

    # --- po narysowaniu figury: obrot i wieksza przezroczystosc ---
    "c09": block("pen_penUp", nxt="c10", parent="c08"),
    "c10": block("data_changevariableby", nxt="c11", parent="c09",
                 inputs={"VALUE": [3, "o01", [4, "10"]]},
                 fields={"VARIABLE": list(VAR_KIERUNEK)}),
    "o01": block("operator_divide", parent="c10",
                 inputs={"NUM1": num(360),
                         "NUM2": var_input(VAR_FIGURY, (4, ""))}),
    "c11": block("pen_changePenColorParamBy", parent="c10",
                 inputs={"COLOR_PARAM": [1, "m02"],
                         "VALUE": [3, "o02", [4, "10"]]}),
    "m02": block("pen_menu_colorParam", parent="c11", shadow=True,
                 fields={"colorParam": ["transparency", None]}),
    "o02": block("operator_divide", parent="c11",
                 inputs={"NUM1": num(75),
                         "NUM2": var_input(VAR_FIGURY, (4, ""))}),
}

# --- kostiumy (minimalne SVG) -------------------------------------------------
BACKDROP_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360">'
    '<rect width="480" height="360" fill="#ffffff"/></svg>'
).encode()

SPRITE_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16">'
    '<circle cx="8" cy="8" r="7" fill="#5b3bd6"/></svg>'
).encode()


def asset(data, name, center):
    md5 = hashlib.md5(data).hexdigest()
    costume = {
        "assetId": md5,
        "name": name,
        "md5ext": md5 + ".svg",
        "dataFormat": "svg",
        "rotationCenterX": center[0],
        "rotationCenterY": center[1],
    }
    return costume, md5 + ".svg", data


backdrop_costume, backdrop_file, _ = asset(BACKDROP_SVG, "tlo", (240, 180))
sprite_costume, sprite_file, _ = asset(SPRITE_SVG, "kropka", (8, 8))

PROJECT = {
    "targets": [
        {
            "isStage": True,
            "name": "Stage",
            "variables": {
                VAR_FIGURY[1]: [VAR_FIGURY[0], 0],
                VAR_KIERUNEK[1]: [VAR_KIERUNEK[0], 0],
            },
            "lists": {},
            "broadcasts": {},
            "blocks": {},
            "comments": {},
            "currentCostume": 0,
            "costumes": [backdrop_costume],
            "sounds": [],
            "volume": 100,
            "layerOrder": 0,
            "tempo": 60,
            "videoTransparency": 50,
            "videoState": "off",
            "textToSpeechLanguage": None,
        },
        {
            "isStage": False,
            "name": "Rysownik",
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "blocks": BLOCKS,
            "comments": {},
            "currentCostume": 0,
            "costumes": [sprite_costume],
            "sounds": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "x": 0,
            "y": 0,
            "size": 100,
            "direction": 90,
            "draggable": False,
            "rotationStyle": "all around",
        },
    ],
    "monitors": [],
    "extensions": ["pen"],
    "meta": {
        "semver": "3.0.0",
        "vm": "2.3.0",
        "agent": "",
    },
}

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("project.json", json.dumps(PROJECT, ensure_ascii=False))
    zf.writestr(backdrop_file, BACKDROP_SVG)
    zf.writestr(sprite_file, SPRITE_SVG)

print(f"Zapisano: {OUT}")
