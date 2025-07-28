import subprocess
import os
import tempfile

STEAM_APP_ID = 107410  # Arma 3

def download_mods_with_steamcmd(username, password, mod_ids, steamcmd_path="C:\\SteamCMD\\steamcmd.exe", logger=None):
    if logger:
        logger("[DEBUG] Entered steamcmd.py function")
    print("[DEBUG] Entered steamcmd.py function")

    for mod_id in mod_ids:
        if logger:
            logger(f"[DEBUG] About to download {mod_id}")
        print(f"[DEBUG] About to download {mod_id}")

        #return  # early return to test if this even runs

        # Create SteamCMD script
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as script_file:
            script_file.write(f"login {username}\n")
            script_file.write(f"workshop_download_item {STEAM_APP_ID} {mod_id}\n")
            script_file.write("quit\n")
            script_path = script_file.name

        if logger:
            logger(f"[DEBUG] Creating SteamCMD script")
        print(f"[DEBUG] Creating SteamCMD script")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as script_file:
            script_file.write(f"login {username}\n")
            script_file.write(f"workshop_download_item {STEAM_APP_ID} {mod_id}\n")
            script_file.write("quit\n")
            script_path = script_file.name

        if logger:
            logger(f"[DEBUG] Running SteamCMD with script: {script_path}")
        print(f"[DEBUG] Running SteamCMD with script: {script_path}")

        try:
            result = subprocess.run(
                [steamcmd_path, "+runscript", script_path],
                capture_output=True,
                text=True,
                timeout=300  # timeout after 5 minutes
            )

            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip())

            if logger:
                logger(result.stdout.strip())

        except Exception as e:
            if logger:
                logger(f"[ERROR] Subprocess failed: {str(e)}")
            print(f"[ERROR] Subprocess failed: {str(e)}")