import subprocess
import os
import tempfile

STEAM_APP_ID = 107410  # Arma 3

def download_mods_with_steamcmd(username, mod_ids, download_dir, steamcmd_path="C:\\SteamCMD\\steamcmd.exe", logger=None):
    if logger:
        logger("[DEBUG] Entered steamcmd.py function")
    print("[DEBUG] Entered steamcmd.py function")

    # Ensure download directory exists
    os.makedirs(download_dir, exist_ok=True)

    for mod_id in mod_ids:
        if logger:
            logger(f"[DEBUG] About to download {mod_id}")
        print(f"[DEBUG] About to download {mod_id}")

        # Generate script content
        script_content = (
            f"force_install_dir {download_dir}\n"
            f"login {username}\n"
            f"workshop_download_item {STEAM_APP_ID} {mod_id}\n"
            f"quit\n"
        )

        # Create a temporary script
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as script_file:
            script_file.write(script_content)
            script_path = script_file.name

        if logger:
            logger(f"[DEBUG] Running SteamCMD with script: {script_path}")
        print(f"[DEBUG] Running SteamCMD with script: {script_path}")

        # Real-time streaming of output
        process = subprocess.Popen(
            [steamcmd_path, "+runscript", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # line-buffered
        )

        # Stream lines as they arrive
        for line in process.stdout:
            line = line.strip()
            if line:
                if logger:
                    logger(line)
                print(line)

        process.wait()

        # Check for errors
        if process.returncode != 0:
            msg = f"[ERROR] SteamCMD failed for mod {mod_id} (exit code {process.returncode})"
            if logger:
                logger(msg)
            print(msg)

        # Cleanup temp file
        try:
            os.remove(script_path)
        except OSError:
            pass
