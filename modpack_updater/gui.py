import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from modpack_updater.parser import parse_arma3_modlist_table
from modpack_updater.steamcmd import download_mods_with_steamcmd

# Global: store modlist across tabs
parsed_modlist = []

def run_gui():
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
            title="Select Arma 3 HTML Modlist",
            filetypes=[("HTML Files", "*.html")]
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

    tk.Label(tab_download, text="Steam Password:").pack(pady=(10, 0))
    password_entry = tk.Entry(tab_download, width=40, show="*")
    password_entry.pack()

    #Folder Selection
    tk.Label(tab_download, text="Mod Download Folder:").pack(pady=(10, 0))
    download_dir_var = tk.StringVar()
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

    # Callback
    def download_mods():
        username = username_entry.get()
        password = password_entry.get()

        download_dir = download_dir_var.get()
        if not os.path.exists(download_dir):
            messagebox.showerror("Error", "Please select a valid download directory.")
            return


        def log_line(text):
            download_output.insert(tk.END, text + "\n")
            download_output.see(tk.END)

        mod_ids = ['843577117']  # RHSUSAF, single known ID

        log_line("Starting download of 1 mod...")

        from modpack_updater.steamcmd import download_mods_with_steamcmd

        download_mods_with_steamcmd(username, mod_ids, download_dir, logger=log_line)
        
        log_line("Finished")

    # Button
    tk.Button(tab_download, text="Download Mods", command=download_mods).pack(pady=5)

    root.mainloop()