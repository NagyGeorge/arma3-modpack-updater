"""Helpers for interacting with SteamCMD."""

import os
import subprocess
import tempfile

from .utils import log

STEAM_APP_ID = 107410  # Arma 3


def download_mods_with_steamcmd(
    username: str,
    mod_ids: list[str],
    download_dir: str,
    steamcmd_path: str = "C:\\SteamCMD\\steamcmd.exe",
    logger: callable | None = None,
) -> None:
    """Download a list of mods using SteamCMD."""

    log("[DEBUG] Entered steamcmd.py function", logger)

    # Ensure download directory exists
    flattened_dir = os.path.join(
        download_dir, "mods", "steamapps", "workshop", "content", "107410"
    )
    os.makedirs(flattened_dir, exist_ok=True)

    for mod_id in mod_ids:
        log(f"[DEBUG] About to download {mod_id}", logger)

        # Generate script content
        script_content = (
            f"force_install_dir {flattened_dir}\n"
            f"login {username}\n"
            f"workshop_download_item {STEAM_APP_ID} {mod_id}\n"
            f"quit\n"
        )

        # Create a temporary script
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".txt", mode="w", encoding="utf-8"
        ) as script_file:
            script_file.write(script_content)
            script_path = script_file.name

        log(f"[DEBUG] Running SteamCMD with script: {script_path}", logger)

        # Real-time streaming of output
        process = subprocess.Popen(
            [steamcmd_path, "+runscript", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # line-buffered
        )

        # Stream lines as they arrive
        for line in process.stdout:
            line = line.strip()
            if line:
                log(line, logger)

        process.wait()

        # Check for errors
        if process.returncode != 0:
            msg = (
                f"[ERROR] SteamCMD failed for mod {mod_id} "
                f"(exit code {process.returncode})"
            )
            log(msg, logger)

        # Cleanup temp file
        try:
            os.remove(script_path)
        except OSError:
            pass


def flatten_mods(download_dir: str, logger: callable | None = None) -> None:
    """Move downloaded mods into a flat directory structure."""

    workshop_dir = os.path.join(
        download_dir, "mods", "steamapps", "workshop", "content", "107410"
    )
    target_dir = os.path.join(download_dir, "mods")

    if not os.path.exists(workshop_dir):
        return

    for item in os.listdir(workshop_dir):
        src = os.path.join(workshop_dir, item)
        dst = os.path.join(target_dir, item)
        if os.path.isdir(src):
            if not os.path.exists(dst):
                os.rename(src, dst)
                log(f"Moved {item} to flattened mods directory", logger)

    # Cleanup empty steam structure
    steamapps_root = os.path.join(download_dir, "mods", "steamapps")
    import shutil

    try:
        shutil.rmtree(steamapps_root)
        log("Cleaned up SteamCMD scaffolding.", logger)
    except OSError:
        pass
