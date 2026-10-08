import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# ================== USERS DATA ==================
users = {"kayl": "12345"}  # default admin
sales_data = []

# Product list with prices and stock
products_info = {
    "Processors (Intel/AMD)": {"price": 26000, "stock": 10, "image": r"C:\Users\kayl\Desktop\kemjs images\processor.jpg"},
    "Motherboards": {"price": 6150, "stock": 15, "image": r"C:\Users\kayl\Desktop\kemjs images\motherboard.jpg"},
    "RAM Modules": {"price": 3400, "stock": 20, "image": r"C:\Users\kayl\Desktop\kemjs images\ram modules.jpg"},
    "Storage Drives": {"price": 4250, "stock": 12, "image": r"C:\Users\kayl\Desktop\kemjs images\storage drive.jpg"},
    "Graphics Cards": {"price": 8500, "stock": 8, "image": r"C:\Users\kayl\Desktop\kemjs images\graphic card.jpg"},
    "Power Supply Units": {"price": 4200, "stock": 18, "image": r"C:\Users\kayl\Desktop\kemjs images\powersupply.jpg"},
    "Monitors": {"price": 9600, "stock": 10, "image": r"C:\Users\kayl\Desktop\kemjs images\monitor.jpg"},
}

# ================== SCROLLABLE FRAME HELPER ==================
def make_scrollable(parent, bg="#ffffff"):
    canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=bg)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return scroll_frame

# ================== MAIN WINDOW ==================
def show_main_window(username):
    root = tk.Tk()
    root.title("KEMJS - Computer Sales and Services")
    root.state("zoomed")
    root.config(bg="#1b1b1b")

    # =============== STYLES ===============
    TITLE_FONT = ("Segoe UI", 28, "bold")
    HEADER_FONT = ("Segoe UI", 22, "bold")
    TEXT_FONT = ("Segoe UI", 15)
    BUTTON_FONT = ("Segoe UI", 14, "bold")

    # Left Navigation
    nav_frame = tk.Frame(root, bg="#0d7377", width=240)
    nav_frame.pack(side="left", fill="y")

    # Main content
    content_frame = tk.Frame(root, bg="#eeeeee")
    content_frame.pack(side="right", fill="both", expand=True)

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    # =============== PURCHASE FORM ===============
    def open_purchase_form(product_name):
        product = products_info[product_name]
        form = tk.Toplevel(root)
        form.title(f"Purchase: {product_name}")
        form.geometry("460x640")
        form.config(bg="#f5f5f5")

        tk.Label(form, text="🛒 PURCHASE FORM", font=HEADER_FONT, fg="#0d7377", bg="#f5f5f5").pack(pady=15)
        tk.Label(form, text=f"{product_name}", font=("Segoe UI", 16, "bold"), fg="#212121", bg="#f5f5f5").pack()
        tk.Label(form, text=f"Price: ₱{product['price']}", font=TEXT_FONT, bg="#f5f5f5").pack()

        # Customer fields
        def add_field(label):
            tk.Label(form, text=label, font=("Segoe UI", 13, "bold"), fg="#333", bg="#f5f5f5").pack(anchor="w", padx=25, pady=(10, 0))
            entry = tk.Entry(form, width=40, font=("Segoe UI", 13))
            entry.pack(padx=25)
            return entry

        name_entry = add_field("Full Name:")
        address_entry = add_field("Delivery Address:")

        tk.Label(form, text="Quantity:", font=("Segoe UI", 13, "bold"), bg="#f5f5f5").pack(anchor="w", padx=25, pady=(10, 0))
        qty_spin = tk.Spinbox(form, from_=1, to=product["stock"], width=5, font=("Segoe UI", 13))
        qty_spin.pack(padx=25, anchor="w")

        tk.Label(form, text="Payment Method:", font=("Segoe UI", 13, "bold"), bg="#f5f5f5").pack(anchor="w", padx=25, pady=(10, 0))
        payment_var = tk.StringVar(value="Gcash")
        tk.OptionMenu(form, payment_var, "Gcash", "Cash on Delivery", "Bank Transfer").pack(padx=25)

        def confirm_purchase():
            name, address = name_entry.get(), address_entry.get()
            qty = int(qty_spin.get())
            if not name or not address:
                return messagebox.showwarning("Incomplete", "Please fill in all required fields.")
            if qty > product["stock"]:
                return messagebox.showerror("Stock Error", "Not enough stock available.")

            total = qty * product["price"]
            product["stock"] -= qty
            sales_data.append([product_name, qty, total])

            messagebox.showinfo("Order Confirmed", f"Thank you, {name}!\n\n✔ {qty}x {product_name}\n✔ Total: ₱{total}\n✔ Payment: {payment_var.get()}")
            form.destroy()

        tk.Button(form, text="Confirm Purchase", command=confirm_purchase,
                  bg="#0d7377", fg="white", font=BUTTON_FONT, relief="flat", padx=15, pady=5).pack(pady=25)

    # =============== HOME TAB ===============
    def show_home():
        clear_content()
        home_frame = tk.Frame(content_frame, bg="#eeeeee")
        home_frame.pack(expand=True)

        try:
            logo_path = r"C:\Users\kayl\Desktop\kemjs images\logo.png"
            logo_img = Image.open(logo_path).resize((500, 350))
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(home_frame, image=logo_photo, bg="#eeeeee")
            logo_label.image = logo_photo
            logo_label.pack(pady=20)
        except:
            tk.Label(home_frame, text="[Logo Here]", font=("Segoe UI", 22, "bold"), bg="#eeeeee", fg="#444").pack(pady=20)

        tk.Label(home_frame, text='"Sulbad sa Problema, Serbisyo nga Kasaligan\n i-KEMJS na yan!!"',
                 font=("Segoe UI", 20, "italic"), fg="#393e46", bg="#eeeeee").pack(pady=25)

    # =============== PRODUCTS TAB ===============
    def show_products():
        clear_content()
        title = tk.Label(content_frame, text="📦 PRODUCTS", font=TITLE_FONT, fg="#0d7377", bg="#eeeeee")
        title.pack(pady=20)

        scroll_frame = make_scrollable(content_frame, bg="#eeeeee")
        grid_frame = tk.Frame(scroll_frame, bg="#eeeeee")
        grid_frame.pack(pady=10)

        columns = 3
        for index, (name, info) in enumerate(products_info.items()):
            row, col = index // columns, index % columns
            frame = tk.Frame(grid_frame, bg="white", padx=15, pady=15, relief="raised", bd=3)
            frame.grid(row=row, column=col, padx=25, pady=25, sticky="nsew")

            try:
                img = Image.open(info["image"]).resize((180, 140))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=photo, bg="white")
                img_label.image = photo
                img_label.pack(pady=5, anchor="center")
            except:
                tk.Label(frame, text="No Image", bg="#ccc", width=25, height=8).pack(anchor="center")

            tk.Label(frame, text=f"{name}", font=("Segoe UI", 16, "bold"), fg="#0d7377", bg="white").pack(pady=(10, 0), anchor="center")
            tk.Label(frame, text=f"₱{info['price']}", font=("Segoe UI", 15, "bold"), bg="white", fg="#333").pack(anchor="center")
            tk.Label(frame, text=f"Stock: {info['stock']}", font=("Segoe UI", 14), fg="#444", bg="white").pack(anchor="center")

            tk.Button(frame, text="Purchase", command=lambda n=name: open_purchase_form(n),
                      bg="#32e0c4", fg="black", font=("Segoe UI", 13, "bold"), relief="flat", padx=12, pady=4).pack(pady=8, anchor="center")

        grid_frame.grid_columnconfigure((0, 1, 2), weight=1)

    # =============== SERVICES TAB ===============
    def show_services():
        clear_content()
        scroll_frame = make_scrollable(content_frame, bg="#ffffff")

        tk.Label(scroll_frame, text="🛠 OUR SERVICES", font=("Segoe UI", 30, "bold"), fg="#0d7377", bg="#ffffff").pack(pady=25)

        services = [
            "Virus Removal and System Cleaning",
            "Laptop and Desktop Repair",
            "Photocopying and Document Printing",
            "Home Wi-Fi Installation",
            "Network Troubleshooting",
            "Printer and Scanner Repair"
        ]
        for s in services:
            tk.Label(scroll_frame, text=s, font=("Segoe UI", 18, "underline"), bg="#ffffff", fg="#222").pack(pady=6, anchor="center")

        tk.Label(scroll_frame, text="📞 Contact Information:", bg="#ffffff", font=("Segoe UI", 18, "bold")).pack(pady=(35, 10))
        tk.Label(scroll_frame, text="📍 Location: Purok1A, Panadtalan, Maramag Bukidnon", bg="#ffffff", font=("Segoe UI", 16)).pack(pady=3)
        tk.Label(scroll_frame, text="📱 Contact Number: 12345678910", bg="#ffffff", font=("Segoe UI", 16)).pack(pady=3)
        tk.Label(scroll_frame, text="📧 Email: kemjs@gmail.com", bg="#ffffff", font=("Segoe UI", 16)).pack(pady=3)
        tk.Label(scroll_frame, text="Thank you for choosing KEMJS!", font=("Segoe UI", 16, "italic"), bg="#ffffff", fg="#00695c").pack(pady=20)

    # =============== SALES TAB ===============
    def show_sales():
        clear_content()
        tk.Label(content_frame, text="💰 SALES MONITORING", font=TITLE_FONT, fg="#0d7377", bg="#eeeeee").pack(pady=20)

        sales_frame = tk.Frame(content_frame, bg="#eeeeee")
        sales_frame.pack(expand=True)

        cols = ("Product", "Quantity", "Total Sales")
        tree = ttk.Treeview(sales_frame, columns=cols, show="headings", height=15)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 16, "bold"), foreground="#0d7377")
        style.configure("Treeview", font=("Segoe UI", 15), rowheight=34)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=280, anchor="center")
        tree.pack(pady=20, expand=True)

        for record in sales_data:
            tree.insert("", "end", values=record)

        total_sales = sum(r[2] for r in sales_data)
        tk.Label(sales_frame, text=f"📊 Total Sales: ₱{total_sales}",
                 font=("Segoe UI", 22, "bold"), bg="#eeeeee", fg="#222831").pack(pady=25)

    # =============== MANAGE USERS TAB (Admin Only) ===============
    def show_manage_users():
        clear_content()
        tk.Label(content_frame, text="👤 MANAGE USERS", font=TITLE_FONT, fg="#0d7377", bg="#eeeeee").pack(pady=20)

        frame = tk.Frame(content_frame, bg="#eeeeee")
        frame.pack(expand=True)

        cols = ("Username", "Password")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 14, "bold"), foreground="#0d7377")
        style.configure("Treeview", font=("Segoe UI", 13), rowheight=30)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=260, anchor="center")
        tree.pack(pady=20)

        for u, p in users.items():
            tree.insert("", "end", values=(u, p))

    # =============== NAV BUTTONS ===============
    buttons = [
        ("🏠 Home", show_home),
        ("📦 Products", show_products),
        ("🛠 Services", show_services),
        ("💰 Sales", show_sales),
    ]
    if username == "kayl":  # admin only
        buttons.append(("👤 Manage Users", show_manage_users))

    for text, cmd in buttons:
        tk.Button(nav_frame, text=text, command=cmd, font=("Segoe UI", 14, "bold"),
                  bg="#0d7377", fg="white", activebackground="#32e0c4",
                  activeforeground="black", relief="flat", padx=15, pady=8).pack(fill="x", pady=8, padx=15)

    show_home()
    root.mainloop()

# ================== LOGIN WINDOW ==================
def show_login():
    login_window = tk.Tk()
    login_window.title("Login - KEMJS")
    login_window.state("zoomed")
    login_window.config(bg="#eeeeee")

    frame = tk.Frame(login_window, bg="#f5f5f5", padx=40, pady=40)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="🔑 LOGIN", font=("Segoe UI", 28, "bold"), fg="#0d7377", bg="#f5f5f5").pack(pady=20)
    tk.Label(frame, text="Username:", font=("Segoe UI", 14), bg="#f5f5f5").pack()
    username_entry = tk.Entry(frame, font=("Segoe UI", 14)); username_entry.pack(pady=8)

    tk.Label(frame, text="Password:", font=("Segoe UI", 14), bg="#f5f5f5").pack()
    password_entry = tk.Entry(frame, show="*", font=("Segoe UI", 14)); password_entry.pack(pady=8)

    def attempt_login():
        u, p = username_entry.get(), password_entry.get()
        if u in users and users[u] == p:
            login_window.destroy()
            show_main_window(u)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_register():
        reg_win = tk.Toplevel(login_window)
        reg_win.title("Register New User")
        reg_win.geometry("400x300")
        reg_win.config(bg="#f5f5f5")

        tk.Label(reg_win, text="Register", font=("Segoe UI", 20, "bold"), fg="#0d7377", bg="#f5f5f5").pack(pady=15)
        tk.Label(reg_win, text="Username:", font=("Segoe UI", 13), bg="#f5f5f5").pack()
        new_user = tk.Entry(reg_win, font=("Segoe UI", 13)); new_user.pack(pady=6)
        tk.Label(reg_win, text="Password:", font=("Segoe UI", 13), bg="#f5f5f5").pack()
        new_pass = tk.Entry(reg_win, font=("Segoe UI", 13), show="*"); new_pass.pack(pady=6)

        def save_new_user():
            u, p = new_user.get(), new_pass.get()
            if not u or not p: return messagebox.showwarning("Error","Fill all fields")
            if u in users: return messagebox.showerror("Error","User exists")
            users[u]=p; messagebox.showinfo("Success",f"User {u} registered"); reg_win.destroy()

        tk.Button(reg_win, text="Register", command=save_new_user, bg="#0d7377", fg="white",
                  font=("Segoe UI", 13, "bold"), relief="flat", padx=12, pady=5).pack(pady=20)

    tk.Button(frame, text="Login", command=attempt_login,
              bg="#0d7377", fg="white", font=("Segoe UI", 16, "bold"),
              relief="flat", padx=15, pady=5).pack(pady=15)
    tk.Button(frame, text="Register", command=open_register,
              bg="#32e0c4", fg="black", font=("Segoe UI", 14, "bold"),
              relief="flat", padx=10, pady=5).pack()

    login_window.mainloop()

show_login()
