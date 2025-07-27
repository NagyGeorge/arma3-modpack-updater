import subprocess
import os
import tempfile

STEAM_APP_ID = 107410  # Arma 3

def download_mods_with_steamcmd(username, password, mod_ids, steamcmd_path="C:\\SteamCMD\\steamcmd.exe", logger=None):
    if not os.path.exists(steamcmd_path):
        raise FileNotFoundError(f"SteamCMD not found at: {steamcmd_path}")

    for mod_id in mod_ids:
        if logger:
            logger(f"→ Downloading mod ID: {mod_id}")

        # Create SteamCMD script
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as script_file:
            script_file.write(f"login {username} {password}\n")
            script_file.write(f"workshop_download_item {STEAM_APP_ID} {mod_id}\n")
            script_file.write("quit\n")
            script_path = script_file.name

        try:
            result = subprocess.run(
                [steamcmd_path, "+runscript", script_path],
                capture_output=True, text=True, timeout=300  # 5 min timeout per mod
            )

            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip())

            if logger:
                logger(result.stdout.strip())

        except Exception as e:
            if logger:
                logger(f"❌ Error downloading {mod_id}: {str(e)}")
