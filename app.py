import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Import DateEntry widget from tkcalendar
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["student_management"]
students_col = db["students"]

# Declare global variables for entry fields
id_entry = None
name_entry = None
father_name_entry = None
mother_name_entry = None
highest_qualification_entry = None
dob_entry = None
address_entry = None
email_entry = None
mobile_entry = None
student_list = None

def add_student():
    global id_entry, name_entry, father_name_entry, mother_name_entry, highest_qualification_entry, dob_entry, address_entry, email_entry, mobile_entry
    student_id = id_entry.get()
    name = name_entry.get()
    father_name = father_name_entry.get()
    mother_name = mother_name_entry.get()
    highest_qualification = highest_qualification_entry.get()
    dob = dob_entry.get_date()  # For DateEntry widget, use get_date() instead of get()
    address = address_entry.get()
    email = email_entry.get()
    mobile = mobile_entry.get()
    
    if student_id and name and father_name and mother_name and highest_qualification and dob and address and email and mobile:
        student_data = {
            "_id": student_id,
            "name": name,
            "father_name": father_name,
            "mother_name": mother_name,
            "highest_qualification": highest_qualification,
            "dob": dob,
            "address": address,
            "email": email,
            "mobile": mobile
        }
        students_col.insert_one(student_data)
        messagebox.showinfo("Success", "Student added successfully.")
        clear_entries()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def clear_entries():
    global id_entry, name_entry, father_name_entry, mother_name_entry, highest_qualification_entry, dob_entry, address_entry, email_entry, mobile_entry
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    father_name_entry.delete(0, tk.END)
    mother_name_entry.delete(0, tk.END)
    highest_qualification_entry.delete(0, tk.END)
    dob_entry.set_date(None)  # Clear DateEntry widget
    address_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    mobile_entry.delete(0, tk.END)

def view_students():
    students = students_col.find()
    student_list.delete(0, tk.END)  # Clear previous entries
    for student in students:
        student_info = f"ID: {student.get('_id', '')}, Name: {student.get('name', '')}, Father's Name: {student.get('father_name', '')}, Mother's Name: {student.get('mother_name', '')}, Highest Qualification: {student.get('highest_qualification', '')}, DOB: {student.get('dob', '')}, Address: {student.get('address', '')}, Email: {student.get('email', '')}, Mobile: {student.get('mobile', '')}"
        student_list.insert(tk.END, student_info)

def update_student():
    global id_entry, name_entry
    student_id = id_entry.get()
    new_name = name_entry.get()
    if student_id and new_name:
        result = students_col.update_one({"_id": student_id}, {"$set": {"name": new_name}})
        if result.modified_count > 0:
            messagebox.showinfo("Success", "Student updated successfully.")
        else:
            messagebox.showwarning("Update Failed", "No changes made or student not found.")
        clear_entries()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def delete_student():
    student_id = id_entry.get()
    if student_id:
        result = students_col.delete_one({"_id": student_id})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Student deleted successfully.")
            clear_entries()
        else:
            messagebox.showerror("Error", "Student not found.")
    else:
        messagebox.showerror("Error", "Please fill in the student ID.")

def main():
    global id_entry, name_entry, father_name_entry, mother_name_entry, highest_qualification_entry, dob_entry, address_entry, email_entry, mobile_entry, student_list
    root = tk.Tk()
    root.title("Student Management System")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TEntry", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))

    label_frame = ttk.Frame(root, padding="20")
    label_frame.grid(row=0, column=0, columnspan=2)

    id_label = ttk.Label(label_frame, text="Student ID:")
    id_label.grid(row=0, column=0, sticky="e")
    id_entry = ttk.Entry(label_frame) 
    id_entry.grid(row=0, column=1)

    name_label = ttk.Label(label_frame, text="Student Name:")
    name_label.grid(row=1, column=0, sticky="e")
    name_entry = ttk.Entry(label_frame)
    name_entry.grid(row=1, column=1)

    father_name_label = ttk.Label(label_frame, text="Father's Name:")
    father_name_label.grid(row=2, column=0, sticky="e")
    father_name_entry = ttk.Entry(label_frame)
    father_name_entry.grid(row=2, column=1)

    mother_name_label = ttk.Label(label_frame, text="Mother's Name:")
    mother_name_label.grid(row=3, column=0, sticky="e")
    mother_name_entry = ttk.Entry(label_frame)
    mother_name_entry.grid(row=3, column=1)

    highest_qualification_label = ttk.Label(label_frame, text="Highest Qualification:")
    highest_qualification_label.grid(row=4, column=0, sticky="e")
    highest_qualification_entry = ttk.Entry(label_frame)
    highest_qualification_entry.grid(row=4, column=1)

    dob_label = ttk.Label(label_frame, text="Date of Birth (DOB):")
    dob_label.grid(row=5, column=0, sticky="e")
    dob_entry = DateEntry(label_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    dob_entry.grid(row=5, column=1)

    address_label = ttk.Label(label_frame, text="Address:")
    address_label.grid(row=6, column=0, sticky="e")
    address_entry = ttk.Entry(label_frame)
    address_entry.grid(row=6, column=1)

    email_label = ttk.Label(label_frame, text="Email:")
    email_label.grid(row=7, column=0, sticky="e")
    email_entry = ttk.Entry(label_frame)
    email_entry.grid(row=7, column=1)

    mobile_label = ttk.Label(label_frame, text="Mobile Number:")
    mobile_label.grid(row=8, column=0, sticky="e")
    mobile_entry = ttk.Entry(label_frame)
    mobile_entry.grid(row=8, column=1)

    button_frame = ttk.Frame(root, padding="20")
    button_frame.grid(row=1, column=0, columnspan=2)
    add_button = ttk.Button(button_frame, text="Add Student", command=add_student)
    add_button.grid(row=0, column=0)

    view_button = ttk.Button(button_frame, text="View All Students", command=view_students)
    view_button.grid(row=0, column=1)

    update_button = ttk.Button(button_frame, text="Update Student", command=update_student)
    update_button.grid(row=0, column=2)

    delete_button = ttk.Button(button_frame, text="Delete Student", command=delete_student)
    delete_button.grid(row=0, column=3)

    student_list_frame = ttk.Frame(root, padding="20")
    student_list_frame.grid(row=2, column=0, columnspan=2)

    student_list_label = ttk.Label(student_list_frame, text="All Students:")
    student_list_label.grid(row=0, column=0, columnspan=2)

    student_list = tk.Listbox(student_list_frame, width=100)  # Increased width for better visibility
    student_list.grid(row=1, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()
