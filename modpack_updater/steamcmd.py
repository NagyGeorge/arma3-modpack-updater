import subprocess
import os
import tempfile

STEAM_APP_ID = 107410  # Arma 3

def download_mods_with_steamcmd(username, mod_ids, download_dir, steamcmd_path="C:\\SteamCMD\\steamcmd.exe", logger=None):
    if logger:
        logger("[DEBUG] Entered steamcmd.py function")
    print("[DEBUG] Entered steamcmd.py function")

    # Make sure download directory exists
    os.makedirs(download_dir, exist_ok=True)

    for mod_id in mod_ids:
        if logger:
            logger(f"[DEBUG] About to download {mod_id}")
        print(f"[DEBUG] About to download {mod_id}")

        # Generate the script content
        script_content = (
            f"force_install_dir {download_dir}\n"
            f"login {username}\n"
            f"workshop_download_item {STEAM_APP_ID} {mod_id}\n"
            f"quit\n"
        )

        # Create a temp script and close it to avoid Windows file locks
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as script_file:
            script_file.write(script_content)
            script_path = script_file.name

        if logger:
            logger(f"[DEBUG] Running SteamCMD with script: {script_path}")
        print(f"[DEBUG] Running SteamCMD with script: {script_path}")

        try:
            result = subprocess.run(
                [steamcmd_path, "+runscript", script_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 min per mod
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip() or "Unknown error"
                if logger:
                    logger(f"[ERROR] SteamCMD failed for mod {mod_id}: {error_msg}")
                print(f"[ERROR] SteamCMD failed for mod {mod_id}: {error_msg}")
            else:
                output = result.stdout.strip()
                if logger:
                    logger(output)
                print(output)

        except Exception as e:
            if logger:
                logger(f"[ERROR] Subprocess failed for mod {mod_id}: {str(e)}")
            print(f"[ERROR] Subprocess failed for mod {mod_id}: {str(e)}")

        finally:
            # Optional: Clean up temp script
            try:
                os.remove(script_path)
            except OSError:
                pass
