from ui import NQueensUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("16-Queens Problem")

    # Disable window resizing
    root.resizable(False, False)

    app = NQueensUI(root, size=16, cell_size=40, offset=40)
    root.mainloop()
