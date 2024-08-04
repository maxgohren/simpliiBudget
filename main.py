import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

df = pd.read_csv('C:\\Users\\Creeper Gang\\Desktop\\simpliibudget\\SIMPLII.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y') # Convert to datetime
df['Month'] = df['Date'].dt.to_period('M')

# Define categories and keywords
categories = {
    'Gas': ['gas', 'gasoline', 'petrol', 'fuel'],
    'Food': ['dinner', 'restaurant', 'meal', 'grocery', 'supermarket'],
    'Shopping': ['purchase', 'buy', 'shop', 'store', 'online'],
    'Entertainment': ['movie', 'concert', 'event', 'ticket', 'show'],
    'Healthcare': ['pharmacy', 'doctor', 'medical', 'clinic', 'hospital'],
    'Utilities': ['electricity', 'water', 'internet', 'phone', 'utility'],
    'Travel': ['flight', 'hotel', 'train', 'bus', 'travel'],
    'Dining': ['cafe', 'bistro', 'brunch', 'lunch', 'dining'],
    'Transport': ['taxi', 'uber', 'ride', 'transport', 'car hire'],
    'Fitness': ['gym', 'yoga', 'exercise', 'workout', 'fitness'],
    'Education': ['tuition', 'school', 'course', 'education', 'training'],
    'Subscription': ['monthly fee', 'subscription', 'membership', 'renewal'],
    'Other': []  # Default category if no match
}

# Function to categorize transactions
def categorize_transaction(detail):
    for category, keywords in categories.items():
        if any(keyword.lower() in detail.lower() for keyword in keywords):
            return category
    return 'Other'

# Apply the categorization function to the DataFrame
df['Category'] = df['Transaction Details'].apply(categorize_transaction)

# Overwrite Data
df.to_csv('SIMPLII.csv', index=False)

class DataFilterApp:
    def __init__(self,root):
        self.root = root
        self.root.title("See Transactions Based On Month")

        # Create label to display selected data
        self.label = tk.Label(root, text="Select a month to view transactions from")
        self.label.pack()

        # Create a dropdown menu for selecting month
        self.month_var = tk.StringVar()
        print(f"{self.month_var}")
        self.month_dropdown  = ttk.Combobox(root, textvariable=self.month_var)
        self.month_dropdown['values'] = df['Month'].unique().tolist()
        self.month_dropdown.bind('<<ComboboxSelected>>', self.update_data)
        self.month_dropdown.set(df['Month'].iloc[0])
        self.month_dropdown.pack()

        # Transactions Window
        self.text = tk.Text(root, height=10, width=50)
        self.text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        # Total Window
        self.total_label = tk.Label(root, text="Total Transactions: $0")
        self.total_label.pack(padx=5, pady=5)
         # Create a frame for the matplotlib figure
        self.figure_frame = tk.Frame(root)
        self.figure_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    def update_data(self, event):
        selected_month = self.month_var.get()
        filtered_df = df[df['Month'] == selected_month]

        filtered_df['Date'] = filtered_df['Date'].dt.strftime('%d/%m')

        print(f"Selected Month: {selected_month}")
        print(f"Filtered DataFrame:\n{filtered_df}")
        self.text.delete(1.0, tk.END) # Clear previous text
        if filtered_df.empty:
            self.text.insert(tk.END, "No data available for the selected month.")
        else:
            self.text.insert(tk.END, filtered_df.to_string(index=False))
        
        total_value = filtered_df[' Funds Out'].sum()
        self.total_label.config(text=f"Total Transactions: ${total_value}")

        # Plot cumulative line chart
        self.plot_cumulative_chart(filtered_df)

    def plot_cumulative_chart(self, filtered_df):
        for widget in self.figure_frame.winfo_children():
            widget.destroy()

        filtered_df['Cumulative'] = filtered_df[' Funds Out'].cumsum()

        fig, ax = plt.subplots()
        ax.plot(filtered_df['Date'], filtered_df['Cumulative'], marker='o')
        ax.set_title("Cumulative Transactions")
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Value")

        canvas = FigureCanvasTkAgg(fig, master=self.figure_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        

# Run the Tkinter event loop
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x1000")
    root.title("SIMPLII Budget")
    app = DataFilterApp(root)
    root.mainloop()
