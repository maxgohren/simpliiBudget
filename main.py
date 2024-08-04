import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import os

# Define the CSV path
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'SIMPLII.csv')
if not os.path.isfile(csv_path):
    print("File not found")
    sys.exit()

# Load and clean data
df = pd.read_csv(csv_path)
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')  # Convert to datetime
df['Month'] = df['Date'].dt.to_period('M')

# Define categories and keywords
categories = {
    'Money Management': ['Transfer Out', 'Transfer In'],
    'Gas': ['gas', 'gasoline', 'petrol', 'fuel'],
    'Food': ['Costco', 'Wal-Mart', 'Walmart', 'Zehrs', 'Loblaws', 'No Frills', 'dinner', 'restaurant', 'meal', 'grocery', 'supermarket'],
    'Credit': ['Visa'],
    'Payroll': ['Husky', 'payroll', 'evertz'],
    'Cash': ['ATM', 'ABM', 'Withdrawal'],
    'E-Transfer': ['E-Transfer'],
    'CONSOOOOM': ['pos', 'merchandise'],
    'Shopping': ['purchase', 'buy', 'shop', 'store', 'online'],
    'Entertainment': ['movie', 'concert', 'event', 'ticket', 'show'],
    'Healthcare': ['hair', 'pharmacy', 'doctor', 'medical', 'clinic', 'hospital'],
    'Education': ['tuition', 'school', 'course', 'education', 'training', 'loans'],
    'Travel': ['uber', 'taxi', 'flight', 'hotel', 'train', 'bus', 'travel'],
    'Dining': ['cafe', 'bistro', 'brunch', 'lunch', 'dining', 'kitchen'],
    'Transport': ['taxi', 'uber', 'ride', 'transport', 'car hire'],
    'Fitness': ['gym', 'yoga', 'exercise', 'workout', 'fitness'],
    'Utilities': ['koodo', 'electricity', 'water', 'internet', 'phone', 'utility'],
    'Other': []  # Default category if no match
}

# Function to categorize transactions
def categorize_transaction(detail):
    for category, keywords in categories.items():
        if any(keyword.lower() in detail.lower() for keyword in keywords):
            return category
    return 'Other'

# Apply the categorization function to the DataFrame
df['Category'] = df[' Transaction Details'].apply(categorize_transaction)
df.to_csv('SIMPLII_categorized.csv', index=False)

# Function to create pie chart for the selected month
def create_pie_chart(selected_month):
    filtered_df = df[(df['Month'] == selected_month) & (df['Category'] != 'Money Management')]
    category_totals = filtered_df.groupby('Category')[' Funds Out'].sum()
    categories = category_totals.index
    sizes = category_totals.values
    
    fig, ax = plt.subplots(figsize=(6, 4))  # Adjust size as needed
    ax.pie(sizes, labels=categories, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(categories))))
    ax.set_title(f'Transaction Distribution for {selected_month}')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    return fig

# Function to update data in the text widget
def update_data(event):
    selected_month = month_var.get()
    filtered_df = df[df['Month'] == selected_month]
    filtered_df['Date'] = filtered_df['Date'].dt.strftime('%d/%m')
    
    # Define column widths
    column_widths = [max(filtered_df[col].astype(str).apply(len).max(), len(col)) for col in filtered_df.columns]

    # Format text with left justification
    formatted_text = ""
    for col, width in zip(filtered_df.columns, column_widths):
        formatted_text += col.ljust(width) + " | "
    formatted_text += "\n" + "-" * (sum(column_widths) + len(column_widths) * 3) + "\n"
    
    for _, row in filtered_df.iterrows():
        for col, width in zip(filtered_df.columns, column_widths):
            formatted_text += str(row[col]).ljust(width) + " | "
        formatted_text += "\n"
    
    text.delete(1.0, tk.END)  # Clear previous text
    if filtered_df.empty:
        text.insert(tk.END, "No data available for the selected month.")
    else:
        text.insert(tk.END, formatted_text)
    
    total_value = filtered_df[' Funds Out'].sum()
    total_label.config(text=f"Total Transactions: ${total_value}")

    # Update pie chart
    fig = create_pie_chart(selected_month)
    for widget in chart_frame.winfo_children():
        widget.destroy()  # Remove old pie chart
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def close_window(event=None):
    root.destroy()
    sys.exit()

# Create the main application window
root = tk.Tk()
root.geometry("1000x1000")
root.title("SIMPLII Budget")

# Create label to display selected data
label = tk.Label(root, text="Select a month to view transactions from")
label.pack()

# Create a dropdown menu for selecting month
month_var = tk.StringVar()
month_dropdown = ttk.Combobox(root, textvariable=month_var)
month_dropdown['values'] = df['Month'].unique().tolist()
month_dropdown.bind('<<ComboboxSelected>>', update_data)
month_dropdown.set(df['Month'].iloc[0])
month_dropdown.pack()

# Transactions Window
text = tk.Text(root, height=20, width=100)
text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

# Total Window
total_label = tk.Label(root, text="Total Transactions: $0")
total_label.pack(padx=5, pady=5)

# Chart Frame
chart_frame = tk.Frame(root)
chart_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

# Bind Esc key to close window
root.bind('<Escape>', close_window)

# Run the Tkinter event loop
root.mainloop()
