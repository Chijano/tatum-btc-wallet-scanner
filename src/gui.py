import tkinter as tk
from tkinter import scrolledtext
from src.app import analyze_wallet_activity


def run_gui():
    window = tk.Tk()
    window.title("Tatum Wallet Analyzer")
    window.geometry("750x550")

    # Input label
    label = tk.Label(window, text="Enter BTC Testnet Address:", font=("Segoe UI", 11))
    label.pack(pady=10)

    # Input field
    address_entry = tk.Entry(window, width=60, font=("Consolas", 11))
    address_entry.pack(pady=5)

    # Output box
    output_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Consolas", 11))
    output_box.pack(expand=True, fill="both", padx=10, pady=10)

    def analyze():
        address = address_entry.get().strip()
        if not address:
            output_box.configure(state="normal")
            output_box.delete(1.0, tk.END)
            output_box.insert(tk.END, "Please enter a BTC testnet address.")
            output_box.configure(state="disabled")
            return

        result = analyze_wallet_activity(address)

        output_box.configure(state="normal")
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, result)
        output_box.configure(state="disabled")

    # Analyze button
    analyze_button = tk.Button(window, text="Analyze", font=("Segoe UI", 11), command=analyze)
    analyze_button.pack(pady=10)

    window.mainloop()


if __name__ == "__main__":
    run_gui()
