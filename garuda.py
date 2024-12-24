import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Function to calculate water sharing
def calculate_water_sharing(total_cost, flat_details):
    # Initialize result list
    results = []

    # Calculate total sharing units
    total_sharing_units = 0
    for flat in flat_details:
        permanent_adults = flat['Permanent Residents']['Adults']
        permanent_kids = flat['Permanent Residents']['Kids']
        guests = flat['Guests']

        total_sharing_units += permanent_adults + (0.5 * permanent_kids) + guests

    for flat in flat_details:
        flat_number = flat['Flat Number']
        permanent_adults = flat['Permanent Residents']['Adults']
        permanent_kids = flat['Permanent Residents']['Kids']
        guests = flat['Guests']

        # Calculate sharing units for the flat
        permanent_sharing = permanent_adults + (0.5 * permanent_kids)
        guest_sharing = guests
        total_sharing = permanent_sharing + guest_sharing

        # Calculate cost for the flat
        flat_cost = (total_cost / total_sharing_units) * total_sharing
        
        # Append to results
        results.append({
            "Flat Number": flat_number,
            "Cost (₹)": round(flat_cost, 2)
        })

    # Convert to DataFrame for better representation
    return pd.DataFrame(results)

# Function to enforce integer input
def validate_integer_input(P):
    if P == "" or P.isdigit():
        return True
    return False

# Function to handle form submission
def submit_details(event=None):  # Allow "Enter" key to trigger
    flat_details = []

    try:
        total_cost = float(total_cost_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount for the total cost.")
        return

    for i in range(len(flat_number_entries)):
        flat_number = flat_numbers[i]  # Keep flat numbers fixed
        permanent_adults = int(permanent_adult_entries[i].get() or 0)  # Default to 0 if empty
        permanent_kids = int(permanent_kid_entries[i].get() or 0)      # Default to 0 if empty
        guests = int(guest_entries[i].get() or 0)                     # Default to 0 if empty

        flat_details.append({
            "Flat Number": flat_number,
            "Permanent Residents": {
                "Adults": permanent_adults,
                "Kids": permanent_kids
            },
            "Guests": guests
        })

    sharing_df = calculate_water_sharing(total_cost, flat_details)

    # Create a new window for the results
    result_window = tk.Toplevel(root)
    result_window.title("Water Sharing Results")
    result_window.geometry("900x600")
    result_window.config(bg="#e6f7ff")

    # Header
    header_label = tk.Label(
        result_window,
        text="GARUDA NEST WATER SHARING",
        font=("Helvetica", 24, "bold"),
        bg="#0099cc",
        fg="white",
        padx=20,
        pady=10
    )
    header_label.pack(fill="x", pady=10)

    # Add copyright text
    copyright_label = tk.Label(
        result_window,
        text="© Tharun Naik",
        font=("Helvetica", 10),
        bg="#e6f7ff",
        fg="#555555"
    )
    copyright_label.pack(side="bottom", pady=10)

    # Display the result in a styled table
    result_frame = tk.Frame(result_window, bg="#e6f7ff", pady=20)
    result_frame.pack(fill="both", expand=True)

    cols = list(sharing_df.columns)
    style = ttk.Style()
    style.configure("Custom.Treeview", borderwidth=1, relief="solid", rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Helvetica", 12, "bold"), borderwidth=1, relief="solid")

    result_table = ttk.Treeview(result_frame, columns=cols, show='headings', height=20, style="Custom.Treeview")
    for col in cols:
        result_table.heading(col, text=col)
        result_table.column(col, anchor="center", width=150)

    for _, row in sharing_df.iterrows():
        result_table.insert("", "end", values=list(row))

    # Add the scrollbar
    scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_table.yview)
    result_table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the main UI window
root = tk.Tk()
root.title("Garuda Nest Water Sharing")
root.geometry("800x600")
root.state('zoomed')  # Open maximized
root.config(bg="#f0f4f7")  # Background color

# Header Label
header_label = tk.Label(root, text="Garuda Nest Water Sharing", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#2f4f4f")
header_label.pack(pady=20)

# Add copyright text to the top-right corner of the input screen
copyright_label_top = tk.Label(
    root,
    text="© Tharun Naik",
    font=("Helvetica", 10),
    bg="#f0f4f7",
    fg="#555555",
    anchor="e"
)
copyright_label_top.pack(fill="x", padx=10)

# Input Section
input_frame_top = tk.Frame(root, bg="#f0f4f7")
input_frame_top.pack(fill="x", pady=10)

cost_label = tk.Label(input_frame_top, text="Enter the total cost of water tanker for the month:", font=("Helvetica", 12), bg="#f0f4f7", anchor="w")
cost_label.pack(side="left", padx=10)

total_cost_entry = tk.Entry(input_frame_top, font=("Helvetica", 12), width=30, bd=2, relief="solid", justify="center")
total_cost_entry.pack(side="left", padx=10)

# Register validation for integer input
vcmd = root.register(validate_integer_input)

# Create Canvas and Scrollbar for Input Section
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a Frame inside the canvas for input fields
input_frame = tk.Frame(canvas, bg="#f0f4f7")
canvas.create_window((0, 0), window=input_frame, anchor="nw")

# Pack the canvas and scrollbar to ensure correct positioning
canvas.pack(pady=10, fill="both", expand=True, side="left")
scrollbar.pack(side="right", fill="y")

flat_number_entries = []
permanent_adult_entries = []
permanent_kid_entries = []
guest_entries = []

header = ["Flat Number", "Resident Adults", "Resident Kids (<5 years)", "Guests"]
for idx, text in enumerate(header):
    tk.Label(input_frame, text=text, font=("Helvetica", 12), bg="#f0f4f7", fg="#2f4f4f").grid(row=0, column=idx, padx=10, pady=10)

# Generate flat numbers in the series 001-004, 101-104, 201-204, 301-304, 401-404
flat_numbers = [f"{block}{flat:02}" for block in ["0", "1", "2", "3", "4"] for flat in range(1, 5)]

# Add the flat numbers dynamically to the form
for i, flat_number in enumerate(flat_numbers):
    # Auto-populate flat numbers
    flat_number_label = tk.Label(input_frame, text=flat_number, font=("Helvetica", 10), width=20, bd=2, relief="solid", justify="center", bg="#d9eaf7")
    flat_number_label.grid(row=i + 1, column=0, padx=10, pady=5)
    flat_number_entries.append(flat_number_label)

    permanent_adult_entry = tk.Entry(input_frame, font=("Helvetica", 10), width=20, bd=2, relief="solid", justify="center", validate="key", validatecommand=(vcmd, '%P'))
    permanent_adult_entry.grid(row=i + 1, column=1, padx=10, pady=5)
    permanent_adult_entries.append(permanent_adult_entry)

    permanent_kid_entry = tk.Entry(input_frame, font=("Helvetica", 10), width=20, bd=2, relief="solid", justify="center", validate="key", validatecommand=(vcmd, '%P'))
    permanent_kid_entry.grid(row=i + 1, column=2, padx=10, pady=5)
    permanent_kid_entries.append(permanent_kid_entry)

    guest_entry = tk.Entry(input_frame, font=("Helvetica", 10), width=20, bd=2, relief="solid", justify="center", validate="key", validatecommand=(vcmd, '%P'))
    guest_entry.grid(row=i + 1, column=3, padx=10, pady=5)
    guest_entries.append(guest_entry)

# Update scroll region to encompass the entire input frame
input_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Submit Button
submit_button = tk.Button(
    root,
    text="Calculate Sharing",
    command=submit_details,
    font=("Helvetica", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    relief="solid",
    width=20
)

# Align the button neatly at the bottom-right corner
submit_button.pack(side="bottom", pady=20)

# Bind the "Enter" key to trigger the submit function
root.bind('<Return>', submit_details)

# Start the main loop
root.mainloop()
