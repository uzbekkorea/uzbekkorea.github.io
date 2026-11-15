# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Generate dialog audio with VoiceStudio (OmniVoice).

Usage:
    uv run tools/tts.py p2-ch01            # generate missing or changed clips
    uv run tools/tts.py p2-ch01 --force    # regenerate everything
    uv run tools/tts.py p2-ch01 --adopt p01-ko=take.wav
                                           # use a clip approved by ear as is

Reads _data/dialogs/<name>.yml and writes assets/audio/<name>/:
    <id>-ko.m4a, <id>-uz.m4a   one clip per line and language
    chapter.m4a                the whole dialog, Korean then Uzbek per line
    manifest.json              hash of what each clip was made from

VoiceStudio must be running (it serves the API on 127.0.0.1:3900).
"""

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import uuid
import wave
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
API = "http://127.0.0.1:3900"
ENGINE = "omnivoice"
GAP_BETWEEN_LANGS = 0.6  # seconds of silence in chapter.m4a
GAP_BETWEEN_LINES = 1.0

# OmniVoice reads the current o'/sh spelling better than the new alphabet,
# so Uzbek text is converted just before synthesis. The page keeps the new alphabet.
UZ_OLD_SPELLING = {
    "ö": "o'", "Ö": "O'",
    "ğ": "g'", "Ğ": "G'",
    "ş": "sh", "Ş": "Sh",
    "ç": "ch", "Ç": "Ch",
    "ʼ": "'",
}


def to_old_spelling(text):
    return "".join(UZ_OLD_SPELLING.get(c, c) for c in text)


def post_generate(text, lang, instruct, seed, duration=None):
    boundary = uuid.uuid4().hex
    fields = {"text": text, "language": lang, "instruct": instruct, "seed": str(seed)}
    if duration:
        fields["duration"] = str(duration)
    body = b"".join(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
        for k, v in fields.items()
    ) + f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"{API}/generate",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        if not resp.headers.get("Content-Type", "").startswith("audio/wav"):
            raise RuntimeError(f"unexpected response: {resp.read()[:300]!r}")
        return resp.read()


def wav_to_m4a(wav_path, m4a_path):
    subprocess.run(
        ["afconvert", "-f", "m4af", "-d", "aac", "-b", "48000", str(wav_path), str(m4a_path)],
        check=True,
    )


def m4a_to_wav(m4a_path, wav_path):
    subprocess.run(
        ["afconvert", "-f", "WAVE", "-d", "LEI16@24000", str(m4a_path), str(wav_path)],
        check=True,
    )


def build_chapter(clips, out_m4a, tmp):
    """Join clips [(path, gap_after_seconds)] into one m4a."""
    joined = tmp / "chapter.wav"
    with wave.open(str(joined), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(24000)
        for i, (m4a, gap) in enumerate(clips):
            wav = tmp / f"part{i}.wav"
            m4a_to_wav(m4a, wav)
            with wave.open(str(wav), "rb") as w:
                out.writeframes(w.readframes(w.getnframes()))
            out.writeframes(b"\x00\x00" * int(24000 * gap))
    wav_to_m4a(joined, out_m4a)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="dialog data file name, e.g. p2-ch01")
    parser.add_argument("--force", action="store_true", help="regenerate all clips")
    parser.add_argument("--adopt", action="append", default=[], metavar="KEY=WAV",
                        help="install a WAV for clip KEY (e.g. p01-ko) instead of generating it")
    args = parser.parse_args()
    adopt = dict(a.split("=", 1) for a in args.adopt)

    data_file = ROOT / "_data" / "dialogs" / f"{args.name}.yml"
    data = yaml.safe_load(data_file.read_text(encoding="utf-8"))
    out_dir = ROOT / "assets" / "audio" / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "manifest.json"
    manifest = {} if args.force or not manifest_path.exists() else json.loads(manifest_path.read_text())

    try:
        urllib.request.urlopen(f"{API}/engines/tts", timeout=5)
    except (urllib.error.URLError, OSError):
        sys.exit("VoiceStudio is not running. Open the VoiceStudio app and try again.")

    items = [it for section in ("dialog", "phrases") for it in data.get(section) or []]
    changed = False
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for it in items:
            voice = data["speakers"][it["speaker"]]["voice"]
            for lang in ("ko", "uz"):
                # `tts` gives the text to speak when it differs from the text shown
                text = (it.get("tts") or {}).get(lang) or it[lang]
                if lang == "uz":
                    text = to_old_spelling(text)
                v = voice[lang]
                duration = (it.get("duration") or {}).get(lang)
                key = f"{it['id']}-{lang}"
                digest = hashlib.sha256(
                    json.dumps([ENGINE, lang, text, v["instruct"], v["seed"], duration], ensure_ascii=False).encode()
                ).hexdigest()[:16]
                m4a = out_dir / f"{key}.m4a"
                if key in adopt:
                    print(f"{key}: adopted {adopt[key]}")
                    wav_to_m4a(Path(adopt[key]), m4a)
                    manifest[key] = digest
                    changed = True
                    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
                    continue
                if manifest.get(key) == digest and m4a.exists():
                    continue
                print(f"{key}: {text}")
                wav = tmp / f"{key}.wav"
                wav.write_bytes(post_generate(text, lang, v["instruct"], v["seed"], duration))
                wav_to_m4a(wav, m4a)
                manifest[key] = digest
                changed = True
                manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        chapter = out_dir / "chapter.m4a"
        if data.get("dialog") and (changed or not chapter.exists()):
            clips = []
            for it in data["dialog"]:
                clips.append((out_dir / f"{it['id']}-ko.m4a", GAP_BETWEEN_LANGS))
                clips.append((out_dir / f"{it['id']}-uz.m4a", GAP_BETWEEN_LINES))
            build_chapter(clips, chapter, tmp)
            print("chapter.m4a: rebuilt")

    print("Done." if changed else "Up to date.")


if __name__ == "__main__":
    main()
