import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import os
from src.app import analyze_wallet_activity


def run_gui():
    window = tk.Tk()
    window.title("Tatum Wallet Analyzer")
    window.geometry("750x650")
    window.configure(bg="white")

    # Resolve absolute path to image
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_dir, "..", "assets", "wsb.jpg")

    # Load and resize image
    img = Image.open(img_path)
    img = img.resize((300, 200), Image.Resampling.LANCZOS)
    logo: ImageTk.PhotoImage = ImageTk.PhotoImage(img)

    # Display image
    logo_label = tk.Label(window, image=logo, bg="white")  # type: ignore[arg-type]
    logo_label.image = logo
    logo_label.pack(pady=10)

    # Input label
    label = tk.Label(window, text="Enter BTC Testnet Address:", font=("Segoe UI", 11), bg="white")
    label.pack(pady=10)

    # Input field
    address_entry = tk.Entry(window, width=60, font=("Consolas", 11))
    address_entry.pack(pady=5)

    # Output box
    output_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Consolas", 11))
    output_box.pack(expand=True, fill="both", padx=10, pady=10)

    # Red text tag
    output_box.tag_config("red", foreground="red")

    def analyze():
        address = address_entry.get().strip()
        output_box.configure(state="normal")
        output_box.delete(1.0, tk.END)

        if not address:
            output_box.insert(tk.END, "Please enter a BTC testnet address.")
            output_box.configure(state="disabled")
            return

        result = analyze_wallet_activity(address)

        for line in result.split("\n"):
            if line.startswith("Wallet value:"):
                output_box.insert(tk.END, line + "\n", "red")
            else:
                output_box.insert(tk.END, line + "\n")

        output_box.configure(state="disabled")

    # Button row (Analyze + Exit)
    button_row = tk.Frame(window, bg="white")
    button_row.pack(pady=10)

    analyze_button = tk.Button(button_row, text="Analyze", font=("Segoe UI", 11), command=analyze)
    analyze_button.pack(side="left", padx=10)

    exit_button = tk.Button(button_row, text="Exit", font=("Segoe UI", 11), command=window.destroy)
    exit_button.pack(side="left", padx=10)

    window.mainloop()


if __name__ == "__main__":
    run_gui()
