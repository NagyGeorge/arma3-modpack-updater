import os
import shutil

def deploy_mods(modlist, steamcmd_download_dir, deploy_dir, symlink=True, logger=None):
    workshop_dir = os.path.join(steamcmd_download_dir, "steamapps", "workshop", "content", "107410")
    os.makedirs(deploy_dir, exist_ok=True)

    for mod in modlist:
        mod_id = mod['id']
        mod_name = f"@{mod['name'].replace(' ', '_')}"
        source_path = os.path.join(workshop_dir, mod_id)
        target_path = os.path.join(deploy_dir, mod_name)

        if not os.path.exists(source_path):
            if logger:
                logger(f"Source folder missing for {mod_name} (ID {mod_id})")
            continue

        if os.path.exists(target_path):
            if logger:
                logger(f"ℹ️ Mod {mod_name} already deployed, skipping.")
            continue

        try:
            if symlink:
                os.symlink(source_path, target_path, target_is_directory=True)
                if logger:
                    logger(f"Symlinked {mod_name} → {target_path}")
            else:
                shutil.copytree(source_path, target_path)
                if logger:
                    logger(f"Copied {mod_name} → {target_path}")
        except Exception as e:
            if logger:
                logger(f"Failed to deploy {mod_name}: {str(e)}")