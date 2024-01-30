import tkinter as tk
from tkinter import ttk
import win32com.client, openpyxl

def show_options():
    frame3.place(x=x_position, y=y_position)

def show_scrollbar():
    label_search = tk.Label(frame, text="Search for instrument:",font=("Arial", 20))
    label_search.grid(row=0, column=0, sticky="ns")
    scrollbar.grid(row=2, column=1, sticky="ns")
    listbox.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")
    entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    frame2.place(x=x_position*3.2, y=y_position)

def on_combobox_selected(event):
        selected_option = view_var.get()
        if selected_option == "Scrollbar":
            show_scrollbar()
            checkbox.grid_forget()
            frame3.place_forget()
        elif selected_option == "Choose":
            show_options()
            scrollbar.grid_forget()
            listbox.grid_forget()
            label_choose.grid_forget()

def on_click_im(is_importer):
    is_importer.set(True)
    label_choose.config(text="Choose models:")
    btn_im.grid_forget()
    btn_eks.grid_forget()
    show_scrollbar()

def on_click_eks(is_importer):
    is_importer.set(False)
    label_choose.config(text="Choose models:")
    btn_im.grid_forget()
    btn_eks.grid_forget()
    show_scrollbar()

def instructions():
    pass # blured

# uploading selected options and buying side to excel, starting macro
# macro in excel generates powerpoint presentation
def generate(selected_options, is_importer):
    file_path = ""
    side = is_importer.get()
    excel_app = win32com.client.Dispatch("Excel.Application")
    excel_app.Visible = False  
    # writing selected options to excel
    workbook = excel_app.Workbooks.Open(file_path)
    sheet = workbook.Sheets(1)
    for i, option in enumerate(selected_options):
        sheet.Cells(i + 1, 1).Value = option
    # running macro 1 or macro 2
    if side == True:
        excel_app.Run("Module1.macro1") 
    if side == False:
        excel_app.Run("Module1.macro2") 
    workbook.Close(SaveChanges=False)
    excel_app.Quit()

def do_frame2():
    global frame2, view_var
    frame2 = ttk.Frame(root, width=200, height=400)
    label_view = tk.Label(frame2, text="Which View:", font=("Arial", 20), 
                                background="#606060", foreground="white")
    label_which_view = tk.Label(frame2, text="Which View:")
    label_which_view.grid(row=0, column=0, sticky="w")
    view_options = ["Scrollbar", "Choose"]
    view_var = tk.StringVar(value=view_options[0])
    view_dropdown = ttk.Combobox(frame2, values=view_options, textvariable=view_var, state="readonly")
    view_dropdown.grid(row=1, column=0, padx=10)
    view_dropdown.bind("<<ComboboxSelected>>", on_combobox_selected)
    label_choose_options = tk.Label(frame2, text="Choose from options:")
    label_choose_options.grid(row=2, column=0, sticky="w", pady=(10, 0))
    choose_options = ["All", "Collar", "Forward", "Option"]
    choose_var = tk.StringVar(value=choose_options[0])
    choose_dropdown = ttk.Combobox(frame2, values=choose_options, textvariable=choose_var, state="readonly")
    choose_dropdown.grid(row=3, column=0, padx=10)
    confirm1 = tk.Button(frame2, text="Confirm", command=confirm1_selection, font=("Arial", 14))
    confirm1.grid(row=4, column=0, padx=10, pady=10)

def confirm1_selection():
    global selected_options
    selected_option = view_var.get()
    if selected_option == "Choose": selected_options = [options[i] for i, var in enumerate(checkbox_vars) if var.get()]
    if selected_option == "Scrollbar":
        selected_indices = listbox.curselection()
        selected_options = [listbox.get(index) for index in selected_indices]
    generate(selected_options, is_importer)

def on_search(entry_text):
    filtered_options = [option for option in options if entry_text.lower() in option.lower()]
    update_listbox(filtered_options)

def update_listbox(filtered_options):
    listbox.delete(0, tk.END)
    for i, option in enumerate(filtered_options):
        background_color = "#E8F7DF" if i % 2 == 0 else "white"
        listbox.insert(tk.END, option)
        listbox.itemconfig(i, {'bg': background_color})

def on_entry_change(event):
        search_text = entry.get()
        on_search(search_text)

# ___________________________main_________________________________

def main():
    # variables
    global is_importer, options, x_position, y_position, root, checkbox_vars
    global btn_eks, btn_ins, btn_im, scrollbar, frame,frame3, listbox, entry, label_choose, checkbox
    options = ["Opcja 1", "Opcja 2", "Opcja 3", "Opcja 4", "Opcja 5", "Opcja 6",
               "Opcja 7", "Opcja 8", "Opcja 9","Opcja 10", "Opcja 11", "Opcja 12",
               "Opcja 13", "Opcja 14", "Opcja 15","Opcja 16", "Opcja 17", "Opcja 18",
               "Opcja 19", "Opcja 20", "Opcja 21","Opcja 22", "Opcja 23", "Opcja 24"]
    root = tk.Tk()
    
    # App settings
    root.title("Ceemea presentation generator")
    root.configure(bg="#404040") 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    style = ttk.Style()
    style.configure("TCheckbutton", foreground="black", background="white", font=("Arial", 24), padding=(20, 10, 10, 5)) 
    frame_width = int(screen_width * 0.7)
    frame_height = int(screen_height * 0.5)
    x_position = (screen_width - frame_width + 140) // 2
    y_position = (screen_height- frame_height - 30) // 2
    is_importer = tk.BooleanVar()

    # instructions
    btn_ins = tk.Button(root, text="Instructions", command=instructions, foreground="Black", font=("Arial", 18))
    btn_ins.place(y=0, x=0)

    # Frame RHS/ LHS
    frame = ttk.Frame(root)
    frame.place(x=x_position, y=y_position)
    
    # Frame with options to choose
    frame3 = ttk.Frame(root)
    checkbox_vars = [tk.BooleanVar() for _ in options]
    checkboxes = []
    k, col, row_i = 0,1,1
    for i, option in enumerate(options):
        k += 1
        checkbox = ttk.Checkbutton(frame3, text=option, variable=checkbox_vars[i], style="TCheckbutton")
        checkbox["state"] = "normal"
        checkbox.grid(row=row_i, column=col, sticky=tk.W, padx=10, pady=8)
        checkboxes.append(checkbox)
        if k == 8:
            row_i, col = 0, 2
        if k == 16:
            row_i, col = 0, 3
        row_i += 1

    # labels and bottons o the intro:
    label_choose = tk.Label(root, text="Choose a site:", font=("Arial", 24), 
                                background="#404040", foreground="white")
    label_choose.place(x=x_position*2.1, y=y_position-50)
    btn_im = tk.Button(frame, text="RHS - buying base currency", command=lambda: on_click_im(is_importer),
                        foreground="black", background="white", font=("Arial", 24), height=5)
    btn_im.grid(row=1, column=0, padx=30, pady=30)
    btn_eks = tk.Button(frame, text="LHS - selling base currency", command=lambda: on_click_eks(is_importer),
                            foreground="black", background="white", font=("Arial", 24), height=5)
    btn_eks.grid(row=1, column=1, padx=30, pady=30)
    
    # scrollbar
    scrollbar = tk.Scrollbar(frame, orient="vertical")
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.MULTIPLE, width=40,
                         font=('Arial', 24), background="white",foreground="black")
    scrollbar.config(command=listbox.yview)
    for i, option in enumerate(options):
        background_color = "#E8F7DF" if i % 2 == 0 else "white"
        listbox.insert(tk.END, option)
        listbox.itemconfig(i, {'bg': background_color})
    entry = tk.Entry(frame)
    entry.bind("<KeyRelease>", on_entry_change)
    do_frame2()

        #
    root.mainloop()

if __name__ == "__main__":
    main()
