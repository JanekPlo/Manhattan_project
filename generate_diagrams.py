#!/usr/bin/env python3
"""Generuje diagramy (PNG) do dokumentu Projektu systemu SmartDorm:
  - diagrams/architektura-logiczna.png  (Załącznik A)
  - diagrams/schemat-bazy-danych.png    (Załącznik B)

Użycie:
    pip install matplotlib
    python generate_diagrams.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT_DIR = "diagrams"

# --- paleta ---
C_CLIENT = "#dbeafe"   # jasny niebieski
C_EDGE_L = "#1e3a5f"
C_APP = "#dcfce7"      # jasny zielony
C_APP_E = "#14532d"
C_DATA = "#fef3c7"     # jasny żółty
C_DATA_E = "#78350f"
C_EXT = "#fce7f3"      # jasny różowy
C_EXT_E = "#831843"
C_ASYNC = "#ede9fe"    # jasny fiolet
C_ASYNC_E = "#4c1d95"
C_GRAY = "#f1f5f9"
C_GRAY_E = "#334155"


def box(ax, x, y, w, h, text, fc, ec, fs=10, bold=False, sub=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=1.4))
    weight = "bold" if bold else "normal"
    if sub:
        ax.text(x + w / 2, y + h * 0.62, text, ha="center", va="center",
                fontsize=fs, fontweight=weight, color=ec)
        ax.text(x + w / 2, y + h * 0.30, sub, ha="center", va="center",
                fontsize=fs - 2.2, color=ec, style="italic")
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, fontweight=weight, color=ec, wrap=True)


def arrow(ax, x1, y1, x2, y2, color="#475569", style="-|>", lw=1.4, ls="-", label=None, lfs=7.5, loff=(0, 0)):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=13, color=color, lw=lw, linestyle=ls,
                                 shrinkA=2, shrinkB=2))
    if label:
        ax.text((x1 + x2) / 2 + loff[0], (y1 + y2) / 2 + loff[1], label,
                ha="center", va="center", fontsize=lfs, color=color,
                bbox=dict(fc="white", ec="none", pad=1))


def zone(ax, x, y, w, h, title, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc="none", ec=ec, lw=1.1, linestyle=(0, (4, 3))))
    ax.text(x + 0.12, y + h - 0.06, title, ha="left", va="top",
            fontsize=9.5, fontweight="bold", color=ec)


def architektura():
    fig, ax = plt.subplots(figsize=(11.7, 12.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 13)
    ax.axis("off")
    ax.set_title("SmartDorm — diagram architektury logicznej",
                 fontsize=15, fontweight="bold", pad=14)

    # --- warstwa klienta ---
    zone(ax, 0.3, 11.1, 11.4, 1.55, "WARSTWA KLIENTA", C_EDGE_L)
    box(ax, 1.0, 11.3, 4.4, 1.0, "Aplikacja WWW (SPA)", C_CLIENT, C_EDGE_L,
        bold=True, sub="React 18.3 + TypeScript, przeglądarka")
    box(ax, 6.6, 11.3, 4.4, 1.0, "Aplikacja mobilna (PWA)", C_CLIENT, C_EDGE_L,
        bold=True, sub="ten sam frontend, tryb offline-cache")

    # --- warstwa dostępu ---
    zone(ax, 0.3, 8.9, 11.4, 1.75, "WARSTWA DOSTĘPU", C_GRAY_E)
    box(ax, 1.0, 9.15, 4.4, 1.0, "Nginx Ingress", C_GRAY, C_GRAY_E,
        bold=True, sub="TLS 1.3, rate-limiting, load-balancing")
    box(ax, 6.6, 9.15, 4.4, 1.0, "Keycloak 25 (OIDC)", C_GRAY, C_GRAY_E,
        bold=True, sub="OAuth2 / JWT, SSO, 2FA")

    arrow(ax, 3.2, 11.3, 3.2, 10.15, label="HTTPS / REST + JSON")
    arrow(ax, 8.8, 11.3, 8.8, 10.15, label="HTTPS / OIDC (logowanie)")
    arrow(ax, 5.4, 9.65, 6.6, 9.65, label="weryfikacja JWT (JWKS)")

    # --- aplikacja: modularny monolit ---
    zone(ax, 0.3, 5.15, 8.6, 3.45, "APLIKACJA SMARTDORM — MODULARNY MONOLIT (Spring Boot 3.3, Java 21)", C_APP_E)
    mods = [
        ("Moduł pokoi\ni budynków", 0.7, 7.15), ("Moduł\nkwaterowania", 2.75, 7.15),
        ("Moduł helpdesk\n(usterki)", 4.8, 7.15), ("Moduł\npłatności", 6.85, 7.15),
        ("Moduł\npowiadomień", 0.7, 5.5), ("Moduł\nużytkowników", 2.75, 5.5),
        ("Moduł raportów\ni administracji", 4.8, 5.5), ("API REST\n(/api/v1)", 6.85, 5.5),
    ]
    for name, x, y in mods:
        box(ax, x, y, 1.85, 1.15, name, C_APP, C_APP_E, fs=9, bold=True)

    arrow(ax, 3.2, 9.15, 3.2, 8.6, label="ruch po autoryzacji")

    # --- workery asynchroniczne ---
    zone(ax, 9.3, 5.15, 2.4, 3.45, "ASYNC", C_ASYNC_E)
    box(ax, 9.5, 7.15, 2.0, 1.15, "RabbitMQ 3.13\n(broker zdarzeń)", C_ASYNC, C_ASYNC_E, fs=9, bold=True)
    box(ax, 9.5, 5.5, 2.0, 1.15, "Worker\npowiadomień\ni rozliczeń", C_ASYNC, C_ASYNC_E, fs=9, bold=True)
    arrow(ax, 8.9, 7.7, 9.5, 7.7, label="zdarzenia", loff=(0, 0.22))
    arrow(ax, 10.5, 7.15, 10.5, 6.65, label="konsumpcja")

    # --- warstwa danych ---
    zone(ax, 0.3, 2.8, 11.4, 2.0, "WARSTWA DANYCH", C_DATA_E)
    box(ax, 0.8, 3.05, 3.2, 1.3, "PostgreSQL 16", C_DATA, C_DATA_E, bold=True,
        sub="dane relacyjne,\npgcrypto (PESEL)")
    box(ax, 4.4, 3.05, 3.2, 1.3, "Redis 7.2", C_DATA, C_DATA_E, bold=True,
        sub="cache dostępności pokoi,\nsesje, rate-limit")
    box(ax, 8.0, 3.05, 3.2, 1.3, "MinIO (S3 API)", C_DATA, C_DATA_E, bold=True,
        sub="załączniki zgłoszeń\n(zdjęcia usterek)")
    arrow(ax, 2.4, 5.15, 2.4, 4.35, label="JDBC / JPA")
    arrow(ax, 6.0, 5.15, 6.0, 4.35, label="cache")
    arrow(ax, 9.6, 5.15, 9.6, 4.35, label="S3 API")

    # --- integracje zewnętrzne ---
    zone(ax, 0.3, 0.35, 11.4, 1.95, "INTEGRACJE ZEWNĘTRZNE", C_EXT_E)
    exts = [("Bramka płatności\nPayU (REST + webhook)", 0.8),
            ("E-mail\nSMTP / SendGrid", 3.65),
            ("Push / SMS\nFirebase FCM", 6.25),
            ("System uczelni\nUSOS (import studentów)", 8.95)]
    for name, x in exts:
        box(ax, x, 0.6, 2.5, 1.25, name, C_EXT, C_EXT_E, fs=9, bold=True)
    arrow(ax, 2.05, 2.8, 2.05, 1.85, ls="--")
    arrow(ax, 5.02, 2.8, 5.02, 1.85, ls="--")
    arrow(ax, 7.62, 2.8, 7.62, 1.85, ls="--")
    arrow(ax, 10.12, 2.8, 10.12, 1.85, ls="--")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "architektura-logiczna.png"), dpi=170)
    plt.close(fig)


def entity(ax, x, y, w, title, cols, hh=0.42, rh=0.335):
    """Rysuje encję ERD; zwraca (x, y_top, w, h)."""
    h = hh + rh * len(cols)
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="square,pad=0",
                                fc="white", ec="#1e3a5f", lw=1.5))
    ax.add_patch(FancyBboxPatch((x, y - hh), w, hh, boxstyle="square,pad=0",
                                fc="#1e3a5f", ec="#1e3a5f", lw=1.5))
    ax.text(x + w / 2, y - hh / 2, title, ha="center", va="center",
            fontsize=10, fontweight="bold", color="white")
    for i, col in enumerate(cols):
        cy = y - hh - rh * (i + 0.5)
        weight = "bold" if col.startswith(("PK", "FK")) else "normal"
        ax.text(x + 0.12, cy, col, ha="left", va="center", fontsize=8.3,
                fontweight=weight, color="#0f172a", family="DejaVu Sans")
        if i:
            ax.plot([x, x + w], [y - hh - rh * i] * 2, color="#cbd5e1", lw=0.6)
    return (x, y, w, h)


def rel(ax, points, label, label_at=None):
    """Rysuje relację jako łamaną przez listę punktów [(x, y), ...]."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color="#64748b", lw=1.2, solid_capstyle="round", zorder=1)
    if label_at is None:
        mid = len(points) // 2
        label_at = ((points[mid - 1][0] + points[mid][0]) / 2,
                    (points[mid - 1][1] + points[mid][1]) / 2)
    ax.text(label_at[0], label_at[1], label, ha="center", va="center",
            fontsize=8, color="#334155", fontweight="bold", zorder=3,
            bbox=dict(fc="white", ec="#94a3b8", pad=1.5))


def schemat_bazy():
    fig, ax = plt.subplots(figsize=(12.4, 14.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 15)
    ax.axis("off")
    ax.set_title("SmartDorm — schemat bazy danych (PostgreSQL 16)",
                 fontsize=15, fontweight="bold", pad=14)

    entity(ax, 0.5, 14.2, 3.4, "uzytkownicy", [
        "PK  id  UUID", "imie  VARCHAR(80)", "nazwisko  VARCHAR(120)",
        "email  VARCHAR(255)  UQ", "pesel_enc  BYTEA (AES-256)",
        "nr_dowodu_enc  BYTEA (AES-256)", "rola  ENUM(student, admin,",
        "        technik, ksiegowosc)", "aktywny  BOOLEAN", "utworzono  TIMESTAMPTZ"])

    entity(ax, 5.0, 14.2, 3.2, "budynki", [
        "PK  id  UUID", "nazwa  VARCHAR(120)", "adres  VARCHAR(255)"])
    entity(ax, 5.0, 12.2, 3.2, "pietra", [
        "PK  id  UUID", "FK  budynek_id", "numer  SMALLINT"])
    entity(ax, 5.0, 10.35, 3.2, "pokoje", [
        "PK  id  UUID", "FK  pietro_id", "numer  VARCHAR(10)",
        "liczba_miejsc  SMALLINT", "status  ENUM(dostepny,",
        "        pelny, wylaczony)"])

    entity(ax, 9.3, 14.2, 3.3, "wnioski_kwaterunkowe", [
        "PK  id  UUID", "FK  student_id", "FK  pokoj_id",
        "status  ENUM(zlozony, przyjety,", "        odrzucony, anulowany)",
        "data_zlozenia  TIMESTAMPTZ", "wersja  INTEGER (opt. lock)"])

    entity(ax, 9.3, 10.6, 3.3, "zakwaterowania", [
        "PK  id  UUID", "FK  student_id", "FK  pokoj_id", "FK  wniosek_id",
        "data_od  DATE", "data_do  DATE", "status  ENUM(aktywne,",
        "        zakonczone)"])

    entity(ax, 0.5, 9.6, 3.4, "zgloszenia", [
        "PK  id  UUID", "FK  mieszkaniec_id", "FK  pokoj_id",
        "FK  technik_id  NULL", "tytul  VARCHAR(200)", "opis  TEXT",
        "priorytet  ENUM(niski, sredni,", "        wysoki, krytyczny)",
        "status  ENUM(nowe, w_realizacji,", "        naprawione, zamkniete)",
        "utworzono  TIMESTAMPTZ"])

    entity(ax, 0.5, 4.4, 3.4, "zalaczniki_zgloszen", [
        "PK  id  UUID", "FK  zgloszenie_id", "klucz_s3  VARCHAR(512)",
        "mime  VARCHAR(100)", "rozmiar_b  BIGINT"])

    entity(ax, 5.0, 7.6, 3.2, "naliczenia", [
        "PK  id  UUID", "FK  zakwaterowanie_id", "okres  DATE (rok-miesiac)",
        "kwota_czynsz  NUMERIC(10,2)", "kwota_media  NUMERIC(10,2)",
        "termin_platnosci  DATE", "status  ENUM(oczekujace,",
        "        oplacone, zalegle)", "UQ (zakwaterowanie_id, okres)"])

    entity(ax, 9.3, 7.0, 3.3, "wplaty", [
        "PK  id  UUID", "FK  naliczenie_id", "kwota  NUMERIC(10,2)",
        "data_wplaty  TIMESTAMPTZ", "zrodlo  ENUM(payu, przelew)",
        "id_transakcji  VARCHAR(64) UQ", "status  ENUM(zainicjowana,",
        "        zaksiegowana, zwrocona)"])

    entity(ax, 5.0, 3.9, 3.2, "powiadomienia", [
        "PK  id  UUID", "FK  uzytkownik_id", "typ  ENUM(platnosc, usterka,",
        "        kwaterunek, systemowe)", "kanal  ENUM(email, push, sms)",
        "tresc  TEXT", "wyslano  TIMESTAMPTZ NULL", "przeczytano  BOOLEAN"])

    entity(ax, 9.3, 3.2, 3.3, "zdarzenia_outbox", [
        "PK  id  BIGSERIAL", "typ_zdarzenia  VARCHAR(100)",
        "payload  JSONB", "utworzono  TIMESTAMPTZ",
        "opublikowano  TIMESTAMPTZ NULL"])

    # relacje (łamane prowadzone korytarzami między kolumnami encji)
    rel(ax, [(6.6, 12.77), (6.6, 12.2)], "1 : N")             # budynki -> pietra
    rel(ax, [(6.6, 10.77), (6.6, 10.35)], "1 : N")            # pietra -> pokoje
    rel(ax, [(8.2, 10.05), (8.75, 10.05), (8.75, 12.0), (9.3, 12.0)],
        "1 : N", label_at=(8.75, 11.1))                       # pokoje -> wnioski
    rel(ax, [(8.2, 8.6), (9.3, 8.6)], "1 : N")                # pokoje -> zakwaterowania
    rel(ax, [(2.2, 14.2), (2.2, 14.62), (10.9, 14.62), (10.9, 14.2)],
        "1 : N (student)", label_at=(6.55, 14.62))            # uzytkownicy -> wnioski
    rel(ax, [(10.9, 11.43), (10.9, 10.6)], "1 : 1")           # wnioski -> zakwaterowania
    rel(ax, [(2.2, 10.42), (2.2, 9.6)], "1 : N")              # uzytkownicy -> zgloszenia
    rel(ax, [(2.2, 5.49), (2.2, 4.4)], "1 : N")               # zgloszenia -> zalaczniki
    rel(ax, [(9.3, 7.75), (8.75, 7.75), (8.75, 7.2), (8.2, 7.2)],
        "1 : N", label_at=(8.75, 7.48))                       # zakwaterowania -> naliczenia
    rel(ax, [(8.2, 5.8), (9.3, 5.8)], "1 : N")                # naliczenia -> wplaty
    rel(ax, [(3.9, 10.55), (4.45, 10.55), (4.45, 3.0), (5.0, 3.0)],
        "1 : N", label_at=(4.45, 6.6))                        # uzytkownicy -> powiadomienia

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "schemat-bazy-danych.png"), dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    architektura()
    schemat_bazy()
    print("Zapisano diagramy w katalogu:", OUT_DIR)
