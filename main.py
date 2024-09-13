import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label
from PIL import Image, ImageTk
import webbrowser

# Function to establish a connection to MySQL database
def connect():
    try:
        conn = mysql.connector.connect(host='localhost', database='crime_management_system', user='xyz', password='xyz@123' )
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)
        messagebox.showerror("Error", "Failed to connect to database")

# Function to verify login credentials
def verify_login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "admin" and password == "admin@123":
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_window():
    global conn
    global crime_tree  
    global update_id_entry  
    global new_status_entry  

    main_window = tk.Tk()
    main_window.title("Crime Management System")
    main_window.configure(bg='#313131')

    # Hover functions
    def on_enter(e):
        e.widget['background'] = '#27496d'
        e.widget['relief'] = 'raised'

    def on_leave(e):
        e.widget['background'] = '#206ca4'
        e.widget['relief'] = 'flat'

    # Toggle between dark and light mode
    def toggle_theme():
        if main_window.cget('bg') == '#313131':  # Currently in dark mode
            main_window.configure(bg='#d3c5b0')  # Switch to earthy, darker light mode
            update_to_light_mode()
        else:                                    # Currently in light mode
            main_window.configure(bg='#313131')  # Switch back to dark mode
            update_to_dark_mode()

    def update_to_light_mode():
        for widget in main_window.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry):
                widget.configure(bg='#d3c5b0', fg='#4a3f35')  # Darker beige background, deep brown text
            if isinstance(widget, tk.Button):
                widget.configure(bg='#6b4226', fg='white')  # Deep brown buttons in light mode
        style.configure("Treeview", background="#bca68a", foreground="#4a3f35", fieldbackground="#bca68a")

    def update_to_dark_mode():
        for widget in main_window.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry):
                widget.configure(bg='#313131', fg='white')  # Dark mode with white text
            if isinstance(widget, tk.Button):
                widget.configure(bg='#206ca4', fg='white')  # Blue buttons in dark mode
        style.configure("Treeview", background="#313131", foreground="white", fieldbackground="#313131")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", background="#313131", foreground="#ffffff", fieldbackground="#313131", rowheight=25, font=('Arial', 10))
    style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
    style.configure("TButton", background="#206ca4", foreground="#ffffff", relief="flat", font=('Arial', 10))

    # Labels and entries for crime input
    labels = ["Crime Type:", "Date Reported (YYYY-MM-DD):", "Description:", "Location ID:"]
    for i, label_text in enumerate(labels):
        label = tk.Label(main_window, text=label_text, bg='#313131', fg='white')
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(main_window, bg='#40444b', fg='white', insertbackground='white')
        entry.grid(row=i, column=1, padx=10, pady=5)

        if label_text == "Crime Type:":
            global crime_type_entry
            crime_type_entry = entry
        elif label_text == "Date Reported (YYYY-MM-DD):":
            global date_reported_entry
            date_reported_entry = entry
        elif label_text == "Description:":
            global description_entry
            description_entry = entry
        else:
            global location_id_entry
            location_id_entry = entry

    # Buttons for crime actions
    buttons = [("Add Crime", add_crime), ("Update Status", open_update_status_window), ("Delete Crime", delete_crime_gui), ("View All Crimes", view_crimes), ("Wanted Criminals", open_wanted_criminals), ("Victims & Witness Inquiries", open_inquiries_form)]
    for i, (text, command) in enumerate(buttons):
        button = tk.Button(main_window, text=text, command=command, width=20, bg='#206ca4', fg='white', relief='flat', font=('Arial', 10))
        button.grid(row=i+6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        button.bind("<Enter>", on_enter)  # Bind hover enter
        button.bind("<Leave>", on_leave)  # Bind hover leave

    # Treeview to display crime records
    crime_tree = ttk.Treeview(main_window, columns=('No.', 'CrimeID', 'CrimeType', 'DateReported', 'Status', 'Description', 'LocationID'), show='headings')
    crime_tree.heading('No.', text='No.')
    crime_tree.heading('CrimeID', text='CrimeID')
    crime_tree.heading('CrimeType', text='CrimeType')
    crime_tree.heading('DateReported', text='DateReported')
    crime_tree.heading('Status', text='Status')
    crime_tree.heading('Description', text='Description')
    crime_tree.heading('LocationID', text='LocationID')

    crime_tree.column('No.', width=50, anchor='center')
    crime_tree.column('CrimeID', width=80, anchor='center')
    crime_tree.column('CrimeType', width=150, anchor='center')
    crime_tree.column('DateReported', width=120, anchor='center')
    crime_tree.column('Status', width=80, anchor='center')
    crime_tree.column('Description', width=250, anchor='center')
    crime_tree.column('LocationID', width=80, anchor='center')

    crime_tree.grid(row=0, column=2, rowspan=12, padx=10, pady=10, sticky="nsew")

    # Scrollbar for treeview
    tree_scroll = ttk.Scrollbar(main_window, orient='vertical', command=crime_tree.yview)
    tree_scroll.grid(row=0, column=3, rowspan=12, sticky='ns')
    crime_tree.configure(yscrollcommand=tree_scroll.set)

    # Add toggle theme button
    theme_button = tk.Button(main_window, text="Toggle Dark Mode", command=toggle_theme, width=20, bg='#206ca4', fg='white', relief='flat', font=('Arial', 10))
    theme_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    theme_button.bind("<Enter>", on_enter)
    theme_button.bind("<Leave>", on_leave)

    conn = connect()
    main_window.mainloop()

# Function to open the update status window
def open_update_status_window():
    update_status_window = tk.Toplevel()
    update_status_window.title("Update Crime Status")
    update_status_window.geometry("400x200")
    update_status_window.configure(bg='#242424')

    id_label = tk.Label(update_status_window, text="Crime ID:", bg='#242424', fg='white')
    id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    global update_id_entry
    update_id_entry = tk.Entry(update_status_window, bg='#40444b', fg='white', insertbackground='white')
    update_id_entry.grid(row=0, column=1, padx=10, pady=5)

    new_status_label = tk.Label(update_status_window, text="New Status (Open/Closed):", bg='#242424', fg='white')
    new_status_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    global new_status_entry
    new_status_entry = tk.Entry(update_status_window, bg='#40444b', fg='white', insertbackground='white')
    new_status_entry.grid(row=1, column=1, padx=10, pady=5)

    update_button = tk.Button(update_status_window, text="Update", command=update_status, width=15, bg='#206ca4', fg='white', relief='flat', font=('Arial', 10))
    update_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

def update_status():
    crime_id = int(update_id_entry.get())
    new_status = new_status_entry.get()
    update_crime_status(conn, crime_id, new_status)
    view_crimes()

def open_wanted_criminals():
    wanted_window = tk.Toplevel()
    wanted_window.title("Wanted Criminals")
    wanted_window.geometry("400x525")
    wanted_window.configure(bg='#242424')

    tk.Label(wanted_window, text="FBI Top 10 Wanted Criminals List", bg='#242424', fg='white').pack(pady=20)

    # Dictionary of criminals and their image paths
    criminals = {
        "abc": "name1.png",
        "xyz": "name2.png",
    }

    # Function to display the poster in a new window
    def show_poster(criminal_name, poster_link):
        poster_window = tk.Toplevel(wanted_window)
        poster_window.title(f"Wanted Poster - {criminal_name}")
        poster_window.configure(bg='#242424')

        img = Image.open(poster_link)
        img = img.resize((350, 500), Image.LANCZOS)
        poster_img = ImageTk.PhotoImage(img)

        poster_label = tk.Label(poster_window, image=poster_img, bg='#242424')
        poster_label.image = poster_img
        poster_label.pack(padx=10, pady=10)

    # Create a button for each wanted criminal
    for name, poster_link in criminals.items():
        btn = tk.Button(wanted_window, text=name, command=lambda n=name, p=poster_link: show_poster(n, p), bg='#206ca4', fg='white', relief='flat', font=('Arial', 10))
        btn.pack(padx=10, pady=10, fill='x')

    wanted_window.mainloop()

def add_crime():
    crime_type = crime_type_entry.get()
    date_reported = date_reported_entry.get()
    description = description_entry.get()
    location_id = int(location_id_entry.get())
    insert_crime(conn, crime_type, date_reported, description, location_id)
    view_crimes()

def open_update_crime_window():
    update_window = tk.Toplevel()
    update_window.title("Update Crime")
    update_window.geometry("400x00")
    update_window.configure(bg='#242424')

    id_label = tk.Label(update_window, text="Crime ID:", bg='#242424', fg='white')
    id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    id_entry = tk.Entry(update_window, bg='#40444b', fg='white', insertbackground='white')
    id_entry.grid(row=0, column=1, padx=10, pady=5)
    
    new_type_label = tk.Label(update_window, text="New Crime Type:", bg='#242424', fg='white')
    new_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    new_type_entry = tk.Entry(update_window, bg='#40444b', fg='white', insertbackground='white')
    new_type_entry.grid(row=1, column=1, padx=10, pady=5)
    
    new_date_label = tk.Label(update_window, text="New Date Reported (YYYY-MM-DD):", bg='#242424', fg='white')
    new_date_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    new_date_entry = tk.Entry(update_window, bg='#40444b', fg='white', insertbackground='white')
    new_date_entry.grid(row=2, column=1, padx=10, pady=5)
    
    new_description_label = tk.Label(update_window, text="New Description:", bg='#242424', fg='white')
    new_description_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    new_description_entry = tk.Entry(update_window, bg='#40444b', fg='white', insertbackground='white')
    new_description_entry.grid(row=3, column=1, padx=10, pady=5)

    update_button = tk.Button(update_window, text="Update", command=lambda: update_crime(update_window, id_entry.get(), new_type_entry.get(), new_date_entry.get(), new_description_entry.get()), width=15, bg='#206ca4', fg='white', relief='flat', font=('Arial', 10))
    update_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

def update_crime(update_window, crime_id, new_type, new_date, new_description):
    update_crime_details(conn, int(crime_id), new_type, new_date, new_description)
    update_window.destroy()
    view_crimes()

def open_inquiries_form():
    inquiries_window = tk.Toplevel()
    inquiries_window.title("Victims & Witness Inquiries")
    inquiries_window.geometry("400x200")
    inquiries_window.configure(bg='#242424')

    info_label = tk.Label(inquiries_window, text="Download and fill out the inquiry form:", bg='#242424', fg='white')
    info_label.pack(pady=10)

    download_button = tk.Button(inquiries_window, text="Download Inquiry Form", command=download_form, width=30, bg='#206ca4', fg='white', relief='flat', font=('Arial', 10))
    download_button.pack(pady=10)

    inquiries_window.mainloop()

def download_form():
    import webbrowser
    webbrowser.open("enhanced_witness_inquiry_form.pdf")

def submit_inquiry():
    messagebox.showinfo("Thank You", "Thank you for your input. Your inquiry has been submitted.")

def view_crimes():
    for row in crime_tree.get_children():
        crime_tree.delete(row)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crime")
    rows = cursor.fetchall()
    for idx, row in enumerate(rows):
        crime_tree.insert('', 'end', values=(idx+1, row[0], row[1], row[2], row[3], row[4], row[5]))

def delete_crime_gui():
    delete_window = tk.Toplevel()
    delete_window.title("Delete Crime")
    delete_window.geometry("300x150")
    delete_window.configure(bg='#242424')

    crime_id_label = tk.Label(delete_window, text="Crime ID:", bg='#242424', fg='white')
    crime_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    crime_id_entry = tk.Entry(delete_window, bg='#40444b', fg='white', insertbackground='white')
    crime_id_entry.grid(row=0, column=1, padx=10, pady=5)

    delete_button = tk.Button(delete_window, text="Delete", command=lambda: delete_crime(delete_window, crime_id_entry.get()), width=15, bg='#206ca4', fg='white', relief='flat', font=('Arial', 10))
    delete_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

def delete_crime(delete_window, crime_id):
    delete_crime_from_db(conn, int(crime_id))
    delete_window.destroy()
    view_crimes()

def insert_crime(conn, crime_type, date_reported, description, location_id):
    cursor = conn.cursor()
    query = "INSERT INTO crime (CrimeType, DateReported, Description, LocationID) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (crime_type, date_reported, description, location_id))
    conn.commit()

def update_crime_status(conn, crime_id, new_status):
    cursor = conn.cursor()
    query = "UPDATE crime SET Status = %s WHERE CrimeID = %s"
    cursor.execute(query, (new_status, crime_id))
    conn.commit()

def update_crime_details(conn, crime_id, new_type, new_date, new_description):
    cursor = conn.cursor()
    query = "UPDATE crime SET CrimeType = %s, DateReported = %s, Description = %s WHERE CrimeID = %s"
    cursor.execute(query, (new_type, new_date, new_description, crime_id))
    conn.commit()

def delete_crime_from_db(conn, crime_id):
    cursor = conn.cursor()
    query = "DELETE FROM crime WHERE CrimeID = %s"
    cursor.execute(query, (crime_id,))
    conn.commit()

def main():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x550")  
    login_window.configure(bg='#242424')

    image_path = 'detective-modified.png'
    logo_image = Image.open(image_path)

    logo_image = logo_image.resize((300, 300), Image.Resampling.LANCZOS)

    logo_image_tk = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(login_window, image=logo_image_tk, bg='#242424')
    logo_label.image = logo_image_tk
    logo_label.pack(pady=10)

    tk.Label(login_window, text="Username:", bg='#242424', fg='white').pack(pady=5)
    global username_entry
    username_entry = tk.Entry(login_window, bg='#40444b', fg='white', insertbackground='white')
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", bg='#242424', fg='white').pack(pady=5)
    global password_entry
    password_entry = tk.Entry(login_window, show='*', bg='#40444b', fg='white', insertbackground='white')
    password_entry.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", command=verify_login, width=15, bg='#206ca4', fg='white', relief='flat', font=('Arial', 10))
    login_button.pack(pady=20)

    login_window.mainloop()

if __name__ == "__main__":
    main()
