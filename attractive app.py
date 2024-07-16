import tkinter as tk
from tkinter import messagebox

class ExpenseSharingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Sharing App")

        # Center the window on the screen
        window_width = 500
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        
        self.expenses = []

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg='#f0f0f0')
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Expense input frame
        input_frame = tk.LabelFrame(main_frame, text="Add New Expense", padx=10, pady=10, bg='#d9d9d9', font=('Arial', 12, 'bold'))
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(input_frame, text="Expense Description:", bg='#d9d9d9').grid(row=0, column=0, sticky="e")
        self.desc_entry = tk.Entry(input_frame)
        self.desc_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(input_frame, text="Amount:", bg='#d9d9d9').grid(row=1, column=0, sticky="e")
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(input_frame, text="Paid By:", bg='#d9d9d9').grid(row=2, column=0, sticky="e")
        self.paid_by_entry = tk.Entry(input_frame)
        self.paid_by_entry.grid(row=2, column=1, sticky="ew")

        tk.Label(input_frame, text="Shared With (comma-separated):", bg='#d9d9d9').grid(row=3, column=0, sticky="e")
        self.shared_with_entry = tk.Entry(input_frame)
        self.shared_with_entry.grid(row=3, column=1, sticky="ew")

        tk.Button(input_frame, text="Add Expense", command=self.add_expense, bg='#4CAF50', fg='white').grid(row=4, column=0, columnspan=2, pady=5)

        # Expense list frame
        expense_list_frame = tk.LabelFrame(main_frame, text="Expenses", padx=10, pady=10, bg='#d9d9d9', font=('Arial', 12, 'bold'))
        expense_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.expenses_listbox = tk.Listbox(expense_list_frame, selectmode=tk.SINGLE)
        self.expenses_listbox.grid(row=0, column=0, sticky="nsew")
        self.expenses_listbox.bind('<Delete>', self.remove_expense)
        
        tk.Button(expense_list_frame, text="Remove Selected", command=self.remove_expense, bg='#f44336', fg='white').grid(row=1, column=0, pady=5)

        # Balance frame
        balance_frame = tk.LabelFrame(main_frame, text="Balances", padx=10, pady=10, bg='#d9d9d9', font=('Arial', 12, 'bold'))
        balance_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        tk.Button(balance_frame, text="Calculate Balances", command=self.calculate_balances, bg='#2196F3', fg='white').grid(row=0, column=0, pady=5)

        self.balances_listbox = tk.Listbox(balance_frame)
        self.balances_listbox.grid(row=1, column=0, sticky="nsew")

    def add_expense(self):
        desc = self.desc_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return
        paid_by = self.paid_by_entry.get().strip()
        shared_with = [name.strip() for name in self.shared_with_entry.get().split(',')]

        if not desc or not paid_by or not shared_with:
            messagebox.showerror("Error", "All fields are required")
            return

        if paid_by in shared_with:
            messagebox.showerror("Error", "Paid by person cannot be in shared with list")
            return

        expense = {
            "desc": desc,
            "amount": amount,
            "paid_by": paid_by,
            "shared_with": shared_with
        }

        self.expenses.append(expense)
        self.update_expenses_listbox()

        # Clear input fields
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.paid_by_entry.delete(0, tk.END)
        self.shared_with_entry.delete(0, tk.END)

    def update_expenses_listbox(self):
        self.expenses_listbox.delete(0, tk.END)
        for expense in self.expenses:
            self.expenses_listbox.insert(tk.END, f"{expense['desc']}: {expense['amount']} paid by {expense['paid_by']} shared with {', '.join(expense['shared_with'])}")

    def remove_expense(self, event=None):
        selected_idx = self.expenses_listbox.curselection()
        if not selected_idx:
            return

        idx = selected_idx[0]
        del self.expenses[idx]
        self.update_expenses_listbox()

    def calculate_balances(self):
        balances = {}
        for expense in self.expenses:
            amount_per_person = expense['amount'] / (len(expense['shared_with']) + 1)

            if expense['paid_by'] not in balances:
                balances[expense['paid_by']] = 0
            balances[expense['paid_by']] += expense['amount'] - amount_per_person

            for person in expense['shared_with']:
                if person not in balances:
                    balances[person] = 0
                balances[person] -= amount_per_person

        self.balances_listbox.delete(0, tk.END)
        
        for person in balances:
            balances[person] = round(balances[person], 2)

        for person, balance in balances.items():
            if balance > 0:
                self.balances_listbox.insert(tk.END, f"{person} is owed: {balance:.2f}")
            else:
                self.balances_listbox.insert(tk.END, f"{person} owes: {-balance:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseSharingApp(root)
    root.mainloop()
