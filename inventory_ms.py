import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk  # Import ttk for Combobox
import json

class InventoryManagementSystemGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("700x500")

        # Load or initialize inventory
        self.inventory = self.load_inventory()

        # GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Add Item Section
        add_item_frame = tk.LabelFrame(self, text="Add/Update Item", padx=10, pady=10)
        add_item_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(add_item_frame, text="Item Name:").pack(side=tk.LEFT)
        self.item_name_entry = tk.Entry(add_item_frame)
        self.item_name_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(add_item_frame, text="Quantity:").pack(side=tk.LEFT)
        self.quantity_entry = tk.Entry(add_item_frame, width=5)
        self.quantity_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(add_item_frame, text="Price:").pack(side=tk.LEFT)
        self.price_entry = tk.Entry(add_item_frame, width=5)
        self.price_entry.pack(side=tk.LEFT, padx=5)

        add_item_button = tk.Button(add_item_frame, text="Add/Update Item", command=self.add_update_item)
        add_item_button.pack(side=tk.LEFT, padx=10)

        # Restock Alert Section
        restock_alert_frame = tk.LabelFrame(self, text="Set Restock Alert", padx=10, pady=10)
        restock_alert_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(restock_alert_frame, text="Item Name:").pack(side=tk.LEFT)
        self.alert_item_name_combobox = ttk.Combobox(restock_alert_frame, values=list(self.inventory.keys()))
        self.alert_item_name_combobox.pack(side=tk.LEFT, padx=5)

        tk.Label(restock_alert_frame, text="Threshold:").pack(side=tk.LEFT)
        self.threshold_entry = tk.Entry(restock_alert_frame, width=5)
        self.threshold_entry.pack(side=tk.LEFT, padx=5)

        set_alert_button = tk.Button(restock_alert_frame, text="Set Alert", command=self.set_restock_alert)
        set_alert_button.pack(side=tk.LEFT, padx=10)

        # Display Area
        self.display_area = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD)
        self.display_area.pack(padx=10, pady=5, fill="both", expand=True)

        # Buttons Frame for Reports and Checks
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(fill="x")

        self.report_button = tk.Button(buttons_frame, text="Generate Report", command=self.generate_report)
        self.report_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.check_inventory_button = tk.Button(buttons_frame, text="Check Inventory", command=self.check_inventory)
        self.check_inventory_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.restock_check_button = tk.Button(buttons_frame, text="Inventory that needs Restocking", command=self.check_restock)
        self.restock_check_button.pack(side=tk.LEFT, padx=10, pady=10)

    def add_update_item(self):
        item_name = self.item_name_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
            if item_name:
                self.inventory[item_name] = {'quantity': quantity, 'price': price}
                self.display_area.insert(tk.END, f"Item '{item_name}' added/updated successfully.\n")
                # Update Combobox values
                self.alert_item_name_combobox['values'] = list(self.inventory.keys())
            else:
                messagebox.showerror("Error", "Item name cannot be empty.")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price. Please enter valid numbers.")
        finally:
            self.item_name_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)

    def set_restock_alert(self):
        item_name = self.alert_item_name_combobox.get()
        try:
            threshold = int(self.threshold_entry.get())
            if item_name and item_name in self.inventory and threshold >= 0:
                self.inventory[item_name]['restock_threshold'] = threshold
                self.display_area.insert(tk.END, f"Restock alert set for '{item_name}' at threshold {threshold} units.\n")
            else:
                messagebox.showerror("Error", "Invalid item name or threshold.")
        except ValueError:
            messagebox.showerror("Error", "Invalid threshold. Please enter a valid number.")
        finally:
            self.threshold_entry.delete(0, tk.END)

    def check_inventory(self):
        self.display_area.delete('1.0', tk.END)
        for item, details in self.inventory.items():
            self.display_area.insert(tk.END, f"{item}: {details['quantity']} units\n")

    def generate_report(self):
        self.display_area.delete('1.0', tk.END)
        total_value = 0
        for item, details in self.inventory.items():
            item_value = details['quantity'] * details['price']
            self.display_area.insert(tk.END, f"{item}: {details['quantity']} units at ${details['price']}/unit. Total: ${item_value}\n")
            total_value += item_value
        self.display_area.insert(tk.END, f"Total inventory value: ${total_value}\n")

    def check_restock(self):
        self.display_area.delete('1.0', tk.END)
        for item, details in self.inventory.items():
            if 'restock_threshold' in details and details['quantity'] <= details['restock_threshold']:
                self.display_area.insert(tk.END, f"{item}: {details['quantity']} units, below restock threshold of {details['restock_threshold']} units. Consider restocking.\n")

    def load_inventory(self):
        try:
            with open('inventory.json', 'r') as f:
                inventory = json.load(f)
            return inventory
        except FileNotFoundError:
            return {}

    def on_closing(self):
        with open('inventory.json', 'w') as f:
            json.dump(self.inventory, f)
        self.destroy()

if __name__ == "__main__":
    app = InventoryManagementSystemGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
