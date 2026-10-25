"""Pubblica il prossimo carosello da caroselli/queue/ (una cartella per carosello).

Ogni cartella: 1.jpg, 2.jpg, ... (da 2 a 10 immagini JPEG) + caption.txt.
Instagram scarica le immagini da link pubblici: il repo deve essere pubblico.
"""
import os
import shutil
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import publish as p

QUEUE, DONE = p.ROOT / "caroselli" / "queue", p.ROOT / "caroselli" / "published"
STATE = p.ROOT / "state" / "last_carosello.txt"

# Giovedì verso le 11:00 italiane
DAY = 3
SLOT = ((10, 30), (11, 45))


def in_slot() -> bool:
    now = datetime.now(ZoneInfo("Europe/Rome"))
    return now.weekday() == DAY and SLOT[0] <= (now.hour, now.minute) <= SLOT[1]


def published_recently(hours: float = 20) -> bool:
    if not STATE.exists():
        return False
    last = datetime.fromisoformat(STATE.read_text().strip())
    return (datetime.now(ZoneInfo("UTC")) - last).total_seconds() < hours * 3600


def slides(folder: Path) -> list:
    return sorted((f for f in folder.glob("*.jpg")), key=lambda f: int(f.stem) if f.stem.isdigit() else 999)


def wait(container: str, token: str):
    for _ in range(30):
        code = p.call(f"{p.API}/{container}?fields=status_code&access_token={token}").get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            sys.exit(f"Elaborazione fallita: {code}")
        time.sleep(5)


def main():
    scheduled = os.environ.get("GITHUB_EVENT_NAME") == "schedule"
    if scheduled and not in_slot():
        print("Caroselli: fuori giorno o fascia oraria italiana.")
        return
    if scheduled and published_recently():
        print("Caroselli: già pubblicato in questa fascia.")
        return
    QUEUE.mkdir(parents=True, exist_ok=True)
    folders = sorted(f for f in QUEUE.iterdir() if f.is_dir() and (f / "caption.txt").exists()
                     and 2 <= len(slides(f)) <= 10)
    if not folders:
        print("Nessun carosello completo (2-10 immagini JPEG + caption.txt) in coda.")
        return
    folder = folders[0]
    caption = p.build_caption(folder / "caption.jpg")  # legge caption.txt
    print(f"Pubblico carosello: {folder.name} ({len(slides(folder))} immagini)")
    if os.environ.get("DRY_RUN") == "1":
        print(f"[DRY RUN] Caption:\n{caption}")
        return

    ig_id, token = os.environ["IG_USER_ID"], os.environ["IG_ACCESS_TOKEN"]
    base = f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/main/caroselli/queue"

    children = []
    for img in slides(folder):
        url = f"{base}/{urllib.parse.quote(folder.name)}/{img.name}"
        cid = p.call(f"{p.API}/{ig_id}/media", data=urllib.parse.urlencode({
            "image_url": url, "is_carousel_item": "true", "access_token": token}).encode())["id"]
        children.append(cid)
    for cid in children:
        wait(cid, token)

    parent = p.call(f"{p.API}/{ig_id}/media", data=urllib.parse.urlencode({
        "media_type": "CAROUSEL", "children": ",".join(children),
        "caption": caption, "access_token": token}).encode())["id"]
    wait(parent, token)
    p.call(f"{p.API}/{ig_id}/media_publish", data=urllib.parse.urlencode({
        "creation_id": parent, "access_token": token}).encode())
    print("Pubblicato!")
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(datetime.now(ZoneInfo("UTC")).isoformat())

    DONE.mkdir(parents=True, exist_ok=True)
    shutil.move(folder, DONE / folder.name)


if __name__ == "__main__":
    main()
