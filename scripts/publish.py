"""Pubblica la prossima foto in queue/ su Instagram e la sposta in published/.

Instagram scarica la foto da un link pubblico: il repo deve essere pubblico.
"""
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

API = "https://graph.instagram.com/v21.0"
ROOT = Path(__file__).resolve().parent.parent
QUEUE, DONE = ROOT / "queue", ROOT / "published"
STATE = ROOT / "state" / "last_publish.txt"

# Giorni (0=lun) e fasce orarie italiane delle uscite: lun, mar, gio, sab verso le 12:30
DAYS = (0, 1, 3, 5)
SLOT = ((12, 0), (13, 15))


def call(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Errore API {e.code}: {e.read().decode()}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() if path.exists() else ""


def list_images(folder: Path) -> list:
    return sorted(f for f in folder.iterdir() if f.suffix.lower() in (".jpg", ".jpeg"))


def next_cta() -> str:
    lines = [l.strip() for l in read(ROOT / "config" / "cta.txt").splitlines() if l.strip()]
    return lines[len(list_images(DONE)) % len(lines)] if lines else ""


def build_caption(image: Path) -> str:
    """Frase iniziale + caption + frase finale + CTA + hashtag fissi.

    Nel .txt la CTA va dopo una riga con solo `---`; se scrivi solo NESSUNA, nessuna CTA.
    """
    raw = read(image.with_suffix(".txt"))
    caption, _, cta = raw.partition("\n---\n")
    cfg = ROOT / "config"
    cta = cta.strip()
    no_cta = cta.upper() == "NESSUNA"
    parts = [
        read(cfg / "frase_iniziale.txt"),
        caption.strip(),
        read(cfg / "frase_finale.txt"),
        "" if no_cta else (cta or next_cta()),
        read(cfg / "hashtag.txt"),
    ]
    return "\n\n".join(p for p in parts if p)


def in_slot() -> bool:
    now = datetime.now(ZoneInfo("Europe/Rome"))
    return now.weekday() in DAYS and SLOT[0] <= (now.hour, now.minute) <= SLOT[1]


def published_recently(hours: float = 6) -> bool:
    if not STATE.exists():
        return False
    last = datetime.fromisoformat(STATE.read_text().strip())
    return (datetime.now(ZoneInfo("UTC")) - last).total_seconds() < hours * 3600


def main():
    scheduled = os.environ.get("GITHUB_EVENT_NAME") == "schedule"
    if scheduled and not in_slot():
        print("Fuori giorno o fascia oraria italiana: niente da fare.")
        return
    if scheduled and published_recently():
        print("Già pubblicato in questa fascia: niente da fare.")
        return
    images = [i for i in list_images(QUEUE) if i.with_suffix(".txt").exists()]
    if not images:
        print("Nessun post completo (foto JPEG + caption) in coda: niente da pubblicare.")
        return
    image = images[0]
    caption = build_caption(image)
    print(f"Pubblico: {image.name}")
    if os.environ.get("DRY_RUN") == "1":
        print(f"[DRY RUN] Caption:\n{caption}")
        return

    ig_id, token = os.environ["IG_USER_ID"], os.environ["IG_ACCESS_TOKEN"]
    url = (f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}"
           f"/main/queue/{urllib.parse.quote(image.name)}")

    container = call(
        f"{API}/{ig_id}/media",
        data=urllib.parse.urlencode({
            "image_url": url, "caption": caption, "access_token": token,
        }).encode(),
    )["id"]

    for _ in range(30):
        code = call(f"{API}/{container}?fields=status_code&access_token={token}").get("status_code")
        if code == "FINISHED":
            break
        if code in ("ERROR", "EXPIRED"):
            sys.exit(f"Elaborazione fallita: {code}")
        time.sleep(5)

    call(
        f"{API}/{ig_id}/media_publish",
        data=urllib.parse.urlencode({"creation_id": container, "access_token": token}).encode(),
    )
    print("Pubblicato!")
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(datetime.now(ZoneInfo("UTC")).isoformat())

    DONE.mkdir(exist_ok=True)
    shutil.move(image, DONE / image.name)
    shutil.move(image.with_suffix(".txt"), DONE / image.with_suffix(".txt").name)


if __name__ == "__main__":
    main()
