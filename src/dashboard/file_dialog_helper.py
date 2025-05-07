import tkinter as tk
from tkinter import filedialog, messagebox
import json
import sys

def main():
    root = tk.Tk()
    root.withdraw()
    try:
        answer = messagebox.askquestion("Select Type", "Single File?\nClick 'No' to select a folder.")
        if answer == 'yes':
            path = filedialog.askopenfilename(
                title="Select Python File",
                filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
            )
        else:
            path = filedialog.askdirectory(title="Select Folder")
        print(json.dumps({"path": path if path else None}))
    except Exception:
        print(json.dumps({"path": None}))
    finally:
        root.destroy()

if __name__ == "__main__":
    main()
