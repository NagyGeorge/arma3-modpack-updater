"""Tkinter based GUI for the modpack updater."""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from modpack_updater.parser import parse_arma3_modlist_table

# Global: store modlist across tabs
parsed_modlist = []


def run_gui():
    from modpack_updater.config import load_config, save_config

    config = load_config()

    root = tk.Tk()
    root.title("Arma 3 Modpack Updater")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # TAB 1: Modlist Import
    tab_import = ttk.Frame(notebook)
    notebook.add(tab_import, text="Import Modlist")

    import_output = scrolledtext.ScrolledText(tab_import, width=90, height=30)
    import_output.pack(padx=10, pady=10)

    def open_file():
        global parsed_modlist
        file_path = filedialog.askopenfilename(
            title="Select Arma 3 HTML Modlist", filetypes=[("HTML Files", "*.html")]
        )
        if not file_path:
            return

        try:
            parsed_modlist = parse_arma3_modlist_table(file_path)
            import_output.delete(1.0, tk.END)
            for mod in parsed_modlist:
                import_output.insert(tk.END, f"{mod['name']} - ID: {mod['id']}\n")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse modlist:\n{str(e)}")

    tk.Button(tab_import, text="Import Modlist", command=open_file).pack(pady=5)

    # TAB 2: SteamCMD Download
    tab_download = ttk.Frame(notebook)
    notebook.add(tab_download, text="Download Mods")

    # Login fields
    tk.Label(tab_download, text="Steam Username:").pack(pady=(10, 0))
    username_entry = tk.Entry(tab_download, width=40)
    username_entry.pack()

    # Pre-fill username if 'remember_username' was saved
    if config.get("remember_username"):
        username_entry.insert(0, config.get("username", ""))

    tk.Label(tab_download, text="Steam Password:").pack(pady=(10, 0))
    password_entry = tk.Entry(tab_download, width=40, show="*")
    password_entry.pack()

    # Remember Username checkbox
    remember_username_var = tk.BooleanVar(value=config.get("remember_username", False))
    tk.Checkbutton(
        tab_download, text="Remember Username", variable=remember_username_var
    ).pack()

    # Folder Selection
    tk.Label(tab_download, text="Mod Download Folder:").pack(pady=(10, 0))
    download_dir_var = tk.StringVar()
    download_dir_var.set(config.get("download_dir", ""))
    download_dir_entry = tk.Entry(tab_download, textvariable=download_dir_var, width=60)
    download_dir_entry.pack(pady=(0, 5))

    def choose_download_folder():
        path = filedialog.askdirectory()
        if path:
            download_dir_var.set(path)

    tk.Button(tab_download, text="Select Folder", command=choose_download_folder).pack()

    # Output
    download_output = scrolledtext.ScrolledText(tab_download, width=90, height=25)
    download_output.pack(padx=10, pady=10)

    # Download button
    download_button = tk.Button(tab_download, text="Download Mods")
    download_button.pack(pady=5)

    # Callback
    def download_mods():
        username = username_entry.get()
        download_dir = download_dir_var.get()

        if not os.path.exists(download_dir):
            messagebox.showerror("Error", "Please select a valid download directory.")
            return

        if not parsed_modlist:
            messagebox.showerror(
                "Error", "No modlist imported. Please import a modlist first."
            )
            return

        def log_line(text):
            download_output.insert(tk.END, text + "\n")
            download_output.see(tk.END)

        mod_ids = [mod["id"] for mod in parsed_modlist]
        log_line(f"Starting download of {len(mod_ids)} mod(s)...")

        # Disable button during download
        download_button.config(state=tk.DISABLED)

        # Worker function for background thread
        def worker():
            from modpack_updater.steamcmd import (
                download_mods_with_steamcmd,
                flatten_mods,
            )

            download_mods_with_steamcmd(
                username, mod_ids, download_dir, logger=log_line
            )
            flatten_mods(download_dir, logger=log_line)
            log_line("Finished downloading mods.")
            root.after(0, lambda: download_button.config(state=tk.NORMAL))

        threading.Thread(target=worker, daemon=True).start()

    # Bind the button
    download_button.config(command=download_mods)

    # TAB 3: Deploy Mods
    tab_deploy = ttk.Frame(notebook)
    notebook.add(tab_deploy, text="Deploy Mods")

    # Deployment folder selection
    tk.Label(tab_deploy, text="Deploy Mods To Folder:").pack(pady=(10, 0))
    deploy_dir_var = tk.StringVar()
    deploy_dir_var.set(config.get("deploy_dir", ""))
    deploy_dir_entry = tk.Entry(tab_deploy, textvariable=deploy_dir_var, width=60)
    deploy_dir_entry.pack(pady=(0, 5))

    def choose_deploy_folder():
        path = filedialog.askdirectory()
        if path:
            deploy_dir_var.set(path)

    tk.Button(tab_deploy, text="Select Folder", command=choose_deploy_folder).pack()

    # Deployment log output
    deploy_output = scrolledtext.ScrolledText(tab_deploy, width=90, height=25)
    deploy_output.pack(padx=10, pady=10)

    # Deploy button
    deploy_button = tk.Button(tab_deploy, text="Deploy Mods")
    deploy_button.pack(pady=5)

    def deploy_mods_gui():
        deploy_dir = deploy_dir_var.get()
        if not os.path.exists(deploy_dir):
            messagebox.showerror("Error", "Please select a valid deployment directory.")
            return

        if not parsed_modlist:
            messagebox.showerror(
                "Error", "No modlist imported. Please import a modlist first."
            )
            return

        def log_line(text):
            deploy_output.insert(tk.END, text + "\n")
            deploy_output.see(tk.END)

        log_line(f"Starting deployment of {len(parsed_modlist)} mod(s)...")

        # Disable deploy button during operation
        deploy_button.config(state=tk.DISABLED)

        # Worker function to run in background
        def worker():
            from modpack_updater.deploy import deploy_mods

            # Replace this path with the same folder you used for SteamCMD downloads
            steamcmd_download_dir = download_dir_var.get()

            deploy_mods(
                parsed_modlist,
                steamcmd_download_dir,
                deploy_dir,
                symlink=True,
                logger=log_line,
            )

            log_line("✅ Deployment complete.")
            root.after(0, lambda: deploy_button.config(state=tk.NORMAL))

        threading.Thread(target=worker, daemon=True).start()

    deploy_button.config(command=deploy_mods_gui)

    def on_close():
        new_config = {
            "download_dir": download_dir_var.get(),
            "deploy_dir": deploy_dir_var.get(),
            "remember_username": remember_username_var.get(),
        }
        if remember_username_var.get():
            new_config["username"] = username_entry.get()
        save_config(new_config)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
