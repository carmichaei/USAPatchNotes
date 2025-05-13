# run_fetch_gui.py
import tkinter as tk
from tkinter import messagebox
import subprocess

def run_fetch():
    date = entry.get()
    if not date:
        messagebox.showerror("Missing Date", "Please enter a date in YYYY-MM-DD format.")
        return

    try:
        result = subprocess.run(
            ["python", "fetch_eos.py", date],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            messagebox.showinfo("Success", f"Fetch complete for {date}")
        else:
            messagebox.showerror("Error", result.stderr)
    except Exception as e:
        messagebox.showerror("Execution Failed", str(e))

root = tk.Tk()
root.title("EO Patch Fetcher")

tk.Label(root, text="Enter date (YYYY-MM-DD):").pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)

tk.Button(root, text="Fetch Executive Orders", command=run_fetch).pack(pady=10)
root.mainloop()
