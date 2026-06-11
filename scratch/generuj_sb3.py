#!/usr/bin/env python3
"""Generuje projekt Scratcha (.sb3) rysujacy wirujace spirale.

Program w Scratchu:
  - po kliknieciu zielonej flagi pyta "Ile figur mam narysowac?",
  - rysuje pisakiem tyle spiralnych ramion, ile podal uzytkownik,
  - ramiona sa rozlozone symetrycznie co (360 / liczba figur) stopni,
  - kazde kolejne ramie jest bardziej przezroczyste (pen transparency).
"""
import hashlib
import json
import zipfile
from pathlib import Path

OUT = Path(__file__).parent / "wirujace_spirale.sb3"

# --- identyfikatory zmiennych -------------------------------------------------
VAR_FIGURY = ("figury", "var_figury")
VAR_KIERUNEK = ("kierunek", "var_kierunek")
VAR_KROK = ("krok", "var_krok")


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


BLOCKS = {
    # --- start ---
    "b01": block("event_whenflagclicked", nxt="b02", top=True),
    "b02": block("pen_clear", nxt="b03", parent="b01"),
    "b03": block("looks_hide", nxt="b04", parent="b02"),
    "b04": block("pen_penUp", nxt="b05", parent="b03"),
    "b05": block("pen_setPenSizeTo", nxt="b06", parent="b04",
                 inputs={"SIZE": [1, [4, "2"]]}),
    "b06": block("pen_setPenColorToColor", nxt="b07", parent="b05",
                 inputs={"COLOR": [1, [9, "#a03c3c"]]}),
    "b07": block("pen_setPenColorParamTo", nxt="b08", parent="b06",
                 inputs={"COLOR_PARAM": [1, "m01"], "VALUE": [1, [4, "0"]]}),
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
                         "SUBSTACK": [2, "b14"]}),
    "b14": block("motion_gotoxy", nxt="b15", parent="b12",
                 inputs={"X": [1, [4, "0"]], "Y": [1, [4, "0"]]}),
    "b15": block("motion_pointindirection", nxt="b16", parent="b14",
                 inputs={"DIRECTION": var_input(VAR_KIERUNEK, (8, "90"))}),
    "b16": block("data_setvariableto", nxt="b17", parent="b15",
                 inputs={"VALUE": [1, [10, "1"]]},
                 fields={"VARIABLE": list(VAR_KROK)}),
    "b17": block("pen_penDown", nxt="b18", parent="b16"),

    # --- petla wewnetrzna: rysowanie jednej spirali ---
    "b18": block("control_repeat", nxt="b22", parent="b17",
                 inputs={"TIMES": [1, [6, "45"]], "SUBSTACK": [2, "b19"]}),
    "b19": block("motion_movesteps", nxt="b20", parent="b18",
                 inputs={"STEPS": var_input(VAR_KROK)}),
    "b20": block("motion_turnright", nxt="b21", parent="b19",
                 inputs={"DEGREES": [1, [4, "8"]]}),
    "b21": block("data_changevariableby", parent="b20",
                 inputs={"VALUE": [1, [4, "0.4"]]},
                 fields={"VARIABLE": list(VAR_KROK)}),

    # --- po narysowaniu figury: obrot i wieksza przezroczystosc ---
    "b22": block("pen_penUp", nxt="b23", parent="b18"),
    "b23": block("data_changevariableby", nxt="b25", parent="b22",
                 inputs={"VALUE": [3, "b24", [4, "10"]]},
                 fields={"VARIABLE": list(VAR_KIERUNEK)}),
    "b24": block("operator_divide", parent="b23",
                 inputs={"NUM1": [1, [4, "360"]],
                         "NUM2": var_input(VAR_FIGURY, (4, ""))}),
    "b25": block("pen_changePenColorParamBy", parent="b23",
                 inputs={"COLOR_PARAM": [1, "m02"],
                         "VALUE": [3, "b26", [4, "10"]]}),
    "m02": block("pen_menu_colorParam", parent="b25", shadow=True,
                 fields={"colorParam": ["transparency", None]}),
    "b26": block("operator_divide", parent="b25",
                 inputs={"NUM1": [1, [4, "75"]],
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
                VAR_KROK[1]: [VAR_KROK[0], 0],
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
