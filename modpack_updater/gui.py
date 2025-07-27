import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from modpack_updater.parser import parse_arma3_modlist_table

def run_gui():
    # Window setup
    root = tk.Tk()
    root.title("Arma 3 Modpack Updater")
    root.geometry("700x500")

    # Header
    tk.Label(root, text="Import Modlist (.html)", font=("Segoe UI", 14)).pack(pady=10)

    # Output window
    output_box = scrolledtext.ScrolledText(root, width=80, height=25)
    output_box.pack(padx=10, pady=10)

    # Button callback
    def open_file():
        file_path = filedialog.askopenfilename(
            title="Select Arma 3 HTML Modlist",
            filetypes=[("HTML Files", "*.html")]
        )
        if not file_path:
            return

        try:
            modlist = parse_arma3_modlist_table(file_path)
            output_box.delete(1.0, tk.END)  # Clear previous output

            for mod in modlist:
                output_box.insert(tk.END, f"{mod['name']} - ID: {mod['id']}\n")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse modlist:\n{str(e)}")

    # Button
    tk.Button(root, text="Import Modlist", command=open_file).pack(pady=10)

    # Run GUI loop
    root.mainloop()
