import tkinter as tk
from datetime import datetime
from tkinter import filedialog


class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking App")
        self.root.configure(bg="black")

        # Cash input
        self.cash_label = tk.Label(root, text="Cash Amount:", bg="black", fg="white")
        self.cash_label.pack()
        self.cash_entry = tk.Entry(root)
        self.cash_entry.pack()

        # Reason input
        self.reason_label = tk.Label(root, text="Reason:", bg="black", fg="white")
        self.reason_label.pack()
        self.reason_entry = tk.Entry(root)
        self.reason_entry.pack()

        # Deposit and Withdraw buttons
        self.deposit_button = tk.Button(root, text="Deposit", command=self.deposit, bg="green", fg="white")
        self.deposit_button.pack(side=tk.LEFT, padx=10)
        self.withdraw_button = tk.Button(root, text="Withdraw", command=self.withdraw, bg="red", fg="white")
        self.withdraw_button.pack(side=tk.RIGHT, padx=10)

        # Display current cash
        self.current_cash_label = tk.Label(root, text="Current Cash: $0.00", font=("Arial", 14), bg="black", fg="white")
        self.current_cash_label.pack(pady=5)

        # Display transactions
        self.transaction_display = tk.Text(root, wrap=tk.WORD, bg="black", fg="white")
        self.transaction_display.pack(pady=10)

        # Transaction data
        self.transactions = []

        # Load existing transactions from file on startup
        self.load_transactions()

        # Save button
        self.save_button = tk.Button(root, text="Save Current Transactions", command=self.save_current_transactions, bg="blue", fg="white")
        self.save_button.pack(pady=10)

        # Reset button
        self.reset_button = tk.Button(root, text="Reset All", command=self.reset_transactions, bg="orange", fg="black")
        self.reset_button.pack(pady=10, anchor='s')  # 'w' stands for west (left)


    def deposit(self):
        amount = float(self.cash_entry.get())
        reason = self.reason_entry.get()
        self.update_transactions(amount, "Deposit", reason)

    def withdraw(self):
        amount = float(self.cash_entry.get())
        reason = self.reason_entry.get()
        self.update_transactions(-amount, "Withdraw", reason)

    def update_transactions(self, amount, reason_type, reason):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = {"amount": amount, "date": timestamp, "reason_type": reason_type, "reason": reason}
        self.transactions.append(transaction)

        # Save transactions to file
        self.save_transactions()

        # Update display
        current_cash = sum(transaction['amount'] for transaction in self.transactions)
        self.display_transactions(current_cash)

    def display_transactions(self, current_cash):
        self.transaction_display.delete(1.0, tk.END)

        for i, transaction in enumerate(self.transactions):
            transaction_text = f"{transaction['date']} - {transaction['reason_type']} ({transaction['reason']}): {transaction['amount']}"

            # Add a Delete button for each transaction
            delete_button = tk.Button(self.root, text="Delete", command=lambda idx=i: self.delete_transaction(idx), bg="orange", fg="black")
            self.transaction_display.window_create(tk.END, window=delete_button)
            self.transaction_display.insert(tk.END, f"{transaction_text}\n")

        # Update the display to ensure it's updated before retrieving dimensions
        self.transaction_display.update_idletasks()

        # Adjust the height of the text widget based on the number of lines
        self.transaction_display.config(height=int(self.transaction_display.get("1.0", "end-1c").count("\n") * 2))

        # Calculate the maximum line length and set the width accordingly
        max_line_length = max(len(line) for line in self.transaction_display.get("1.0", "end-1c").split('\n'))
        self.transaction_display.config(width=int(max_line_length*1.2))

        # Update current cash label
        self.current_cash_label.config(text=f"Current Cash: ${current_cash:.2f}")

    def delete_transaction(self, index):
        deleted_transaction = self.transactions.pop(index)

        # Subtract the original amount from the current cash
        current_cash = sum(transaction['amount'] for transaction in self.transactions)

        # Save transactions to file
        self.save_transactions()

        # Update display
        self.display_transactions(current_cash)

    def save_current_transactions(self):
    # Allow the user to choose the file location and name
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            # Save current transactions to the specified file
            with open(file_path, "w") as file:
                for transaction in self.transactions:
                    file.write(f"{transaction['date']} - {transaction['reason_type']} ({transaction['reason']}): {transaction['amount']}\n")

            # Create a new file for future transactions
            self.transactions = []
            self.save_transactions()

            # Update display
            self.display_transactions(0)

    def reset_transactions(self):
        # Reset transactions and update display
        self.transactions = []
        self.save_transactions()
        self.display_transactions(0)

    def save_transactions(self):
        with open("transactions.txt", "w") as file:
            for transaction in self.transactions:
                file.write(f"{transaction['date']} - {transaction['reason_type']} ({transaction['reason']}): {transaction['amount']}\n")

    def load_transactions(self):
        try:
            with open("transactions.txt", "r") as file:
                for line in file:
                    # Split the line into components
                    components = line.strip().split(" - ")
                    date, rest = components[0], components[1]

                    # Split the rest of the line to get reason_type, reason, and amount
                    rest_components = rest.split("): ")
                    reason_info, amount = rest_components[0], rest_components[1]

                    # Extract reason_type and reason
                    reason_components = reason_info.split(" (")
                    reason_type, reason = reason_components[0], reason_components[1]

                    # Convert the amount back to a float
                    amount = float(amount)

                    # Create a dictionary and append to transactions
                    transaction = {"date": date, "reason_type": reason_type, "reason": reason, "amount": amount}
                    self.transactions.append(transaction)

            current_cash = sum(transaction['amount'] for transaction in self.transactions)
            self.display_transactions(current_cash)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()