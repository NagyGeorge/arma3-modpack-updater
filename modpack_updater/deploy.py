"""Deployment utilities for downloaded mods."""

import os
import shutil

from .utils import log


def deploy_mods(
    modlist: list[dict],
    steamcmd_download_dir: str,
    deploy_dir: str,
    symlink: bool = True,
    logger: callable | None = None,
) -> None:
    """Deploy mods to ``deploy_dir`` using symlinks or copies."""

    workshop_dir = os.path.join(steamcmd_download_dir, "mods")
    os.makedirs(deploy_dir, exist_ok=True)

    for mod in modlist:
        mod_id = mod["id"]
        mod_name = f"@{mod['name'].replace(' ', '_')}"
        source_path = os.path.join(workshop_dir, mod_id)
        target_path = os.path.join(deploy_dir, mod_name)

        if not os.path.exists(source_path):
            log(f"Source folder missing for {mod_name} (ID {mod_id})", logger)
            continue

        if os.path.exists(target_path):
            log(f"ℹMod {mod_name} already deployed, skipping.", logger)
            continue

        try:
            if symlink:
                os.symlink(source_path, target_path, target_is_directory=True)
                log(f"Symlinked {mod_name} → {target_path}", logger)
            else:
                shutil.copytree(source_path, target_path)
                log(f"Copied {mod_name} → {target_path}", logger)
        except Exception as e:
            log(f"Failed to deploy {mod_name}: {str(e)}", logger)
