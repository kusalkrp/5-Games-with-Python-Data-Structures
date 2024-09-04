import tkinter as tk

def create_chessboard(canvas, size, cell_size, offset):
    color1 = "#954535"  # Brown color
    color2 = "#F5DEB3"  # White color

    for row in range(size):
        for col in range(size):
            color = color1 if (row + col) % 2 == 0 else color2
            canvas.create_rectangle(
                col * cell_size + offset, row * cell_size + offset,
                (col + 1) * cell_size + offset, (row + 1) * cell_size + offset,
                fill=color, outline=color
            )

def add_labels(root, size, cell_size, offset):
    for i in range(size):
        row_label = tk.Label(root, text=str(size - i), font=('Times New Roman', 10))
        row_label.place(x=offset // 2, y=i * cell_size + offset + cell_size // 4)

        col_label = tk.Label(root, text=str(i + 1), font=('Times New Roman', 10))
        col_label.place(x=i * cell_size + offset + cell_size // 3, y=offset // 4)

        row_label_mirror = tk.Label(root, text=str(size - i), font=('Times New Roman', 10))
        row_label_mirror.place(x=size * cell_size + offset + offset // 3, y=i * cell_size + offset + cell_size // 4)

        col_label_mirror = tk.Label(root, text=str(i + 1), font=('Times New Roman', 10))
        col_label_mirror.place(x=i * cell_size + offset + cell_size // 3, y=size * cell_size + offset + offset // 4)
