import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # API configuration
        self.api_key = "YOUR_API_KEY"  # Замените на ваш ключ
        self.base_url = "https://v6.exchangerate-api.com/v6"
        
        # Available currencies
        self.currencies = ["USD", "EUR", "GBP", "JPY", "CNY", "RUB", "CAD", "AUD", 
                          "CHF", "INR", "MXN", "BRL", "KRW", "TRY", "ZAR"]
        
        # Load history
        self.history_file = "history.json"
        self.history = self.load_history()
        
        # Setup UI
        self.setup_ui()
        self.update_history_table()
    
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="Currency Converter", font=("Arial", 20, "bold"))
        title.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20)
        
        # From currency
        tk.Label(main_frame, text="From:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.from_currency = ttk.Combobox(main_frame, values=self.currencies, width=15, font=("Arial", 12))
        self.from_currency.grid(row=0, column=1, padx=10, pady=5)
        self.from_currency.set("USD")
        
        # To currency
        tk.Label(main_frame, text="To:", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.to_currency = ttk.Combobox(main_frame, values=self.currencies, width=15, font=("Arial", 12))
        self.to_currency.grid(row=0, column=3, padx=10, pady=5)
        self.to_currency.set("EUR")
        
        # Amount input
        tk.Label(main_frame, text="Amount:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.amount_entry = tk.Entry(main_frame, width=20, font=("Arial", 12))
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Convert button
        self.convert_btn = tk.Button(main_frame, text="Convert", command=self.convert_currency, 
                                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15)
        self.convert_btn.grid(row=1, column=2, columnspan=2, pady=10)
        
        # Result label
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 14, "bold"), fg="#2196F3")
        self.result_label.grid(row=2, column=0, columnspan=4, pady=10)
        
        # History section
        history_frame = tk.LabelFrame(self.root, text="Conversion History", font=("Arial", 12, "bold"))
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Treeview for history
        columns = ("Date", "From", "To", "Amount", "Result")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        
        # Define headings
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons for history management
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.load_btn = tk.Button(button_frame, text="Load History", command=self.load_history_from_file,
                                  bg="#FF9800", fg="white", font=("Arial", 10))
        self.load_btn.pack(side="left", padx=5)
        
        self.clear_btn = tk.Button(button_frame, text="Clear History", command=self.clear_history,
                                   bg="#F44336", fg="white", font=("Arial", 10))
        self.clear_btn.pack(side="left", padx=5)
    
    def validate_amount(self, amount_str):
        """Validate if amount is a positive number"""
        try:
            amount = float(amount_str)
            if amount <= 0:
                return False, "Amount must be positive"
            return True, amount
        except ValueError:
            return False, "Please enter a valid number"
    
    def convert_currency(self):
        """Perform currency conversion using API"""
        amount_str = self.amount_entry.get().strip()
        
        # Validate amount
        is_valid, result = self.validate_amount(amount_str)
        if not is_valid:
            messagebox.showerror("Input Error", result)
            return
        
        amount = result
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        
        # Validate currency selection
        if not from_curr or not to_curr:
            messagebox.showerror("Error", "Please select currencies")
            return
        
        # Make API request
        try:
            url = f"{self.base_url}/{self.api_key}/pair/{from_curr}/{to_curr}/{amount}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data["result"] == "success":
                converted_amount = data["conversion_result"]
                rate = data["conversion_rate"]
                
                # Display result
                result_text = f"{amount:.2f} {from_curr} = {converted_amount:.2f} {to_curr} (Rate: {rate:.4f})"
                self.result_label.config(text=result_text)
                
                # Save to history
                self.save_to_history(from_curr, to_curr, amount, converted_amount, rate)
            else:
                messagebox.showerror("API Error", "Failed to get exchange rate")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Failed to connect to API: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def save_to_history(self, from_curr, to_curr, amount, result, rate):
        """Save conversion to history"""
        history_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "from_currency": from_curr,
            "to_currency": to_curr,
            "amount": amount,
            "result": result,
            "rate": rate
        }
        
        self.history.append(history_entry)
        self.save_history()
        self.update_history_table()
    
    def save_history(self):
        """Save history to JSON file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save history: {str(e)}")
    
    def load_history(self):
        """Load history from JSON file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def load_history_from_file(self):
        """Manually load history from file"""
        self.history = self.load_history()
        self.update_history_table()
        messagebox.showinfo("Success", "History loaded successfully")
    
    def clear_history(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            self.history = []
            self.save_history()
            self.update_history_table()
            messagebox.showinfo("Success", "History cleared")
    
    def update_history_table(self):
        """Update the history table display"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add history entries
        for entry in reversed(self.history):  # Show newest first
            self.history_tree.insert("", "end", values=(
                entry["date"],
                entry["from_currency"],
                entry["to_currency"],
                f"{entry['amount']:.2f}",
                f"{entry['result']:.2f}"
            ))

def main():
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
