#!/usr/bin/env python3
"""Buduje plik Scratch (.sb3): symetryczny kwiat z płatków (dwa łuki) + własny blok.

Program w Scratchu (rozszerzenie Pióro):
  - po starcie pyta: "Ile figur narysować?"
  - rysuje podaną liczbę figur (płatków = dwa połączone łuki) rozłożonych
    symetrycznie wokół środka sceny
  - po każdej figurze duszek wraca na środek, obraca się o 360/liczba i rysuje
    kolejną figurę
  - każda kolejna figura jest odrobinę bardziej przezroczysta od poprzedniej
  - figura rysowana jest we własnym bloku "narysuj figurę"
"""
import hashlib
import json
import zipfile

VID_COUNT = "var-liczba"

# Parametry płatka
KROK = "8"        # długość kroku łuku
SKRET = 7         # obrót po kroku (stopnie)
KROKI = 20        # liczba kroków jednego łuku
WAIT = "0.01"     # krótka pauza -> wolniejsze, widoczne rysowanie
TIP = str(180 - KROKI * SKRET)   # czubek płatka: 180 - 140 = 40 stopni
SKRET = str(SKRET)
KROKI = str(KROKI)

PROC = "narysuj figurę"   # nazwa własnego bloku


def var_in(name, vid, default="0"):
    return [3, [12, name, vid], [4, default]]


blocks = {}


def add(bid, opcode, *, next=None, parent=None, inputs=None, fields=None,
        shadow=False, top=False, x=None, y=None, mutation=None):
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
    if mutation is not None:
        b["mutation"] = mutation
    blocks[bid] = b


# ===========================================================================
# 1) SKRYPT GŁÓWNY (po kliknięciu zielonej flagi)
# ===========================================================================
add("flag", "event_whenflagclicked", next="ask", top=True, x=40, y=40)

add("ask", "sensing_askandwait", parent="flag", next="setcount",
    inputs={"QUESTION": [1, [10, "Ile figur narysować?"]]})

add("answer", "sensing_answer", parent="setcount")
add("setcount", "data_setvariableto", parent="ask", next="clear",
    inputs={"VALUE": [3, "answer", [10, "0"]]},
    fields={"VARIABLE": ["liczba figur", VID_COUNT]})

add("clear", "pen_clear", parent="setcount", next="goto")

add("goto", "motion_gotoxy", parent="clear", next="point",
    inputs={"X": [1, [4, "0"]], "Y": [1, [4, "0"]]})
add("point", "motion_pointindirection", parent="goto", next="setcolor",
    inputs={"DIRECTION": [1, [8, "90"]]})

add("setcolor", "pen_setPenColorToColor", parent="point", next="settrans",
    inputs={"COLOR": [1, [9, "#cc0033"]]})

# przezroczystość pióra <- 0
add("paramS", "pen_menu_colorParam", parent="settrans", shadow=True,
    fields={"colorParam": ["transparency", None]})
add("settrans", "pen_setPenColorParamTo", parent="setcolor", next="repouter",
    inputs={"COLOR_PARAM": [1, "paramS"], "VALUE": [1, [4, "0"]]})

# powtórz (liczba figur) razy
add("repouter", "control_repeat", parent="settrans",
    inputs={"TIMES": var_in("liczba figur", VID_COUNT, "8"),
            "SUBSTACK": [2, "call"]})

# --- ciało pętli ---
# wywołaj własny blok "narysuj figurę"
add("call", "procedures_call", parent="repouter", next="goto2",
    inputs={}, mutation={
        "tagName": "mutation", "children": [],
        "proccode": PROC, "argumentids": "[]", "warp": "false",
    })
# wróć na środek
add("goto2", "motion_gotoxy", parent="call", next="turn",
    inputs={"X": [1, [4, "0"]], "Y": [1, [4, "0"]]})
# obróć o 360 / liczba figur
add("divrot", "operator_divide", parent="turn",
    inputs={"NUM1": [1, [4, "360"]], "NUM2": var_in("liczba figur", VID_COUNT, "1")})
add("turn", "motion_turnright", parent="goto2", next="changetrans",
    inputs={"DEGREES": [3, "divrot", [4, "0"]]})
# zwiększ przezroczystość o 80 / liczba figur
add("paramC", "pen_menu_colorParam", parent="changetrans", shadow=True,
    fields={"colorParam": ["transparency", None]})
add("divtr", "operator_divide", parent="changetrans",
    inputs={"NUM1": [1, [4, "80"]], "NUM2": var_in("liczba figur", VID_COUNT, "1")})
add("changetrans", "pen_changePenColorParamBy", parent="turn",
    inputs={"COLOR_PARAM": [1, "paramC"], "VALUE": [3, "divtr", [4, "0"]]})

# ===========================================================================
# 2) WŁASNY BLOK "narysuj figurę" (definicja)
# ===========================================================================
add("def", "procedures_definition", top=True, x=40, y=320, next="pendown",
    inputs={"custom_block": [1, "proto"]})
add("proto", "procedures_prototype", parent="def", shadow=True,
    inputs={}, mutation={
        "tagName": "mutation", "children": [],
        "proccode": PROC, "argumentids": "[]", "argumentnames": "[]",
        "argumentdefaults": "[]", "warp": "false",
    })

add("pendown", "pen_penDown", parent="def", next="a1rep")

# łuk 1 (na zewnątrz)
add("a1rep", "control_repeat", parent="pendown", next="tip1",
    inputs={"TIMES": [1, [6, KROKI]], "SUBSTACK": [2, "a1mv"]})
add("a1mv", "motion_movesteps", parent="a1rep", next="a1tn",
    inputs={"STEPS": [1, [4, KROK]]})
add("a1tn", "motion_turnright", parent="a1mv", next="a1wt",
    inputs={"DEGREES": [1, [4, SKRET]]})
add("a1wt", "control_wait", parent="a1tn",
    inputs={"DURATION": [1, [5, WAIT]]})

# czubek
add("tip1", "motion_turnright", parent="a1rep", next="a2rep",
    inputs={"DEGREES": [1, [4, TIP]]})

# łuk 2 (powrót w stronę środka)
add("a2rep", "control_repeat", parent="tip1", next="tip2",
    inputs={"TIMES": [1, [6, KROKI]], "SUBSTACK": [2, "a2mv"]})
add("a2mv", "motion_movesteps", parent="a2rep", next="a2tn",
    inputs={"STEPS": [1, [4, KROK]]})
add("a2tn", "motion_turnright", parent="a2mv", next="a2wt",
    inputs={"DEGREES": [1, [4, SKRET]]})
add("a2wt", "control_wait", parent="a2tn",
    inputs={"DURATION": [1, [5, WAIT]]})

# czubek domykający + podnieś pisak
add("tip2", "motion_turnright", parent="a2rep", next="penup",
    inputs={"DEGREES": [1, [4, TIP]]})
add("penup", "pen_penUp", parent="tip2")

# ===========================================================================
# Kostiumy / tła
# ===========================================================================
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
    "isStage": True, "name": "Stage",
    "variables": {VID_COUNT: ["liczba figur", 0]},
    "lists": {}, "broadcasts": {}, "blocks": {}, "comments": {},
    "currentCostume": 0,
    "costumes": [{"assetId": bg_md5, "name": "tło", "md5ext": bg_md5 + ".svg",
                  "dataFormat": "svg", "rotationCenterX": 240, "rotationCenterY": 180}],
    "sounds": [], "volume": 100, "layerOrder": 0, "tempo": 60,
    "videoTransparency": 50, "videoState": "on", "textToSpeechLanguage": None,
}
sprite = {
    "isStage": False, "name": "Pisak",
    "variables": {}, "lists": {}, "broadcasts": {},
    "blocks": blocks, "comments": {}, "currentCostume": 0,
    "costumes": [{"assetId": dot_md5, "name": "kropka", "md5ext": dot_md5 + ".svg",
                  "dataFormat": "svg", "rotationCenterX": 8, "rotationCenterY": 8}],
    "sounds": [], "volume": 100, "layerOrder": 1, "visible": True,
    "x": 0, "y": 0, "size": 100, "direction": 90,
    "draggable": False, "rotationStyle": "all around",
}
project = {
    "targets": [stage, sprite], "monitors": [], "extensions": ["pen"],
    "meta": {"semver": "3.0.0", "vm": "2.3.0", "agent": ""},
}

out = "figury.sb3"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("project.json", json.dumps(project, ensure_ascii=False))
    z.writestr(dot_md5 + ".svg", DOT_SVG)
    z.writestr(bg_md5 + ".svg", BG_SVG)
print("Zapisano", out, "| TIP =", TIP)
