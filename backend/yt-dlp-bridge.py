#!/usr/bin/env python3
"""YT-DLP Bridge Server v1.2 - Browser Extension Backend"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import threading
import os
import sys
import json
import uuid
import shutil
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)

SETTINGS_FILE = Path(__file__).parent / "settings.json"
DOWNLOADS = {}


def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "download_dir": str(Path.home() / "Downloads"),
        "format": "best",
        "port": 8765
    }


SETTINGS = load_settings()


def save_settings():
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(SETTINGS, f, indent=2)
    except Exception as e:
        print("[WARN] Failed to save settings:", e)


def find_ytdlp():
    ytdlp = shutil.which("yt-dlp") or shutil.which("yt-dlp.exe")
    if ytdlp:
        return ytdlp
    candidates = [
        Path.home() / "Downloads" / "yt-dlp.exe",
        Path.home() / "Downloads" / "yt-dlp",
        Path(__file__).parent / "yt-dlp.exe",
        Path(__file__).parent / "yt-dlp",
    ]
    for p in sys.path:
        pp = Path(p)
        if pp.name == "Scripts" or "site-packages" in str(pp):
            candidates.append(pp / "yt-dlp.exe")
            candidates.append(pp / "yt-dlp")
    for c in candidates:
        if c.exists():
            return str(c)
    return "yt-dlp"


def build_cmd(url, fmt, save_dir):
    exe = find_ytdlp()
    cmd = [exe, url, "--newline", "--no-warnings", "--no-color", "--no-playlist"]
    if fmt == "1080p":
        cmd.extend(["-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]"])
    elif fmt == "720p":
        cmd.extend(["-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]"])
    elif fmt == "mp3":
        cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
    out_tpl = os.path.join(save_dir, "%(title)s.%(ext)s")
    cmd.extend(["-o", out_tpl])
    return cmd


def parse_line(line):
    line = line.strip()
    if not line:
        return None, None, None, None

    pct = None
    speed = None
    eta = None
    title = None

    if "[download]" in line and "%" in line:
        try:
            parts = line.split()
            for p in parts:
                if "%" in p:
                    pct = float(p.replace("%", ""))
                    break
        except Exception:
            pass

    if " at " in line and "/s" in line:
        try:
            at_idx = line.index(" at ")
            rest = line[at_idx + 4:].strip()
            parts2 = rest.split()
            for p in parts2:
                if "/s" in p:
                    speed = p
                    break
        except Exception:
            pass

    if "ETA " in line:
        try:
            eta_idx = line.index("ETA ")
            eta = line[eta_idx + 4:eta_idx + 9].strip()
        except Exception:
            pass

    if "Destination:" in line:
        try:
            dest = line.split("Destination:", 1)[1].strip()
            title = Path(dest).stem
        except Exception:
            pass

    return pct, speed, eta, title


def download_worker(job_id, url, fmt, save_dir):
    DOWNLOADS[job_id] = {
        "status": "Starting",
        "progress": 0.0,
        "title": "-",
        "speed": "-",
        "eta": "-",
        "url": url,
        "started": datetime.now().isoformat(),
        "error": None
    }

    if not os.path.isdir(save_dir):
        try:
            os.makedirs(save_dir, exist_ok=True)
        except Exception as e:
            DOWNLOADS[job_id]["status"] = "Error"
            DOWNLOADS[job_id]["error"] = "Cannot create directory: " + str(e)
            return

    cmd = build_cmd(url, fmt, save_dir)

    try:
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=flags,
            bufsize=1
        )
        DOWNLOADS[job_id]["status"] = "Downloading"
        DOWNLOADS[job_id]["pid"] = proc.pid

        for line in proc.stdout:
            pct, speed, eta, title = parse_line(line)
            if pct is not None:
                DOWNLOADS[job_id]["progress"] = pct
            if speed:
                DOWNLOADS[job_id]["speed"] = speed
            if eta:
                DOWNLOADS[job_id]["eta"] = eta
            if title:
                DOWNLOADS[job_id]["title"] = title
            if "has already been downloaded" in line:
                DOWNLOADS[job_id]["status"] = "Completed"
                DOWNLOADS[job_id]["progress"] = 100.0

        proc.wait()
        if proc.returncode == 0:
            DOWNLOADS[job_id]["status"] = "Completed"
            DOWNLOADS[job_id]["progress"] = 100.0
        else:
            DOWNLOADS[job_id]["status"] = "Error"
            if not DOWNLOADS[job_id]["error"]:
                DOWNLOADS[job_id]["error"] = "yt-dlp exited with code " + str(proc.returncode)

    except FileNotFoundError:
        DOWNLOADS[job_id]["status"] = "Error"
        DOWNLOADS[job_id]["error"] = "yt-dlp not found. Place yt-dlp.exe in Downloads or this folder."
    except Exception as e:
        DOWNLOADS[job_id]["status"] = "Error"
        DOWNLOADS[job_id]["error"] = str(e)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "ytdlp": find_ytdlp()})


@app.route("/download", methods=["POST"])
def start_download():
    data = request.json or {}
    url = data.get("url", "").strip()
    fmt = data.get("format", SETTINGS.get("format", "best"))
    save_dir = data.get("save_dir", SETTINGS.get("download_dir", str(Path.home() / "Downloads")))
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "Invalid URL"}), 400
    job_id = str(uuid.uuid4())[:8]
    t = threading.Thread(target=download_worker, args=(job_id, url, fmt, save_dir), daemon=True)
    t.start()
    return jsonify({"job_id": job_id, "status": "started"})


@app.route("/progress/<job_id>", methods=["GET"])
def get_progress(job_id):
    return jsonify(DOWNLOADS.get(job_id, {"status": "Unknown"}))


@app.route("/jobs", methods=["GET"])
def get_jobs():
    return jsonify(DOWNLOADS)


@app.route("/settings", methods=["GET"])
def get_settings():
    return jsonify(SETTINGS)


@app.route("/settings", methods=["POST"])
def update_settings():
    global SETTINGS
    data = request.json or {}
    SETTINGS.update(data)
    save_settings()
    return jsonify(SETTINGS)


if __name__ == "__main__":
    print("=" * 50)
    print("  YT-DLP Bridge Server v1.2")
    print("=" * 50)
    print("  Server:   http://127.0.0.1:" + str(SETTINGS["port"]))
    print("  yt-dlp:   " + find_ytdlp())
    print("  Download: " + SETTINGS["download_dir"])
    print("=" * 50)
    print("  Press Ctrl+C to stop")
    print("=" * 50)
    print()
    try:
        app.run(host="127.0.0.1", port=SETTINGS["port"], threaded=True, debug=False)
    except KeyboardInterrupt:
        print("\n[Server stopped]")
