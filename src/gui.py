import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import os
from src.app import analyze_wallet_activity


class WalletAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tatum Wallet Analyzer")
        self.root.geometry("600x750")
        self.root.resizable(True, True)  # allow window resizing

        # Full white background
        self.root.configure(bg="white")

        # Load and display banner image (keep aspect ratio with max height)
        image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "wsb.jpg")
        img = Image.open(image_path)

        # Target width
        target_width = 580

        # Compute height based on aspect ratio
        w, h = img.size
        aspect_ratio = h / w
        target_height = int(target_width * aspect_ratio)

        # Limit height so GUI doesn't break
        max_height = 150
        if target_height > max_height:
            target_height = max_height
            target_width = int(target_height / aspect_ratio)

        # Resize without distortion
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        self.banner = ImageTk.PhotoImage(img)
        self.banner_label = tk.Label(root, image=self.banner, bg="white")  # type: ignore
        self.banner_label.pack(pady=10)

        # Address input
        tk.Label(root, text="Enter BTC Testnet Address:", bg="white").pack(pady=5)
        self.address_entry = tk.Entry(root, width=50, bg="white")
        self.address_entry.pack(pady=5)

        # API key input
        tk.Label(root, text="Enter Tatum API Key:", bg="white").pack(pady=5)
        self.api_key_entry = tk.Entry(root, width=50, show="*", bg="white")
        self.api_key_entry.pack(pady=5)

        # Block scan range
        tk.Label(root, text="Number of blocks to scan:", bg="white").pack(pady=5)
        self.scan_var = tk.IntVar(value=1)
        self.scan_spin = ttk.Spinbox(root, from_=1, to=50, textvariable=self.scan_var, width=5)
        self.scan_spin.pack(pady=5)

        # Output box
        self.output = scrolledtext.ScrolledText(root, width=70, height=18, bg="white")
        self.output.pack(pady=10, expand=True, fill="both")

        # Buttons
        button_frame = tk.Frame(root, bg="white")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Analyze", command=self.analyze, width=12).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Exit", command=root.quit, width=12).grid(row=0, column=1, padx=10)

    def analyze(self):
        address = self.address_entry.get().strip()
        api_key = self.api_key_entry.get().strip()
        scan_range = self.scan_var.get()

        if not address:
            self.output.insert(tk.END, "Please enter an address.\n")
            return

        if not api_key:
            self.output.insert(tk.END, "Please enter your Tatum API key.\n")
            return

        self.output.delete(1.0, tk.END)

        # >>> NEW: Print address + block range at top of output <<<
        self.output.insert(tk.END, f"Scanning address: {address}\n")
        self.output.insert(tk.END, f"Blocks to scan: {scan_range}\n\n")

        try:
            result = analyze_wallet_activity(address, scan_range, api_key)
            self.output.insert(tk.END, result)
        except Exception as e:
            self.output.insert(tk.END, f"Unexpected error: {e}\n")


def main():
    root = tk.Tk()
    WalletAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
