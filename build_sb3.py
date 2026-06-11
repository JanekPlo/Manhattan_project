#!/usr/bin/env python3
"""Buduje plik Scratch (.sb3) z programem rysującym symetryczny wzór spiral.

Program w Scratchu:
  - po starcie pyta: "Ile figur narysować?"
  - rysuje podaną liczbę spiral rozłożonych symetrycznie wokół środka
  - każda kolejna spirala jest odrobinę bardziej przezroczysta od poprzedniej
"""
import hashlib
import json
import zipfile

# ---------------------------------------------------------------------------
# Identyfikatory zmiennych (globalne, trzymane na Scenie / Stage)
# ---------------------------------------------------------------------------
VID_COUNT = "var-liczba"
VID_ANGLE = "var-kat"
VID_R = "var-promien"


def var_in(name, vid, default="0"):
    """Zmienna użyta jako wartość wejścia (obscured shadow)."""
    return [3, [12, name, vid], [4, default]]


# ---------------------------------------------------------------------------
# Bloki sprite'a
# ---------------------------------------------------------------------------
blocks = {}


def add(bid, opcode, *, next=None, parent=None, inputs=None, fields=None,
        shadow=False, top=False, x=None, y=None):
    b = {
        "opcode": opcode,
        "next": next,
        "parent": parent,
        "inputs": inputs or {},
        "fields": fields or {},
        "shadow": shadow,
        "topLevel": top,
    }
    if top:
        b["x"] = x
        b["y"] = y
    blocks[bid] = b


# --- skrypt główny ---------------------------------------------------------
add("flag", "event_whenflagclicked", next="ask", top=True, x=40, y=40)

add("ask", "sensing_askandwait", parent="flag", next="clear",
    inputs={"QUESTION": [1, [10, "Ile figur narysować?"]]})

add("clear", "pen_clear", parent="ask", next="setcolor")

add("setcolor", "pen_setPenColorToColor", parent="clear", next="setcount",
    inputs={"COLOR": [1, [9, "#cc0033"]]})

# liczba <- odpowiedź
add("answer", "sensing_answer", parent="setcount")
add("setcount", "data_setvariableto", parent="setcolor", next="settrans",
    inputs={"VALUE": [3, "answer", [10, "0"]]},
    fields={"VARIABLE": ["liczba", VID_COUNT]})

# przezroczystość pióra <- 0
add("param1", "pen_menu_colorParam", parent="settrans", shadow=True,
    fields={"colorParam": ["transparency", None]})
add("settrans", "pen_setPenColorParamTo", parent="setcount", next="setangle",
    inputs={"COLOR_PARAM": [1, "param1"], "VALUE": [1, [4, "0"]]})

# kąt <- 0
add("setangle", "data_setvariableto", parent="settrans", next="repouter",
    inputs={"VALUE": [1, [4, "0"]]},
    fields={"VARIABLE": ["kat", VID_ANGLE]})

# powtórz (liczba) razy
add("repouter", "control_repeat", parent="setangle",
    inputs={"TIMES": var_in("liczba", VID_COUNT, "5"),
            "SUBSTACK": [2, "goto"]})

# --- ciało pętli zewnętrznej (jedna figura) --------------------------------
add("goto", "motion_gotoxy", parent="repouter", next="point",
    inputs={"X": [1, [4, "0"]], "Y": [1, [4, "0"]]})

# skieruj w stronę (90 + kat)
add("addop", "operator_add", parent="point",
    inputs={"NUM1": [1, [4, "90"]], "NUM2": var_in("kat", VID_ANGLE)})
add("point", "motion_pointindirection", parent="goto", next="setr",
    inputs={"DIRECTION": [3, "addop", [8, "90"]]})

# promień <- 0
add("setr", "data_setvariableto", parent="point", next="pendown",
    inputs={"VALUE": [1, [4, "0"]]},
    fields={"VARIABLE": ["promien", VID_R]})

add("pendown", "pen_penDown", parent="setr", next="repinner")

# powtórz 36 (rysuj spiralę)
add("repinner", "control_repeat", parent="pendown", next="penup",
    inputs={"TIMES": [1, [6, "36"]], "SUBSTACK": [2, "move"]})

add("move", "motion_movesteps", parent="repinner", next="changer",
    inputs={"STEPS": var_in("promien", VID_R, "1")})
add("changer", "data_changevariableby", parent="move", next="turn",
    inputs={"VALUE": [1, [4, "0.7"]]},
    fields={"VARIABLE": ["promien", VID_R]})
add("turn", "motion_turnright", parent="changer",
    inputs={"DEGREES": [1, [4, "20"]]})

add("penup", "pen_penUp", parent="repinner", next="changeangle")

# kat <- kat + 360/liczba (symetryczne rozłożenie)
add("divang", "operator_divide", parent="changeangle",
    inputs={"NUM1": [1, [4, "360"]], "NUM2": var_in("liczba", VID_COUNT, "1")})
add("changeangle", "data_changevariableby", parent="penup", next="changetrans",
    inputs={"VALUE": [3, "divang", [4, "0"]]},
    fields={"VARIABLE": ["kat", VID_ANGLE]})

# zwiększ przezroczystość o 80/liczba (każda kolejna bardziej przezroczysta)
add("param2", "pen_menu_colorParam", parent="changetrans", shadow=True,
    fields={"colorParam": ["transparency", None]})
add("divtr", "operator_divide", parent="changetrans",
    inputs={"NUM1": [1, [4, "80"]], "NUM2": var_in("liczba", VID_COUNT, "1")})
add("changetrans", "pen_changePenColorParamBy", parent="changeangle",
    inputs={"COLOR_PARAM": [1, "param2"], "VALUE": [3, "divtr", [4, "0"]]})

# ---------------------------------------------------------------------------
# Kostiumy / tła (proste pliki SVG)
# ---------------------------------------------------------------------------
DOT_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" '
    'viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" fill="#5b3ec8"/></svg>'
).encode("utf-8")

BG_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" '
    'viewBox="0 0 480 360"><rect width="480" height="360" fill="#ffffff"/></svg>'
).encode("utf-8")

dot_md5 = hashlib.md5(DOT_SVG).hexdigest()
bg_md5 = hashlib.md5(BG_SVG).hexdigest()

stage = {
    "isStage": True,
    "name": "Stage",
    "variables": {
        VID_COUNT: ["liczba", 0],
        VID_ANGLE: ["kat", 0],
        VID_R: ["promien", 0],
    },
    "lists": {},
    "broadcasts": {},
    "blocks": {},
    "comments": {},
    "currentCostume": 0,
    "costumes": [{
        "assetId": bg_md5,
        "name": "tło",
        "md5ext": bg_md5 + ".svg",
        "dataFormat": "svg",
        "rotationCenterX": 240,
        "rotationCenterY": 180,
    }],
    "sounds": [],
    "volume": 100,
    "layerOrder": 0,
    "tempo": 60,
    "videoTransparency": 50,
    "videoState": "on",
    "textToSpeechLanguage": None,
}

sprite = {
    "isStage": False,
    "name": "Pisak",
    "variables": {},
    "lists": {},
    "broadcasts": {},
    "blocks": blocks,
    "comments": {},
    "currentCostume": 0,
    "costumes": [{
        "assetId": dot_md5,
        "name": "kropka",
        "md5ext": dot_md5 + ".svg",
        "dataFormat": "svg",
        "rotationCenterX": 8,
        "rotationCenterY": 8,
    }],
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
}

project = {
    "targets": [stage, sprite],
    "monitors": [],
    "extensions": ["pen"],
    "meta": {"semver": "3.0.0", "vm": "2.3.0", "agent": ""},
}

# ---------------------------------------------------------------------------
# Zapis archiwum .sb3
# ---------------------------------------------------------------------------
out = "spirala.sb3"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("project.json", json.dumps(project, ensure_ascii=False))
    z.writestr(dot_md5 + ".svg", DOT_SVG)
    z.writestr(bg_md5 + ".svg", BG_SVG)

print("Zapisano", out)
print("project.json OK, kostiumy:", dot_md5, bg_md5)
