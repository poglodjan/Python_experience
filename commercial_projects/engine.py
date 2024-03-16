import tkinter as tk
from tkinter import ttk
from frames_options import *
from tkinter import PhotoImage, Tk
from PIL import Image, ImageTk

# first episode

def create_frames(selected_options, is_importer):
    importer = is_importer.get()
    frame_ins.grid_forget()
    change_frame.place_forget()
    frame.place_forget()
    frame3.place_forget()
    label_choose.place_forget()
    do_settings_frame(is_importer, root, screen_height, selected_options)

    counter = 1
    global canvas
    canvas = tk.Canvas(root, bg="#404040", scrollregion=(0, 0, 1000, len(selected_options)*120))
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    if len(selected_options) > 5:
        scrollbar_c = tk.Scrollbar(root, command=on_canvas_scroll, width=30)
        scrollbar_c.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=scrollbar_c.set)

    # showing selected options to input data:
    if "FX Forward" in selected_options: 
        create_forward_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Parforward" in selected_options: 
        create_Parforward_frame(importer,eye_icon,info_icon, canvas, counter)
        counter +=1
    if "European Call Option" in selected_options: 
        create_EurOp_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Call Spread" in selected_options: 
        create_Spread_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Participating Forward" in selected_options: 
        create_Participating_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Capped Forward" in selected_options: 
        create_Capped_frame(importer,eye_icon,info_icon, canvas, counter)
        counter +=1
    if "Loss Capped Forward" in selected_options: 
        create_Loss_frame(importer,eye_icon,info_icon, canvas, counter)
        counter +=1
    if "Collar" in selected_options: 
        create_collar_frame(importer,eye_icon,info_icon, canvas, counter)
        counter +=1
    if "Step Down Forward" in selected_options: 
        create_StepFw_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Leveraged Forward" in selected_options: 
        create_Leveraged_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Seagull" in selected_options: 
        create_Seagull_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Lookback Forward" in selected_options: 
        create_Lookback_frame(importer,info_icon, canvas, counter) 
        counter +=1.7
    if "Convertible Forward" in selected_options: 
        create_ConvertibleFrw_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Knock-Out Forward" in selected_options: 
        create_KnockFrw_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Knock-Out Collar" in selected_options: 
        create_KnockCol_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Knock-Out Collar with Subsidy" in selected_options: 
        create_KnockColSub_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Knock-Out Forward with Subsidy" in selected_options: 
        create_KnockFrwSub_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Step Down Collar" in selected_options: 
        create_StepCol_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Convertible Collar" in selected_options: 
        create_ConvertibleCol_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "Extendable Forward" in selected_options: 
        create_Ex_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "TARF" in selected_options: 
        create_TARF_frame(importer,info_icon, canvas, counter) 
        counter +=1.7
    if "American Call Option" in selected_options: 
        create_AmerOp_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "European Call Option with Rebate" in selected_options: 
        create_EurOp_r_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1.7
    if "American Call Option with Rebate" in selected_options: 
        create_AmerOp_r_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1.7
    if "Option on Option" in selected_options: 
        create_OpOp_frame(importer,eye_icon,info_icon, canvas, counter) 
        counter +=1
    if "New Instrument" in selected_options:
        create_NewIn_frame(root, canvas, counter) 
    
def go_to_change():
    pass   

def on_canvas_scroll(*args):
    canvas.yview(*args)    

def show_options():
    frame3.place(x=x_position, y=200)

def show_scrollbar():
    do_scrollbar(options)       
    label_search = tk.Label(frame, text="Search for instrument:",font=("Arial", 16))
    label_search.grid(row=0, column=0, sticky="ns")
    scrollbar.grid(row=2, column=1, sticky="ns")
    listbox.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")
    entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    change_frame.place(x=x_position+700, y=200)

def on_view_selected(event):
        selected_option = view_var.get()
        if selected_option == "Scrollbar":
            show_scrollbar()
            checkbox.grid_forget()
            frame3.place_forget()
        elif selected_option == "Checkboxes":
            show_options()
            scrollbar.grid_forget()
            listbox.grid_forget()
            label_choose.grid_forget()

def on_choose_selected(event):
        global options
        filter_list = choose_var.get()
        selected_option = view_var.get()
        options_old = options
        if filter_list == "Collar":
            filtered_options = [option for option in options if "Collar" in option]
            filtered_options.sort()
            if selected_option == "Choose": do_checkboxes_options(filtered_options)
            if selected_option == "Scrollbar": do_scrollbar(filtered_options)
        elif filter_list == "Forward":
            filtered_options = [option for option in options if "Forward" in option]
            filtered_options.sort()
            if selected_option == "Choose": do_checkboxes_options(filtered_options)
            if selected_option == "Scrollbar": do_scrollbar(filtered_options)
        elif filter_list == "Options":
            filtered_options = [option for option in options if "Options" in option]
            filtered_options.sort()
            options = filtered_options
            if selected_option == "Choose": do_checkboxes_options(filtered_options)
            if selected_option == "Scrollbar": do_scrollbar(filtered_options)
        elif filter_list == "All":
            if selected_option == "Choose": do_checkboxes_options(options_old)
            if selected_option == "Scrollbar": do_scrollbar(options_old)

def on_click_im(is_importer):
    is_importer.set(True)
    label_choose.config(text="Choose models:")
    btn_im.grid_forget()
    frame_set1.grid_forget()
    frame_template.grid_forget()
    btn_eks.grid_forget()
    show_scrollbar()

def on_click_eks(is_importer):
    is_importer.set(False)
    label_choose.config(text="Choose models:")
    frame_set1.grid_forget()
    frame_template.grid_forget()
    btn_im.grid_forget()
    btn_eks.grid_forget()
    show_scrollbar()

def instructions():
    pass 

def do_frame2():
    global change_frame, view_var, choose_var
    change_frame = tk.Frame(root, width=100, height=400, borderwidth=3,relief="ridge",padx=5,pady=2)
    label_which_view = tk.Label(change_frame, text="Which View:",
                                font=("Arial", 16))
    label_which_view.grid(row=0, column=0, sticky="w")
    view_options = ["Scrollbar", "Checkboxes"]
    view_var = tk.StringVar(value=view_options[0])
    view_dropdown = ttk.Combobox(change_frame, values=view_options, textvariable=view_var, 
                                 font=("Arial", 16),width=12,state="readonly")
    view_dropdown.grid(row=1, column=0, padx=4)
    view_dropdown.bind("<<ComboboxSelected>>", on_view_selected)
    label_choose_options = tk.Label(change_frame, text="Choose from options:",
                                    font=("Arial", 16))
    label_choose_options.grid(row=2, column=0, sticky="w", pady=(10, 0))
    choose_options = ["All", "Collar", "Forward", "Option"]
    choose_var = tk.StringVar(value=choose_options[0])
    choose_dropdown = ttk.Combobox(change_frame, values=choose_options,font=("Arial", 16),
                                    textvariable=choose_var, width=12, state="readonly")
    choose_dropdown.grid(row=3, column=0, padx=5)
    choose_dropdown.bind("<<ComboboxSelected>>", on_choose_selected)
    confirm1 = tk.Button(change_frame, text="Confirm", command=confirm1_selection, foreground="white",
                             font=("Arial", 18), background="#007600",highlightbackground="#007600")
    confirm1.grid(row=4, column=0, padx=10, pady=5)

def do_checkboxes_options(options):
# Frame with options to choose
    global checkbox, frame3, checkbox_vars
    frame3 = ttk.Frame(root)
    checkbox_vars = [tk.BooleanVar() for _ in options]
    checkboxes = []
    k, col, row_i = 0,1,1
    for i, option in enumerate(options):
        k += 1
        checkbox = tk.Checkbutton(frame3, text=option, variable=checkbox_vars[i], selectcolor="black",
                                   foreground="white", background="#001F3F", font=("Arial", 16), padx=20, pady=5)
        checkbox["state"] = "normal"
        checkbox.grid(row=row_i, column=col, sticky=tk.W, padx=5, pady=8)
        checkboxes.append(checkbox)
        if k == 10: row_i, col = 0, 2
        if k == 20: row_i, col = 4, 3
        row_i += 1

def do_scrollbar(options):
    global scrollbar, listbox, entry
    scrollbar = tk.Scrollbar(frame, orient="vertical", width=20)
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.MULTIPLE, width=36,height=12,
                         font=('Arial', 18), background="white",foreground="black")
    scrollbar.config(command=listbox.yview)
    for i, option in enumerate(options):
        background_color = "#a9dbf2" if i % 2 == 0 else "white"
        listbox.insert(tk.END, option)
        listbox.itemconfig(i, {'bg': background_color})
    listbox.bind("<<ListboxSelect>>", on_listbox_select)
    entry = tk.Entry(frame)
    entry.bind("<KeyRelease>", on_entry_change)

def do_settings():
    global label_choose,frame_set1,frame_template, btn_eks, btn_im
    label_choose = tk.Label(root, text="Choose a site:", font=("Arial", 18), 
                                background="#404040", foreground="white")
    label_choose.place(x=x_position + 360, y=160)
    btn_im = tk.Button(frame, text="RHS - buying base currency", command=lambda: on_click_im(is_importer),
                        foreground="black", background="white", font=("Arial", 18), height=5)
    btn_im.grid(row=1, column=0, padx=30, pady=30)
    btn_eks = tk.Button(frame, text="LHS - selling base currency", command=lambda: on_click_eks(is_importer),
                            foreground="black", background="white", font=("Arial", 18), height=5)
    btn_eks.grid(row=1, column=1, padx=30, pady=30)
    frame_set1 = tk.Frame(intro, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    frame_set1.grid(row=0,column=1,padx=(5,5))
    text = tk.Label(frame_set1, text=f"See or change textes for options ", font=('Arial', 12), fg='white', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5)) 
    change_textes = tk.Button(frame_set1, command=go_to_change, image=rocket_icon,highlightbackground="navy",font=('Arial', 12))
    frame_template = tk.Frame(intro, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    frame_template.grid(row=0,column=2,padx=(5,5))
    change_textes.grid(row=0, column=1, padx=(5, 5))
    text = tk.Label(frame_template, text=f"See or change PowerPoint template ", font=('Arial', 12), fg='white', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5)) 
    change_textes = tk.Button(frame_template, command=go_to_change, image=rocket_icon,highlightbackground="navy",font=('Arial', 12))
    change_textes.grid(row=0, column=1, padx=(5, 5))

def confirm1_selection():
    selected_option = view_var.get()
    if selected_option == "Checkboxes": selected_options = [options[i] for i, var in enumerate(checkbox_vars) if var.get()]
    if selected_option == "Scrollbar":
        selected_indices = listbox.curselection()
        selected_options = [listbox.get(index) for index in selected_indices]
    create_frames(selected_options, is_importer)

def on_search(entry_text):
    filtered_options = [option for option in options if entry_text.lower() in option.lower()]
    update_listbox(filtered_options)

def on_listbox_select(event):
    selected_indices = listbox.curselection()
    for i in range(listbox.size()):
        is_selected = i in selected_indices
        listbox.itemconfig(i, {'selectbackground': '#19983e' if is_selected else ''})
        listbox.itemconfig(i, {'selectforeground': 'white' if is_selected else ''})

def update_listbox(filtered_options):
    listbox.delete(0, tk.END)
    for i, option in enumerate(filtered_options):
        background_color = "#a9dbf2" if i % 2 == 0 else "white"
        listbox.insert(tk.END, option)
        listbox.itemconfig(i, {'bg': background_color})

def on_entry_change(event):
        search_text = entry.get()
        on_search(search_text)

# ___________________________main_________________________________
        

global is_importer, options, x_position, y_position, root, screen_height, selected_options
global frame_ins, frame, label_choose, eye_icon
options = ["FX Forward", "Parforward", "European Call Option", "Call Spread", "Participating Forward", "Collar",
               "Capped Forward", "Loss Capped Forward", "Step Down Forward","Leveraged Forward", "Seagull", "Lookback Forward",
               "Convertible Forward", "Knock-Out Forward", "Knock-Out Collar", "Knock-Out Collar with Subsidy", "Knock-Out Forward with Subsidy",
                 "Step Down Collar","Convertible Collar", "Extendable Forward", "TARF - not ready","American Call Option", "European Call Option with Rebate", 
                 "American Call Option with Rebate", "Option on Option","New Instrument"]
root = tk.Tk()
eye_icon = ImageTk.PhotoImage(Image.open("eye.png").resize((18,18)))
info_icon = ImageTk.PhotoImage(Image.open("info.png").resize((18,18)))
rocket_icon = ImageTk.PhotoImage(Image.open("rocket.png").resize((18,18)))
                              
selected_options=[]
    # App settings
root.title("Ceemea presentation generator 2.0")
root.configure(bg="#404040") 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
frame_width = int(screen_width * 0.7)
frame_height = int(screen_height * 0.5)
x_position = (screen_width - frame_width) // 2
y_position = (screen_height- frame_height) // 2
is_importer = tk.BooleanVar()

global intro
intro = tk.Frame(root, width=200, height=100, bg='white', bd=4, 
                             highlightbackground="black",highlightthickness=4)
intro.place(x=0, y=0)

    # instructions
frame_ins = tk.Frame(intro, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
frame_ins.grid(row=0,column=0,padx=(5,5))
text = tk.Label(frame_ins, text=f"Instructions ", font=('Arial', 12), fg='white', bg='navy')
text.grid(row=0, column=0, padx=(5, 5)) 
text = tk.Button(frame_ins, command=instructions, image=rocket_icon,highlightbackground="navy",font=('Arial', 12))
text.grid(row=0, column=1, padx=(5, 5))

    # Frame RHS/ LHS
frame = ttk.Frame(root)
frame.place(x=x_position + 100, y=200)
    # frame with all options
do_checkboxes_options(options)

    # labels and buttons in the intro:
do_settings()
    
    # scrollbar
do_scrollbar(options)
do_frame2()

root.mainloop()

# 1 levery
# 2 drugie tabele
# 3 terms
# 4 pauout
# 7 comparison
# 8 usuwanie
