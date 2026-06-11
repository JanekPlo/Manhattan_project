#!/usr/bin/env python3
"""Buduje plik Scratch (.sb3) z programem rysującym FALĘ z półokręgów.

Program w Scratchu:
  - po starcie pyta: "Ile półokręgów narysować?"
  - rysuje pionową falę = łańcuch półokręgów `)` wybrzuszonych w tę samą
    stronę, jeden pod drugim (z dziobkiem/cuspem w punktach łączenia) -
    dokładnie jak na rysunku
  - rysuje się powoli (krótkie "czekaj"), więc widać, jak fala powstaje

Jak powstaje jeden półokrąg:
  pisak jedzie w prawo i zatacza 180 stopni (move + turn right) -> wybrzuszenie
  w prawo, schodząc o średnicę w dół; potem obrót o 180 stopni (dziobek) i
  kolejny taki sam półokrąg poniżej.
"""
import hashlib
import json
import zipfile

VID_COUNT = "var-liczba"

# Parametry fali i tempa rysowania
KROK = "5"            # długość kroku
KROKI_POL = "18"      # ile kroków na jeden półokrąg
SKRET = "10"          # obrót po kroku (18 * 10 = 180 stopni = półokrąg)
CUSP = "180"          # obrót w punkcie łączenia (dziobek), by następny też w prawo
START_Y = "150"       # start u góry sceny, fala schodzi w dół
WAIT_W = "0.01"       # czekaj wewnątrz półokręgu (większe = wolniej)
WAIT_Z = "0.05"       # czekaj w punkcie łączenia


def var_in(name, vid, default="0"):
    """Zmienna użyta jako wartość wejścia (obscured shadow)."""
    return [3, [12, name, vid], [4, default]]


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
    inputs={"QUESTION": [1, [10, "Ile półokręgów narysować?"]]})

add("clear", "pen_clear", parent="ask", next="setcolor")

add("setcolor", "pen_setPenColorToColor", parent="clear", next="setcount",
    inputs={"COLOR": [1, [9, "#cc0033"]]})

# liczba <- odpowiedź
add("answer", "sensing_answer", parent="setcount")
add("setcount", "data_setvariableto", parent="setcolor", next="goto",
    inputs={"VALUE": [3, "answer", [10, "0"]]},
    fields={"VARIABLE": ["liczba", VID_COUNT]})

# ustaw start u góry i skieruj w prawo (wschód) -> wybrzuszenie pójdzie w prawo
add("goto", "motion_gotoxy", parent="setcount", next="point",
    inputs={"X": [1, [4, "0"]], "Y": [1, [4, START_Y]]})
add("point", "motion_pointindirection", parent="goto", next="pendown",
    inputs={"DIRECTION": [1, [8, "90"]]})

add("pendown", "pen_penDown", parent="point", next="repouter")

# powtórz (liczba) razy -> jeden półokrąg na obrót
add("repouter", "control_repeat", parent="pendown", next="penup",
    inputs={"TIMES": var_in("liczba", VID_COUNT, "5"),
            "SUBSTACK": [2, "arcrep"]})

# jeden półokrąg: powtórz (KROKI_POL) razy [idź krok, obróć, czekaj]
add("arcrep", "control_repeat", parent="repouter", next="cusp",
    inputs={"TIMES": [1, [6, KROKI_POL]], "SUBSTACK": [2, "mv"]})
add("mv", "motion_movesteps", parent="arcrep", next="tn",
    inputs={"STEPS": [1, [4, KROK]]})
add("tn", "motion_turnright", parent="mv", next="wt",
    inputs={"DEGREES": [1, [4, SKRET]]})
add("wt", "control_wait", parent="tn",
    inputs={"DURATION": [1, [5, WAIT_W]]})

# dziobek: obróć o 180 stopni, żeby następny półokrąg też był w prawo
add("cusp", "motion_turnright", parent="arcrep", next="waitz",
    inputs={"DEGREES": [1, [4, CUSP]]})
add("waitz", "control_wait", parent="cusp",
    inputs={"DURATION": [1, [5, WAIT_Z]]})

add("penup", "pen_penUp", parent="repouter")

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
    "variables": {VID_COUNT: ["liczba", 0]},
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

out = "figury.sb3"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("project.json", json.dumps(project, ensure_ascii=False))
    z.writestr(dot_md5 + ".svg", DOT_SVG)
    z.writestr(bg_md5 + ".svg", BG_SVG)

print("Zapisano", out)
