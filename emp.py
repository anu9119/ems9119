import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook
from PIL import Image, ImageTk  # Requires pillow library for image handling
import os

# Main application window
root = tk.Tk()
root.title("Northern Railway - Travelling Allowance Journal")
root.geometry("1000x1000")

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Admin Login Frame
login_frame = tk.Frame(root)
login_frame.grid(row=0, column=0, sticky="nsew")

# Home Frame
home_frame = tk.Frame(root)
home_frame.grid(row=0, column=0, sticky="nsew")

# Top Section Frame
top_section_frame = tk.Frame(root)
top_section_frame.grid(row=0, column=0, sticky="nsew")

# Table Section Frame
table_section_frame = tk.Frame(root)
table_section_frame.grid(row=0, column=0, sticky="nsew")

# Certification Section Frame
certification_section_frame = tk.Frame(root)
certification_section_frame.grid(row=0, column=0, sticky="nsew")

# --- Admin Login Page ---
def login():
    if username_entry.get() == "sarvesh9119" and password_entry.get() == "sarvesh@9119":  # Simple check for demo
        show_frame(home_frame)
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

login_label = tk.Label(login_frame, text="Admin Login", font=("Arial", 18, "bold"))
login_label.pack(pady=20)

tk.Label(login_frame, text="Username", font=("Arial", 12)).pack()
username_entry = tk.Entry(login_frame, width=30)
username_entry.pack(pady=5)

tk.Label(login_frame, text="Password", font=("Arial", 12)).pack()
password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=login, font=("Arial", 12, "bold"), bg="blue", fg="white")
login_button.pack(pady=20)

# --- Home Frame with Logo ---
home_label = tk.Label(home_frame, text="Northern Railway - Travelling Allowance Journal", font=("Arial", 20, "bold"), fg="red")
home_label.pack(pady=20)

# Load and display Indian Railway logo
try:
    logo_image = Image.open("indian_railway_logo.png")
    logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(home_frame, image=logo_photo)
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)
except Exception as e:
    print("Error loading logo:", e)

# Navigation buttons
buttons = [
    ("Top Section", lambda: show_frame(top_section_frame)),
    ("Table Section", lambda: show_frame(table_section_frame)),
    ("Certification Section", lambda: show_frame(certification_section_frame)),
]

for text, command in buttons:
    btn = tk.Button(home_frame, text=text, command=command, font=("Arial", 12, "bold"), width=20, pady=5)
    btn.pack(pady=10)

# --- Top Section ---

def submit_data():
    print("Top Section data submitted.")

tk.Label(top_section_frame, text="Main Page", font=("Arial", 14, "bold")).pack(pady=10)

labels = ["Dept.", "PF NO.", "BILL UNIT NO.", "Headquarters", "Journal of duties performed by:", 
          "Designation", "Pay in Level", "of 7th CPC", "Date of Appointment", "Rules by which governed"]

entries_top = {}

frame_top = tk.Frame(top_section_frame)
frame_top.pack(pady=10, padx=10, fill="x")

for i, text in enumerate(labels):
    tk.Label(frame_top, text=text, font=("Arial", 10)).grid(row=i, column=0, sticky="w")
    entry = tk.Entry(frame_top, width=30)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entries_top[text] = entry

tk.Button(top_section_frame, text="Submit", command=submit_data, font=("Arial", 12, "bold"), bg="green", fg="white").pack(pady=10)
tk.Button(top_section_frame, text="Back to Home", command=lambda: show_frame(home_frame), font=("Arial", 12, "bold")).pack()

# --- Table Section (Scrollable) ---

table_headers = ["Month & Date", "Employee Name", "Train no.", "Time left", "Time arrived", "Station (from)", 
                 "Station (to)", "Kilometer", "Day/Night", "Object of Journey", "Rate (Rs.)", "Rate (P.)"]

table_entries = []

def add_row():
    row_entries = []
    for j in range(len(table_headers)):
        entry = tk.Entry(table_inner_frame, width=12)
        entry.grid(row=len(table_entries) + 1, column=j, pady=2)
        row_entries.append(entry)
    table_entries.append(row_entries)

def delete_row():
    if len(table_entries) > 1:
        row = table_entries.pop()
        for entry in row:
            entry.grid_forget()
    else:
        messagebox.showwarning("Warning", "At least one row is required.")

def save_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.append(table_headers)
    for row_entries in table_entries:
        row_data = [entry.get() for entry in row_entries]
        ws.append(row_data)
    save_path = os.path.join(os.getcwd(), "TravelAllowanceData.xlsx")
    wb.save(save_path)
    messagebox.showinfo("Save to Excel", f"Data saved successfully to {save_path}")

def print_form():
    for row_entries in table_entries:
        employee_data = [entry.get() for entry in row_entries]
        print("Employee Data:", employee_data)
    messagebox.showinfo("Print", "Printed form for each employee.")

tk.Label(table_section_frame, text="Table Section", font=("Arial", 14, "bold")).pack(pady=10)

table_frame = tk.Frame(table_section_frame)
table_frame.pack(pady=10, padx=10, fill="both", expand=True)

canvas = tk.Canvas(table_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

table_inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=table_inner_frame, anchor="nw")

table_inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

for j, header in enumerate(table_headers):
    tk.Label(table_inner_frame, text=header, borderwidth=1, relief="solid", width=12, font=("Arial", 10, "bold")).grid(row=0, column=j)

add_row()  # Start with one row of entries

row_control_frame = tk.Frame(table_section_frame)
row_control_frame.pack(pady=5)

tk.Button(row_control_frame, text="Add Row", command=add_row, font=("Arial", 10, "bold"), bg="green", fg="white").grid(row=0, column=0, padx=5)
tk.Button(row_control_frame, text="Delete Row", command=delete_row, font=("Arial", 10, "bold"), bg="red", fg="white").grid(row=0, column=1, padx=5)
tk.Button(row_control_frame, text="Save to Excel", command=save_to_excel, font=("Arial", 10, "bold"), bg="purple", fg="white").grid(row=0, column=2, padx=5)
tk.Button(row_control_frame, text="Print Table", command=print_form, font=("Arial", 10, "bold"), bg="blue", fg="white").grid(row=0, column=3, padx=5)

tk.Button(table_section_frame, text="Back to Home", command=lambda: show_frame(home_frame), font=("Arial", 12, "bold")).pack()

# --- Certification Section ---

certification_texts = [
    "The T.A claimed by me has not been claimed before and will not be claimed hereafter.",
    "Conveyance charges claimed have actually been spent by me and according to local municipal rates.",
    "Cheapest mode of conveyance was utilized.",
    "The journey performed by road for which conveyance has been claimed was over 1.6 km."
]

def submit_certification():
    for entry in certification_entries:
        print(entry.get())
    messagebox.showinfo("Certification", "Certification details submitted.")

tk.Label(certification_section_frame, text="Certification ", font=("Arial", 18, "bold")).pack(pady=10)

certification_frame = tk.Frame(certification_section_frame)
certification_frame.pack(pady=10, padx=10, fill="x")

certification_entries = []
for text in certification_texts:
    tk.Label(certification_frame, text=text, wraplength=700, justify="left", font=("Arial", 10)).pack(anchor="w", pady=2)
    entry = tk.Entry(certification_frame, width=70)
    entry.pack(pady=2)
    certification_entries.append(entry)

tk.Button(certification_section_frame, text="Submit Certification", command=submit_certification, font=("Arial", 18, "bold"), bg="green", fg="white").pack(pady=10)

signature_frame = tk.Frame(certification_section_frame)
signature_frame.pack(pady=10, padx=10, fill="x")

tk.Label(signature_frame, text="Signature of Officer Claiming T.A.", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
signature_entry_officer = tk.Entry(signature_frame, width=30)
signature_entry_officer.grid(row=0, column=1, padx=5)

tk.Label(signature_frame, text="Signature of Head of the Office", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
signature_entry_head = tk.Entry(signature_frame, width=30)
signature_entry_head.grid(row=1, column=1, padx=5)

tk.Button(certification_section_frame, text="Back to Home", command=lambda: show_frame(home_frame), font=("Arial", 12, "bold")).pack()

# Show Login Frame initially
show_frame(login_frame)
root.mainloop()
