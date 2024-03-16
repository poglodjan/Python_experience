import tkinter as tk
from tkinter import ttk
from run import run_pp
from charts import *
from tkinter import PhotoImage, Tk
from PIL import Image, ImageTk
from io import BytesIO

def create_forward_frame(importer,eye_icon,info_icon,canvas,counter):
    values = ["1.5000","1"]
    s = "FX Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. FX Forward | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3, pady=10,padx=(5, 5))
    fxforw_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    fxforw_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    fxforw_S.insert(0, values[0])
    fxforw_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    fxforw_L.grid(row=0, column=4, padx=(5, 5), pady=10)
    fxforw_L.insert(0, values[1])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=5, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_forward_on_button(importer,s, fxforw_S, fxforw_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=6, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=7, padx=(0,5))
    selected_inputs.append([s,fxforw_S,fxforw_L])

def create_Parforward_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.4350","1"]
    s="Parforward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Par Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3, pady=10,padx=(5, 5))
    par_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    par_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    par_S.insert(0, values[0])
    par_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    par_L.grid(row=0, column=4, padx=(5, 5), pady=10)
    par_L.insert(0, values[1])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=5, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_forward_on_button(importer,s, par_S, par_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=6, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than "1". \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=7, padx=(0,5))
    selected_inputs.append([s,par_S,par_L])

def create_Ex_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.5000","01/05/2025","01/01/2025","1"]
    s = "Extendable Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Extendable Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Guaranteed Expiry Date:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Conditional Expiry Date:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7, pady=10,padx=(5, 5))
    Ex_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    Ex_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    Ex_S.insert(0, values[0])
    Ex_GDate = tk.Entry(option_frame, font=('Arial', 15),width=10)
    Ex_GDate.grid(row=0, column=4, padx=(5, 5), pady=10)
    Ex_GDate.insert(0, values[1])
    Ex_CDate = tk.Entry(option_frame, font=('Arial', 15),width=10)
    Ex_CDate.grid(row=0, column=6, padx=(5, 5), pady=10)
    Ex_CDate.insert(0, values[2])
    Ex_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    Ex_L.grid(row=0, column=8, padx=(5, 5), pady=10)
    Ex_L.insert(0, values[3])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=9, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_forward_on_button(importer,s, Ex_S, Ex_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n 
- The dates can be provided in any format. """ 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=11, padx=(0,5))
    selected_inputs.append([s,Ex_S,Ex_GDate,Ex_CDate,Ex_L])

def create_EurOp_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.6000","4.55","1 000 000"]
    s="European Call Option"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. European Option  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Premium (%):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Option Nominal:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5, pady=10,padx=(5, 5))
    eurOp_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    eurOp_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    eurOp_S.insert(0, values[0])
    eurOp_Pr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    eurOp_Pr.grid(row=0, column=4, padx=(5, 5), pady=10)
    eurOp_Pr.insert(0, values[1])
    eurOp_N = tk.Entry(option_frame, font=('Arial', 15),width=10)
    eurOp_N.grid(row=0, column=6, padx=(5, 5), pady=10)
    eurOp_N.insert(0, values[2])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=7, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_option_on_button(importer,s, eurOp_S, eurOp_Pr), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=8, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
- Premium has to be between 0 and 100 \n
- If you want to have diffrent notional in scenario just in this option set it in Option Notional cell""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(0,5))
    selected_inputs.append([s,eurOp_S,eurOp_Pr,eurOp_N])

def create_OpOp_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.6000","2.55","1 000 000"]
    s="Option on Option"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Option on Option  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Premium (%):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Option Nominal:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5, pady=10,padx=(5, 5))
    OpOp_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    OpOp_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    OpOp_S.insert(0, values[0])
    OpOp_Pr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    OpOp_Pr.grid(row=0, column=4, padx=(5, 5), pady=10)
    OpOp_Pr.insert(0, values[1])
    OpOp_N = tk.Entry(option_frame, font=('Arial', 15),width=10)
    OpOp_N.grid(row=0, column=6, padx=(5, 5), pady=10)
    OpOp_N.insert(0, values[2])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=7, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_option_on_button(importer,s, OpOp_S, OpOp_Pr), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=8, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
- Premium has to be between 0 and 100 \n
- If you want to have diffrent notional in scenario just in this option set it in Option Notional cell""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(0,5))
    selected_inputs.append([s,OpOp_S,OpOp_Pr,OpOp_N])

def create_EurOp_r_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.6000","6.55","1 000 000","1.5300","50"]
    s="European Call Option with Rebate"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. European Option with Rebate  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Premium (%):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Option Nominal:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5, pady=10,padx=(5, 5))
    text = tk.Label(option_frame, text="Rebate level:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Rebate (% from option):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=3,padx=(5, 5), pady=10)
    eurOpR_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    eurOpR_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    eurOpR_S.insert(0, values[0])
    eurOpR_Pr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    eurOpR_Pr.grid(row=0, column=4, padx=(5, 5), pady=10)
    eurOpR_Pr.insert(0, values[1])
    eurOpR_N = tk.Entry(option_frame, font=('Arial', 15),width=10)
    eurOpR_N.grid(row=0, column=6, padx=(5, 5), pady=10)
    eurOpR_N.insert(0, values[2])
    eurOpR_RebL = tk.Entry(option_frame, font=('Arial', 15),width=10)
    eurOpR_RebL.grid(row=1, column=2, padx=(5, 5), pady=10)
    eurOpR_RebL.insert(0, values[3])
    eurOpR_Reb = tk.Entry(option_frame, font=('Arial', 15),width=10)
    eurOpR_Reb.grid(row=1, column=4, padx=(5, 5), pady=10)
    eurOpR_Reb.insert(0, values[4])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=7, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_optionR_on_button(importer,s, eurOpR_S, eurOpR_Pr, eurOpR_RebL, eurOpR_Reb), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=8, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
- Premium has to be between 0 and 100 \n
- Rebate corresponds to how much you want to reduce the premium. If the cost of the premium is 10, \n
and you enter a Rebate = 40% this means that the new premium will be 4 (at the rebate level) \n
- Rebate level is the level in which rebate will activate. \n
- If you want to have diffrent notional in scenario just in this option set it in Option Notional cell \n\n
(NOTE) If RHS: Rebate is below the strike. If LHS: Rebate is above the strike. """
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(0,5))
    selected_inputs.append([s, eurOpR_S, eurOpR_Pr, eurOpR_N, eurOpR_RebL, eurOpR_Reb])

def create_AmerOp_r_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.5500","5.5","1 000 000","1.4900","40"]
    s="American Call Option with Rebate"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. American Option with Rebate  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Premium (%):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Option Nominal:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5, pady=10,padx=(5, 5))
    text = tk.Label(option_frame, text="Rebate level:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Rebate (% from option):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=3,padx=(5, 5), pady=10)
    AmerOpR_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    AmerOpR_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    AmerOpR_S.insert(0, values[0])
    AmerOpR_Pr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    AmerOpR_Pr.grid(row=0, column=4, padx=(5, 5), pady=10)
    AmerOpR_Pr.insert(0, values[1])
    AmerOpR_N = tk.Entry(option_frame, font=('Arial', 15),width=10)
    AmerOpR_N.grid(row=0, column=6, padx=(5, 5), pady=10)
    AmerOpR_N.insert(0, values[2])
    AmerOpR_RebL = tk.Entry(option_frame, font=('Arial', 15),width=10)
    AmerOpR_RebL.grid(row=1, column=2, padx=(5, 5), pady=10)
    AmerOpR_RebL.insert(0, values[3])
    AmerOpR_Reb = tk.Entry(option_frame, font=('Arial', 15),width=10)
    AmerOpR_Reb.grid(row=1, column=4, padx=(5, 5), pady=10)
    AmerOpR_Reb.insert(0, values[4])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=7, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_optionR_on_button(importer,s, AmerOpR_S, AmerOpR_Pr,AmerOpR_RebL,AmerOpR_Reb), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=8, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
- Premium has to be between 0 and 100 \n
- Rebate corresponds to how much you want to reduce the premium. If the cost of the premium is 10, \n
and you enter a Rebate = 40% this means that the new premium will be 4 (at the rebate level) \n
- Rebate level is the level in which rebate will activate. \n
- If you want to have diffrent notional in scenario just in this option set it in Option Notional cell \n\n
(NOTE) If RHS: Rebate is below the strike. If LHS: Rebate is above the strike. """ 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(0,5))
    selected_inputs.append([s, AmerOpR_S, AmerOpR_Pr, AmerOpR_RebL, AmerOpR_Reb, AmerOpR_N])

def create_AmerOp_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.6200","4.70","1 000 000"]
    s="American Call Option"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. American Option  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Premium (%):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Option Nominal:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5, pady=10,padx=(5, 5))
    amerOp_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    amerOp_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    amerOp_S.insert(0, values[0])
    amerOp_Pr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    amerOp_Pr.grid(row=0, column=4, padx=(5, 5), pady=10)
    amerOp_Pr.insert(0, values[1])
    amerOp_N = tk.Entry(option_frame, font=('Arial', 15),width=10)
    amerOp_N.grid(row=0, column=6, padx=(5, 5), pady=10)
    amerOp_N.insert(0, values[2])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=7, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_option_on_button(importer, s, amerOp_S, amerOp_Pr), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=8, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
- Premium has to be between 0 and 100 \n
- If you want to have diffrent notional in scenario just in this option set it in Option Notional cell""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(0,5))
    selected_inputs.append([s, amerOp_S, amerOp_Pr, amerOp_N])

def create_Spread_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.3000","1.6000","4.55","1 000 000"]
    s="Call Spread"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Call/Put Spread  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Lower Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Upper Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Premium (%):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Option Nominal:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7, pady=10,padx=(5, 5))
    spread_LS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    spread_LS.grid(row=0, column=2, padx=(5, 5), pady=10)
    spread_LS.insert(0, values[0])
    spread_US = tk.Entry(option_frame, font=('Arial', 15),width=10)
    spread_US.grid(row=0, column=4, padx=(5, 5), pady=10)
    spread_US.insert(0, values[1])
    spread_Pr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    spread_Pr.grid(row=0, column=6, padx=(5, 5), pady=10)
    spread_Pr.insert(0, values[2])
    spread_N = tk.Entry(option_frame, font=('Arial', 15),width=10)
    spread_N.grid(row=0, column=8, padx=(5, 5), pady=10)
    spread_N.insert(0, values[3])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=9, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_spread_on_button(importer,s, spread_LS, spread_US, spread_Pr), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Lower and Upper Strike should be between chart's ranges. \n
- Premium has to be between 0 and 100 \n
- Lower strike should be lower than upper strike \n
- The difference between lower and upper strikes coresponds to the subsidy given to Client \n
- If you want to have diffrent notional in scenario just in this option set it in Option Notional cell""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=11, padx=(0,5))
    selected_inputs.append([s, spread_LS,spread_US, spread_Pr, spread_N])

def create_StepFw_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.5000","5","1.3500","1"]
    s="Step Down Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Step Down/Up Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Reset Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Trigger:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7, pady=10,padx=(5, 5))
    stepF_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    stepF_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    stepF_S.insert(0, values[0])
    stepF_Rst = tk.Entry(option_frame, font=('Arial', 15),width=10)
    stepF_Rst.grid(row=0, column=4, padx=(5, 5), pady=10)
    stepF_Rst.insert(0, values[1])
    stepF_Tr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    stepF_Tr.grid(row=0, column=6, padx=(5, 5), pady=10)
    stepF_Tr.insert(0, values[2])
    stepF_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    stepF_L.grid(row=0, column=8, padx=(5, 5), pady=10)
    stepF_L.insert(0, values[3])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=9, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_stepForw_on_button(importer,s, stepF_S, stepF_Rst, stepF_Tr, stepF_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n 
- The trigger is level in which subsidy will activate.\n\n
(NOTE) If RHS: Trigger and reset strike should be lower than strike. \n
If LHS: Trigger and reset strike should be higher than strike. """ 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=11, padx=(0,5))
    selected_inputs.append([s, stepF_S, stepF_Rst, stepF_Tr, stepF_L])

def create_StepCol_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.5000","1.6000","1.4200","1.3500","1"]
    s="Step Down Collar"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Step Down/Up Collar  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Lower Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Upper Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Reset Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Trigger:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=9, pady=10,padx=(5, 5))
    stepCol_LS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    stepCol_LS.grid(row=0, column=2, padx=(5, 5), pady=10)
    stepCol_LS.insert(0, values[0])
    stepCol_US = tk.Entry(option_frame, font=('Arial', 15),width=10)
    stepCol_US.grid(row=0, column=4, padx=(5, 5), pady=10)
    stepCol_US.insert(0, values[1])
    stepCol_Rst = tk.Entry(option_frame, font=('Arial', 15),width=10)
    stepCol_Rst.grid(row=0, column=6, padx=(5, 5), pady=10)
    stepCol_Rst.insert(0, values[2])
    stepCol_Tr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    stepCol_Tr.grid(row=0, column=8, padx=(5, 5), pady=10)
    stepCol_Tr.insert(0, values[3])
    stepCol_L = tk.Entry(option_frame, font=('Arial', 15),width=5)
    stepCol_L.grid(row=0, column=10, padx=(5, 5), pady=10)
    stepCol_L.insert(0, values[4])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=11, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_stepCol_on_button(importer,s, stepCol_LS,stepCol_US,stepCol_Rst,stepCol_Tr, stepCol_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=12, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strikes should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n 
- The trigger is level in which subsidy will activate.\n\n
(NOTE) If RHS: Trigger and reset strike should be lower than lower strike. \n
If LHS: Trigger and reset strike should be higher than upper strike. """ 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=13, padx=(0,5))
    selected_inputs.append([s,stepCol_LS, stepCol_US, stepCol_Rst, stepCol_Tr, stepCol_L])

def create_ConvertibleFrw_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.5000","1.4200","1"]
    s="Convertible Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Convertible Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Trigger:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5, pady=10,padx=(5, 5))
    convF_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    convF_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    convF_S.insert(0, values[0])
    convF_Tr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    convF_Tr.grid(row=0, column=4, padx=(5, 5), pady=10)
    convF_Tr.insert(0, values[1])
    convF_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    convF_L.grid(row=0, column=6, padx=(5, 5), pady=10)
    convF_L.insert(0, values[2])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=7, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_convForw_on_button(importer,s, convF_S, convF_Tr,convF_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=8, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n 
- The trigger is level in which subsidy will activate.\n\n
(NOTE) If RHS: Trigger should be lower than strike. \n
If LHS: Trigger should be higher than strike. """ 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(0,5))
    selected_inputs.append([s,convF_S, convF_Tr, convF_L])

def create_ConvertibleCol_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.5000","1.6000","1.4200","1"]
    s="Convertible Collar"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Convertible Collar  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Lower Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Upper Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Trigger:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7, pady=10,padx=(5, 5))
    convCol_LS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    convCol_LS.grid(row=0, column=2, padx=(5, 5), pady=10)
    convCol_LS.insert(0, values[0])
    convCol_US = tk.Entry(option_frame, font=('Arial', 15),width=10)
    convCol_US.grid(row=0, column=4, padx=(5, 5), pady=10)
    convCol_US.insert(0, values[1])
    convCol_Tr = tk.Entry(option_frame, font=('Arial', 15),width=10)
    convCol_Tr.grid(row=0, column=6, padx=(5, 5), pady=10)
    convCol_Tr.insert(0, values[2])
    convCol_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    convCol_L.grid(row=0, column=8, padx=(5, 5), pady=10)
    convCol_L.insert(0, values[3])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=9, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_convCol_on_button(importer,s, convCol_LS,convCol_US,convCol_Tr,convCol_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strikes should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n 
- The trigger is level in which subsidy will activate.\n\n
(NOTE) If RHS: Trigger should be lower than lower strike. \n
If LHS: Trigger should be higher than upper strike. """ 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=11, padx=(0,5))
    selected_inputs.append([s,convCol_LS, convCol_US, convCol_Tr, convCol_L])

def create_KnockFrw_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.4000","1.5200","1"]
    s="Knock-Out Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Knock-Out Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Knock-Out:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5, pady=10,padx=(5, 5))
    KnockF_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockF_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    KnockF_S.insert(0, values[0])
    KnockF_KO = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockF_KO.grid(row=0, column=4, padx=(5, 5), pady=10)
    KnockF_KO.insert(0, values[1])
    KnockF_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    KnockF_L.grid(row=0, column=6, padx=(5, 5), pady=10)
    KnockF_L.insert(0, values[2])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=7, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_knockFrw_on_button(importer,s, KnockF_S, KnockF_KO, KnockF_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=8, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n 
- The knock-out is level in which option will activate.\n\n
(NOTE) If RHS: Knock-out should be higher than strike. \n
If LHS: Knock-out should be lower than strike. """ 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(0,5))
    selected_inputs.append([s,KnockF_S, KnockF_KO, KnockF_L])

def create_KnockFrwSub_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.4000","1.5200","5","1"]
    s="Knock-Out Forward with Subsidy"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. KO Forward with Subsidy |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Knock-Out:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Sub:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7, pady=10,padx=(5, 5))
    KnockFS_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockFS_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    KnockFS_S.insert(0, values[0])
    KnockFS_KO = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockFS_KO.grid(row=0, column=4, padx=(5, 5), pady=10)
    KnockFS_KO.insert(0, values[1])
    KnockFS_Sub = tk.Entry(option_frame, font=('Arial', 15),width=6)
    KnockFS_Sub.grid(row=0, column=6, padx=(5, 5), pady=10)
    KnockFS_Sub.insert(0, values[2])
    KnockFS_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    KnockFS_L.grid(row=0, column=8, padx=(5, 5), pady=10)
    KnockFS_L.insert(0, values[3])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=9, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_knockFrwSub_on_button(importer,s, KnockFS_S, KnockFS_KO,KnockFS_Sub,KnockFS_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n 
- The knock-out is level in which option will activate.\n
- The subsidy is a return to Client. If provided 5 that means the Client will receive 0.05*notional in TERM\n\n
(NOTE) If RHS: Knock-out should be higher than strike. \n
If LHS: Knock-out should be lower than strike. """
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=11, padx=(0,5))
    selected_inputs.append([s,KnockFS_S, KnockFS_KO, KnockFS_Sub, KnockFS_L])

def create_KnockCol_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.4000","1.6000","1.6700","1"]
    s="Knock-Out Collar"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Knock-Out Collar  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Lower Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Upper Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Knock-Out:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7, pady=10,padx=(5, 5))
    KnockCol_LS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockCol_LS.grid(row=0, column=2, padx=(5, 5), pady=10)
    KnockCol_LS.insert(0, values[0])
    KnockCol_US = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockCol_US.grid(row=0, column=4, padx=(5, 5), pady=10)
    KnockCol_US.insert(0, values[1])
    KnockCol_KO = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockCol_KO.grid(row=0, column=6, padx=(5, 5), pady=10)
    KnockCol_KO.insert(0, values[2])
    KnockCol_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    KnockCol_L.grid(row=0, column=8, padx=(5, 5), pady=10)
    KnockCol_L.insert(0, values[3])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=9, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_knockCol_on_button(importer,s, KnockCol_LS,KnockCol_US,KnockCol_KO, KnockCol_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strikes should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n 
- The knock-out is level in which option will activate.\n\n
(NOTE) If RHS: Knock-out should be higher than upper strike. \n
If LHS: Knock-out should be lower than lower strike. """
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=11, padx=(0,5))
    selected_inputs.append([s,KnockCol_LS, KnockCol_US, KnockCol_KO, KnockCol_L])

def create_KnockColSub_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.4000","1.6000","1.6700","5","1"]
    s = "Knock-Out Collar with Subsidy"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. KO Collar with Subsidy |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Lower Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Upper Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Knock-Out:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Sub:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=9, pady=10,padx=(5, 5))
    KnockColS_LS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockColS_LS.grid(row=0, column=2, padx=(5, 5), pady=10)
    KnockColS_LS.insert(0, values[0])
    KnockColS_US = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockColS_US.grid(row=0, column=4, padx=(5, 5), pady=10)
    KnockColS_US.insert(0, values[1])
    KnockColS_KO = tk.Entry(option_frame, font=('Arial', 15),width=10)
    KnockColS_KO.grid(row=0, column=6, padx=(5, 5), pady=10)
    KnockColS_KO.insert(0, values[2])
    KnockColS_Sub = tk.Entry(option_frame, font=('Arial', 15),width=6)
    KnockColS_Sub.grid(row=0, column=8, padx=(5, 5), pady=10)
    KnockColS_Sub.insert(0, values[3])
    KnockColS_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    KnockColS_L.grid(row=0, column=10, padx=(5, 5), pady=10)
    KnockColS_L.insert(0, values[4])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=11, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_knockColSub_on_button(importer,s, KnockColS_LS, KnockColS_US,KnockColS_KO,KnockColS_Sub,KnockColS_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=12, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strikes should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n 
- The knock-out is level in which option will activate.\n
- The subsidy is a return to Client. If provided 5 that means the Client will receive 0.05*notional in TERM\n
(NOTE) If RHS: Knock-out should be higher than upper strike. \n
If LHS: Knock-out should be lower than lower strike. """
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=13, padx=(0,5))
    selected_inputs.append([s,KnockColS_LS, KnockColS_US, KnockColS_KO, KnockColS_Sub, KnockColS_L])

def create_Participating_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.5000","25"]
    s="Participating Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Participating Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Participation (%):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3, pady=10,padx=(5, 5))
    partip_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    partip_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    partip_S.insert(0, values[0])
    partip_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    partip_L.grid(row=0, column=4, padx=(5, 5), pady=10)
    partip_L.insert(0, values[1])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=5, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_partyp_on_button(importer,s, partip_S, partip_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=6, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
If you want option without participation leave "100" (100%). \n
If you want to make participation provide value between 0 and 100. \n
For example participation = 25% means that Client will buy/sell 25% of Notional in structure and 75% of Notional at market""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=7, padx=(0,5))
    selected_inputs.append([s,partip_S, partip_L])

def create_Leveraged_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.5000","2"]
    s="Leveraged Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Leveraged Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3, pady=10,padx=(5, 5))
    lev_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    lev_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    lev_S.insert(0, values[0])
    lev_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    lev_L.grid(row=0, column=4, padx=(5, 5), pady=10)
    lev_L.insert(0, values[1])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=5, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_forward_on_button(importer,s, lev_S, lev_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=6, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=7, padx=(0,5))
    selected_inputs.append([s,lev_S, lev_L])

def create_Capped_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.2000","1.4000","1"]
    s="Capped Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Capped Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Lower Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Upper Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=6, pady=10,padx=(5, 5))
    capped_LS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    capped_LS.grid(row=0, column=2, padx=(5, 5), pady=10)
    capped_LS.insert(0, values[0])
    capped_US = tk.Entry(option_frame, font=('Arial', 15),width=10)
    capped_US.grid(row=0, column=5, padx=(5, 5), pady=10)
    capped_US.insert(0, values[1])
    capped_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    capped_L.grid(row=0, column=7, padx=(5, 5), pady=10)
    capped_L.insert(0, values[2])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=8, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_capped_on_button(importer,s, capped_LS,capped_US, capped_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strikes should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n
- The Lower Strike should be lower than Upper Strike. It then coressponds appriopiate to strike on slide""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(0,5))
    selected_inputs.append([s,capped_LS, capped_US, capped_L])

def create_Loss_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.2000","1.4000","1"]
    s="Loss Capped Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Loss Capped Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Lower Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Upper Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=6, pady=10,padx=(5, 5))
    loss_LS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    loss_LS.grid(row=0, column=2, padx=(5, 5), pady=10)
    loss_LS.insert(0, values[0])
    loss_US = tk.Entry(option_frame, font=('Arial', 15),width=10)
    loss_US.grid(row=0, column=5, padx=(5, 5), pady=10)
    loss_US.insert(0, values[1])
    loss_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    loss_L.grid(row=0, column=7, padx=(5, 5), pady=10)
    loss_L.insert(0, values[2])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=8, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_loss_on_button(importer,s, loss_LS, loss_US,loss_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strikes should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n
- The Lower Strike should be lower than Upper Strike. It then coressponds appriopiate to strike on slide"""  
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(0,5))
    selected_inputs.append([s,loss_LS, loss_US, loss_L])

def create_Seagull_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.2000","1.3000","1.4000","1"]
    s="Seagull"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Seagull  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Lower Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Mid Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Upper Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7, pady=10,padx=(5, 5))
    seagull_LS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    seagull_LS.grid(row=0, column=2, padx=(5, 5), pady=10)
    seagull_LS.insert(0, values[0])
    seagull_MS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    seagull_MS.grid(row=0, column=4, padx=(5, 5), pady=10)
    seagull_MS.insert(0, values[1])
    seagull_US = tk.Entry(option_frame, font=('Arial', 15),width=10)
    seagull_US.grid(row=0, column=6, padx=(5, 5), pady=10)
    seagull_US.insert(0, values[2])
    seagull_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    seagull_L.grid(row=0, column=8, padx=(5, 5), pady=10)
    seagull_L.insert(0, values[3])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=9, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_seagull_on_button(importer,s, seagull_LS,seagull_MS, seagull_US, seagull_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strikes should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional \n
- The Lower Strike should be lower than Upper Strike. It then coressponds appriopiate to strike on slide \n
- The Mid Strike should be between lower and upper strikes"""
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=11, padx=(0,5))
    selected_inputs.append([s,seagull_LS, seagull_MS, seagull_US, seagull_L])

def create_Lookback_frame(importer,info_icon, canvas,counter):
    values = ["1.2400","1.2700","1.2000","1.5000","0.05","01/02/2025","01/09/2025"]
    s = "Lookback Forward"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Lookback Forward  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Reset Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Forward Reference:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Range: Min-Max (", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text=" - ", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7, pady=10,padx=(5, 5))
    text = tk.Label(option_frame, text=")", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=9, pady=10,padx=(5, 5))
    text = tk.Label(option_frame, text="Adjustment: (+/-)", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=1, pady=10,padx=(5, 5))
    text = tk.Label(option_frame, text="End of observation Date:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=3, pady=10,padx=(5, 5))
    text = tk.Label(option_frame, text="Expiry Date:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=5, pady=10,padx=(5, 5))
    look_Rst = tk.Entry(option_frame, font=('Arial', 15),width=10)
    look_Rst.grid(row=0, column=2, padx=(5, 5), pady=10)
    look_Rst.insert(0, values[0])
    look_Ref = tk.Entry(option_frame, font=('Arial', 15),width=10)
    look_Ref.grid(row=0, column=4, padx=(5, 5), pady=10)
    look_Ref.insert(0, values[1])
    look_Min = tk.Entry(option_frame, font=('Arial', 15),width=10)
    look_Min.grid(row=0, column=6, padx=(5, 5), pady=10)
    look_Min.insert(0, values[2])
    look_Max = tk.Entry(option_frame, font=('Arial', 15),width=10)
    look_Max.grid(row=0, column=8, padx=(5, 5), pady=10)
    look_Max.insert(0, values[3])
    look_adj = tk.Entry(option_frame, font=('Arial', 15),width=10)
    look_adj.grid(row=1, column=2, padx=(5, 5), pady=10)
    look_adj.insert(0, values[4])
    look_DateObs = tk.Entry(option_frame, font=('Arial', 15),width=10)
    look_DateObs.grid(row=1, column=4, padx=(5, 5), pady=10)
    look_DateObs.insert(0, values[5])
    look_DateExp = tk.Entry(option_frame, font=('Arial', 15),width=10)
    look_DateExp.grid(row=1, column=6, padx=(5, 5), pady=10)
    look_DateExp.insert(0, values[6])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=1, column=7, padx=(5, 5), pady=10)
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
    - Minimum and Maximum values are the range of Lookback Forward \n
    - Adjustment should be (+) positive if RHS and (-) negative if LHS \n
    - Expiry Date and Observation Date can be provided in any format. If equal then scenario is appriopiate """ 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=1, column=8, padx=(0,5))
    selected_inputs.append([s,look_Rst, look_Ref, look_Min, look_Max, look_adj, look_DateObs, look_DateExp])

def create_collar_frame(importer,eye_icon,info_icon, canvas,counter):
    values = ["1.2000","1.4000","1"]
    s="Collar"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. Collar  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Lower Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Upper Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=6, pady=10,padx=(5, 5))
    collar_LS = tk.Entry(option_frame, font=('Arial', 15),width=10)
    collar_LS.grid(row=0, column=2, padx=(5, 5), pady=10)
    collar_LS.insert(0, values[0])
    collar_US = tk.Entry(option_frame, font=('Arial', 15),width=10)
    collar_US.grid(row=0, column=5, padx=(5, 5), pady=10)
    collar_US.insert(0, values[1])
    collar_L = tk.Entry(option_frame, font=('Arial', 15),width=6)
    collar_L.grid(row=0, column=7, padx=(5, 5), pady=10)
    collar_L.insert(0, values[2])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=8, padx=(5, 5), pady=10)
    button_plus = tk.Button(option_frame, image=eye_icon, 
                            command=lambda:show_collar_on_button(importer,s, collar_LS, collar_US,collar_L), bd=2, highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=9, padx=(5,0))
    instruction = """Please provide all values. Don't leave blank cells. Strikes should be between chart's ranges. \n
If you want option without leverage leave "1", if you want to make leverage provide value bigger than 1. \n
For example leverage = 2 is equal to the Notional that is 50% of the Leveraged Niotional
- Lower strike should be lower than Upper Strike""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=0, column=10, padx=(0,5))

    selected_inputs.append([s,collar_LS, collar_US, collar_L])

def create_TARF_frame(importer,info_icon, canvas,counter):
    values = ["1.5000","1.5500","05/01/2025","12","0.6","5","W","1 000 000", "1"]
    s = "TARF"
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. TARF  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Strike:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Spot (scenario):", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Start Date:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Cash Flows:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=7,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Cap:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=9,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Step:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=1,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="[W]eekly/[M]onthly:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=3,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Scenario Analysis:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=5,padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text="Leverage:", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=1, column=7, pady=10,padx=(5, 5))
    tarf_S = tk.Entry(option_frame, font=('Arial', 15),width=10)
    tarf_S.grid(row=0, column=2, padx=(5, 5), pady=10)
    tarf_S.insert(0, values[0])
    tarf_Spot = tk.Entry(option_frame, font=('Arial', 15),width=10)
    tarf_Spot.grid(row=0, column=4, padx=(5, 5), pady=10)
    tarf_Spot.insert(0, values[1])
    tarf_Start = tk.Entry(option_frame, font=('Arial', 15),width=10)
    tarf_Start.grid(row=0, column=6, padx=(5, 5), pady=10)
    tarf_Start.insert(0, values[2])
    tarf_flows = tk.Entry(option_frame, font=('Arial', 15),width=10)
    tarf_flows.grid(row=0, column=8, padx=(5, 5), pady=10)
    tarf_flows.insert(0, values[3])
    tarf_cap = tk.Entry(option_frame, font=('Arial', 15),width=10)
    tarf_cap.grid(row=0, column=10, padx=(5, 5), pady=10)
    tarf_cap.insert(0, values[4])
    tarf_step = tk.Entry(option_frame, font=('Arial', 15),width=10)
    tarf_step.grid(row=1, column=2, padx=(5, 5), pady=10)
    tarf_step.insert(0, values[5])
    tarf_wm = tk.Entry(option_frame, font=('Arial', 15),width=10)
    tarf_wm.grid(row=1, column=4, padx=(5, 5), pady=10)
    tarf_wm.insert(0, values[6])
    tarf_N = tk.Entry(option_frame, font=('Arial', 15),width=10)
    tarf_N.grid(row=1, column=6, padx=(5, 5), pady=10)
    tarf_N.insert(0, values[7])
    tarf_L = tk.Entry(option_frame, font=('Arial', 15),width=10)
    tarf_L.grid(row=1, column=8, padx=(5, 5), pady=6)
    tarf_L.insert(0, values[8])
    text = tk.Label(option_frame, text=f" | ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=1, column=9, padx=(5, 5), pady=10)
    instruction = """Please provide all values. Don't leave blank cells. Strike should be between chart's ranges. \n
    - If RHS spot should be lower than strike. If LHS spot should be higher than strike. \n
    - Date can be provided in any format \n
    - You can provide between 1 and 12 flows. It coressponds to number of rows shows in the table on slide\n
    - If step is equal to 5, that means the spot on scenario goes by 0.05 higher/lower\n
    - You can choose if payout is shown montlhy or weekly. Provide M or W\n
    - If you want to have diffrent notional in scenario just in this option set it in Option Notional cell""" 
    button_plus = tk.Button(option_frame, image=info_icon, bd=2, 
                            command=lambda: info_on_button(s, instruction, canvas), highlightbackground= "#afe39d")
    button_plus.grid(row=1, column=10, padx=(0,5))
    selected_inputs.append([s,tarf_S,tarf_Spot,tarf_cap,tarf_flows,tarf_L,tarf_N,tarf_Start,tarf_step,tarf_wm])

def create_NewIn_frame(root, canvas,counter):
    global screen
    screen = root
    option_frame = tk.Frame(canvas, width=200, height=100, bg='navy', bd=4, 
                             highlightbackground="black",highlightthickness=4)
    canvas.create_window(10, 10 + ((counter - 1) * 80), anchor=tk.NW, window=option_frame)
    text = tk.Label(option_frame, text=f"{int(counter)}. New Instrument  |  ", font=('Arial', 17, 'bold'), fg='#d6d895', bg='navy')
    text.grid(row=0, column=0, padx=(5, 5), pady=10)
    text = tk.Label(option_frame, text=f"You can add textes/payout/terms on the Slide. Click to create chart and scenario: ", font=('Arial', 15), fg='white', bg='navy')
    text.grid(row=0, column=1, padx=(5, 5), pady=10)
    plus_button = tk.Button(option_frame, command=show_popup, text="+",highlightbackground="navy")
    plus_button.grid(row=0, column=2, padx=(5, 5), pady=10)

def show_popup():
    popup = tk.Toplevel(screen)
    popup.title("New instrument - chart and scenario")
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    popup_width = int(screen_width / 2)
    popup_height = int(screen_height / 2)
    popup.geometry(f"{popup_width}x{popup_height}+{int((screen_width - popup_width) / 2)}+{int((screen_height - popup_height) / 2)}")
    entry_label = ttk.Label(popup, text="Provide Structure:")
    entry_label.pack(pady=10)
    entry = ttk.Entry(popup)
    entry.pack(pady=10)

    close_button = ttk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)

def do_settings_frame(importer, canvas, screen_height, selected_options):
    global settings_frame,entry_boxes1,entry_boxes2,entry_boxes3,entry_boxes4,selected_inputs,entry_boxes
    selected_inputs = []
    settings_frame = tk.Frame(canvas, height=screen_height // 5, borderwidth=4,relief="ridge",padx=16,pady=2)
    settings_frame.configure(bg="#404040") 
    settings_frame.pack(fill=tk.X)
    entries_names = ["EUR", "USD", "1 000 000", "01/01/2025", "1.5001", "Client", 
             "1.0000", "2.0000", "4", "1.0000", "2.0000", "4"]
    labels_col1 = ["Base:", "Term:", "Notional:", "Expiry Date:"]
    labels_col2 = ["Spot:","Company's Name:"]
    labels_col3 = ["Scenario's Range min:","Scenario's Range max:", "Scenario's decimal:"]
    labels_col4 = ["Chart's Range min:","Chart's Range max:", "Chart's decimal:"]
    entry_boxes1 = [tk.Entry(settings_frame, bg='white', width=10,font=("Arial", 12)) for _ in range(len(labels_col1))]
    entry_boxes2 = [tk.Entry(settings_frame, bg='white', width=10,font=("Arial", 12)) for _ in range(len(labels_col2))]
    entry_boxes3 = [tk.Entry(settings_frame, bg='white', width=10,font=("Arial", 12)) for _ in range(len(labels_col3))]
    entry_boxes4 = [tk.Entry(settings_frame, bg='white', width=10,font=("Arial", 12)) for _ in range(len(labels_col4))]
    entry_boxes = [entry_boxes1,entry_boxes2,entry_boxes3,entry_boxes4]

    # settings labels in all columns
    for i, label_text in enumerate(labels_col1):
        label = tk.Label(settings_frame, text=label_text,background="#404040", foreground="white", font=("Arial", 12))
        label.grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
    for i, label_text in enumerate(labels_col2):
        label = tk.Label(settings_frame, text=label_text,background="#404040", foreground="white", font=("Arial", 12))
        label.grid(row=i, column=2, sticky=tk.E, padx=5, pady=5)
    for i, label_text in enumerate(labels_col3):
        label = tk.Label(settings_frame, text=label_text,background="#404040", foreground="white", font=("Arial", 11))
        label.grid(row=i, column=4, sticky=tk.E, padx=5, pady=5)
    for i, label_text in enumerate(labels_col4):
        label = tk.Label(settings_frame, text=label_text,background="#404040", foreground="white",font=("Arial", 11))
        label.grid(row=i, column=6, sticky=tk.E, padx=5, pady=5)
    # setting labels in columns 1-7
    k, col=0,0
    for j in [1,3,5,7]:
        i=0
        for i, entry_box in enumerate(entry_boxes[col]):
            entry_box.grid(row=i, column=j, sticky=tk.W, padx=5, pady=5)
            if i == 0:
                entry_box.insert(0, entries_names[k])
                k+=1
            elif i == 1 and j in [1,3,5,7]:
                entry_box.insert(0, entries_names[k])
                k+=1
            elif i == 2 and j in [1,3,5,7]:
                entry_box.insert(0, entries_names[k])
                k+=1
            elif i == 3 and j==1:
                entry_box.insert(0, entries_names[k])
                k+=1
        col+=1
    canvas.update()

    # checkbuttons
    corporate = tk.BooleanVar()
    WhyToUse = tk.BooleanVar()
    rms_slide = tk.BooleanVar()
    Comparison = tk.BooleanVar()
    corporate_label = tk.Checkbutton(settings_frame, text="Corporate Client Slide",background="#404040", font=("Arial",12),
                                   selectcolor="black",foreground="white", variable=corporate)
    corporate_label.grid(row=2, column=2, padx=5,sticky=tk.W)
    WhyToUse_label = tk.Checkbutton(settings_frame, text="Why to use?",background="#404040", font=("Arial",12),
                                   selectcolor="black",foreground="white", variable=WhyToUse)
    WhyToUse_label.grid(row=3, column=2, padx=5,sticky=tk.W)
    rms_label = tk.Checkbutton(settings_frame, text="RMS Slide",background="#404040", font=("Arial",12),
                                   selectcolor="black",foreground="white", variable=rms_slide)
    rms_label.grid(row=2, column=3, padx=5,sticky=tk.W)
    Comparison_label = tk.Checkbutton(settings_frame, text="Comparison Outcome",background="#404040", font=("Arial",12),
                                   selectcolor="black",foreground="white", variable=Comparison)
    Comparison_label.grid(row=3, column=3, padx=5,sticky=tk.W)
    deafult = tk.BooleanVar()
    deafult_label = tk.Checkbutton(settings_frame, text="Default range settings (+/- 10% from spot)?",background="#404040", 
                                   selectcolor="black",font=("Arial",12),foreground="white", variable=deafult)
    deafult_label.grid(row=3, column=6, columnspan=2, padx=5, sticky=tk.E)

    ########
    # GO GO GO!!
    # setting labels in 8th column
    Run = tk.Button(settings_frame, text="Generate",width=5, background="#007600", foreground="white", relief="flat",
                    padx=10, pady=5, highlightbackground="#007600", font=("Arial",12), 
                    command=lambda: run_pp(settings_frame,selected_options,selected_inputs,importer,entry_boxes))
    Run.grid(row=0, column=8, padx=10, pady=5, sticky=tk.W)
    ########

    global forward_var, parforward_var,on_chart_value
    forward_var = tk.BooleanVar()
    parforward_var = tk.BooleanVar()
    forward_label = tk.Checkbutton(settings_frame, text="FX Forward on chart?:",background="#404040", foreground="white",
                                   selectcolor="black",font=("Arial",12),variable=forward_var, command=on_checkbutton_toggle)
    forward_label.grid(row=1, column=8, padx=5,sticky=tk.S)
    parforward_label = tk.Checkbutton(settings_frame, text="Par Forward on chart?:",background="#404040", foreground="white",
                                      selectcolor="black",font=("Arial",12),variable=parforward_var, command=on_checkbutton_toggle)
    parforward_label.grid(row=2, column=8, padx=5,sticky=tk.N)
    on_chart_value = tk.Entry(settings_frame, bg='white', width=14, font=("Arial",12))
    on_chart_value.insert(0, "1.3555")

def on_checkbutton_toggle():
    if forward_var.get() or parforward_var.get():
        on_chart_value.grid(row=3, column=8, padx=5, sticky=tk.NE)
    else:
        on_chart_value.grid_forget()

# 3) __
# _____ code to show charts on button (eye icon) _________

def show_forward_on_button(importer,s, strike, lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = forward_fun(float(strike.get()), 1/float(lev.get())*100, importer, 
                                ch_min, ch_max, decimal_c)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_partyp_on_button(importer,s, strike, partyp):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = Partyp_fun(float(strike.get()), float(partyp.get()), importer, 
                                ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_collar_on_button(importer,s, lower, upper,lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = kor_fun(float(lower.get()), float(upper.get()), 1/float(lev.get())*100,
                      importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_optionR_on_button(importer,s, strike, premium, rebate_level, rebate):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    spot = float(entry_boxes2[0].get())
    array_= Eur_r_fun(float(strike.get()), float(rebate_level.get()), float(rebate.get()), 
                      100, float(premium.get()), spot, importer, ch_min, ch_max)
    chart = do_option_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_option_on_button(importer, s, strike, premium):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    spot = float(entry_boxes2[0].get())
    array_ = Eur_fun(float(strike.get()), 100, float(premium.get()), 
                     spot, importer, ch_min, ch_max)
    chart = do_option_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_spread_on_button(importer,s, lower, upper, premium):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    spot = float(entry_boxes2[0].get())
    array_ = Spread_fun(float(lower.get()), float(upper.get()), float(premium.get()),
                        spot, importer, ch_min, ch_max)
    chart = do_option_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_stepForw_on_button(importer,s, strike, reset,trigger, lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = forw_zrek_fun(float(strike.get()), -float(reset.get()), 1/float(lev.get())*100, float(trigger.get()), importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_stepCol_on_button(importer,s, lower,upper,reset,trigger, lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = kor_zrek_fun(float(lower.get()), float(upper.get()), float(trigger.get()), float(reset.get()), 
                          1/float(lev.get())*100, importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_convForw_on_button(importer,s, strike, trigger,lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = forw_elas_fun(float(strike.get()), float(trigger.get()), 1/float(lev.get())*100, importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_convCol_on_button(importer,s, lower,upper,trigger,lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = kor_elas_fun(float(lower.get()), float(upper.get()), float(trigger.get()), 1/float(lev.get())*100, importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_knockFrw_on_button(importer,s, strike, KO, lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = forw_zwyl_iwyp_fun(float(strike.get()), float(KO.get()), 
                                0, 1/float(lev.get())*100, importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_knockFrwSub_on_button(importer,s, strike, KO, Sub,lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = forw_zwyl_iwyp_fun(float(strike.get()), float(KO.get()), 
                                float(Sub.get()), 1/float(lev.get())*100, importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_knockCol_on_button(importer,s, lower,upper,KO, lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = kor_zwyl_iwyp_fun(float(lower.get()), float(upper.get()), float(KO.get()), 
                               0, 1/float(lev.get())*100, importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_knockColSub_on_button(importer,s, lower, upper,KO,Sub,lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = kor_zwyl_iwyp_fun(float(lower.get()), float(upper.get()), float(KO.get()), 
                               float(Sub.get()), 1/float(lev.get())*100, importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_capped_on_button(importer,s, lower,upper, lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    if importer: array_ = kor_mewa_fun(float(lower.get()), float(upper.get()), float(lower.get()), 1/float(lev.get())*100,
                           importer, ch_min, ch_max)
    if not importer: array_ = kor_mewa_fun(float(lower.get()), float(upper.get()), float(upper.get()), 1/float(lev.get())*100,
                           importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_loss_on_button(importer,s, lower,upper, lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    if importer: array_ = Kor_mewa_fun2(float(lower.get()), float(upper.get()), float(upper.get()), 1/float(lev.get())*100,
                           importer, ch_min, ch_max)
    if not importer: array_ = Kor_mewa_fun2(float(lower.get()), float(upper.get()), float(lower.get()), 1/float(lev.get())*100,
                           importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def show_seagull_on_button(importer,s, lower,mid,upper,lev):
    ch_min = float(entry_boxes4[0].get())
    ch_max = float(entry_boxes4[1].get())
    decimal_c = int(entry_boxes4[2].get())
    base = entry_boxes1[0].get()
    term = entry_boxes1[1].get()
    array_ = kor_mewa_fun(float(lower.get()), float(upper.get()), float(mid.get()), 1/float(lev.get())*100,
                           importer, ch_min, ch_max)
    chart = do_chart(s, base, term, ch_min, ch_max, decimal_c, array_)
    chart.ioff()
    chart.show()

def info_on_button(s, instruction,canvas):
    info_f = tk.Toplevel(canvas, background="black")
    info_f.title("Info")
    info_f.geometry(f"700x300")
    entry_label = tk.Label(info_f, text=s, font=("Arial",14), fg='white', bg="black")
    entry_label.pack(pady=10)
    entry_label = tk.Label(info_f, text=instruction, font=("Arial",12), fg='white', bg="black")
    entry_label.pack(pady=10, padx=(10,10))

