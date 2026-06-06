from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame
from tkinter import StringVar, OptionMenu
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Toplevel, Label
import numpy as np

#*****************************************************************************
# Requirments to run the project
# Libraries: Tkinter, Numpy, Matplotlib

# pip install numpy
# pip install matplotlib

# ******************************************************************************


row_counter = 1 
input_rows = [] 

result_windows = []

def add_more():
    global row_counter, input_rows
    
    row_elements = {}
    
    # START LENGTH ENTRY
    new_entry_start = Entry(
        window,
        bd=1,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    new_entry_start.place(x=152.0, y=516.0 + row_counter * 40, width=115.0, height=23.0)
    
    # END LENGTH ENTRY
    new_entry_end = Entry(
        window,
        bd=1,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    new_entry_end.place(x=515.0, y=516.0 + row_counter * 40, width=115.0, height=23.0)
    
    # LOAD ENTRY
    new_entry_load = Entry(
        window,
        bd=1,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    new_entry_load.place(x=850.0, y=516.0 + row_counter * 40, width=115.0, height=23.0)
    
    row_elements = {
        'start': new_entry_start,
        'end': new_entry_end,
        'load': new_entry_load
    }
    
    input_rows.append(row_elements)
    
    row_counter += 1

    if row_counter >= 5:
        button_3.config(state='disabled')

def calculate():
    beam_length = float(entry_1.get())
    
    loads = []
    start = float(entry_2.get())
    end = float(entry_4.get())
    magnitude = float(entry_6.get())
    loads.append((start, end, magnitude))
    
    # ADDITIONAL ROWS
    for row in input_rows:
        start = float(row['start'].get())
        end = float(row['end'].get())
        magnitude = float(row['load'].get())
        loads.append((start, end, magnitude))
    
    # RESULTS WINDOW
    results_window = Toplevel(window)
    results_window.state('zoomed') 
    results_window.title("SFD and BMD Plots")
    result_windows.append(results_window)

    #CALCULATIONS
    udl_to_point = []
    for st, en, magn in loads:
        position = (st + en)/2
        magni = magn*(en-st)
        udl_to_point.append((position, magni))
    
    reaction_force = sum(x[1] for x in udl_to_point)
    reaction_moment = -sum(x[0]*x[1] for x in udl_to_point)
    
    Label(results_window, 
          text=f"Reaction Force: {reaction_force:.2f} N\nReaction Moment: {reaction_moment:.2f} Nm",
          font=("SourceSerifPro Regular", 14)).pack(pady=10)
    

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
    plt.subplots_adjust(hspace=0.5)
    
    #SFD PLOT
    sf = reaction_force
    shear_forces_dict = {0: sf}
    for start, end, mag in loads:
        shear_forces_dict[start] = sf
        sf -= mag * (end - start)
        shear_forces_dict[end] = sf
    
    x_points_sf = np.linspace(0, beam_length, 200)
    y_points_sf = []
    
    for x in x_points_sf:
        current_sf = reaction_force
        for start, end, mag in loads:
            if x > end:
                current_sf -= mag * (end - start)
            elif x > start:
                current_sf -= mag * (x - start)
        y_points_sf.append(current_sf)
    
    line1, = ax1.plot(x_points_sf, y_points_sf, 'b-', linewidth=2)
    ax1.fill_between(x_points_sf, y_points_sf, 0, alpha=0.1)
    ax1.grid(True)
    ax1.set_title('Shear Force Diagram', pad=20)
    ax1.set_xlabel('Position along beam (m)')
    ax1.set_ylabel('Shear Force (N)')
    ax1.set_xticks(np.arange(0, beam_length + 1, 1))
    
    # BMD PLOT
    x_points = np.linspace(0, beam_length, 200)
    bm_values = []
    
    for x in x_points:
        moment = 0
        for start, end, mag in loads:
            if x <= start:
                length_of_load = end - start
                load_center = (start + end)/2
                total_load = mag * length_of_load
                moment += total_load * (load_center - x)
            elif x <= end:
                moment += mag * (end - x)**2 / 2
        bm_values.append(moment)
    
    line2, = ax2.plot(x_points, [-m for m in bm_values], 'r-', linewidth=2)
    ax2.fill_between(x_points, [-m for m in bm_values], 0, alpha=0.1)
    ax2.grid(True)
    ax2.set_title('Bending Moment Diagram', pad=20)
    ax2.set_xlabel('Position along beam (m)')
    ax2.set_ylabel('Bending Moment (Nm)')
    ax2.set_xticks(np.arange(0, beam_length + 1, 1))
    
    #HOVER FUNCTION
    annot1 = ax1.annotate("", xy=(0,0), xytext=(10,10),
    textcoords="offset points",
    bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9),
    arrowprops=dict(arrowstyle="->"))
    annot1.set_visible(False)

    annot2 = ax2.annotate("", xy=(0,0), xytext=(10,10),
    textcoords="offset points",
     bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9),
    arrowprops=dict(arrowstyle="->"))
    annot2.set_visible(False)

    def update_annot(line, annot, ind):
        x, y = line.get_data()
        annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
        text = f'x: {x[ind["ind"][0]]:.2f}m\ny: {y[ind["ind"][0]]:.2f}'
        annot.set_text(text)

    def hover(event):
        if event.inaxes == ax1:
            cont, ind = line1.contains(event)
            annot = annot1
            line = line1
        elif event.inaxes == ax2:
            cont, ind = line2.contains(event)
            annot = annot2
            line = line2
        else:
            return

        if cont:
            update_annot(line, annot, ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if annot1.get_visible():
                annot1.set_visible(False)
            if annot2.get_visible():
                annot2.set_visible(False)
            fig.canvas.draw_idle()

    plt.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=results_window)
    canvas.draw()
    
    fig.canvas.mpl_connect("motion_notify_event", hover)
    
    canvas.get_tk_widget().pack(pady=10)

def exit_program():
    plt.close('all')
    window.quit()
    window.destroy()

window = Tk()
window.geometry("1134x800")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1090,
    width = 1134,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    18.0,
    21.0,
    1115.0,
    1069.0,
    fill="#E8E8E8",
    outline="")

canvas.create_rectangle(
    26.0,
    28.0,
    1108.0,
    174.0,
    fill="#725959",
    outline="")

canvas.create_text(
    42.0,
    53.0,
    anchor="nw",
    text="Problem Statement:",
    fill="#FFFFFF",
    font=("Inter", 21 * -1)
)

canvas.create_text(
    42.0,
    85.0,
    anchor="nw",
    text="To develop a gernalised computer program for generation of support reactions, SFD and BMD\nof cantilever beam subjected to different UDLs ot different locations over the length of beam.",
    fill="#FFFFFF",
    font=("Inter", 25 * -1)
)

canvas.create_rectangle(
    323.0,
    198.0,
    353.0,
    280.0,
    fill="#EB1215",
    outline="")

canvas.create_rectangle(
    353.0,
    224.0,
    868.0,
    254.0,
    fill="#5A44A4",
    outline="")

canvas.create_rectangle(
    320.99999475463255,
    182.0,
    322.0,
    303.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    307.9999996863278,
    185.0,
    322.0,
    199.00000031367222,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    307.9999996863278,
    215.0,
    322.0,
    229.00000031367222,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    307.9999996863278,
    245.0,
    322.0,
    259.0000003136722,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    307.9999996863278,
    275.0,
    322.0,
    289.0000003136722,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    307.9999996863278,
    200.0,
    322.0,
    214.00000031367222,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    307.9999996863278,
    230.0,
    322.0,
    244.00000031367222,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    307.9999996863278,
    260.0,
    322.0,
    274.0000003136722,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    307.9999996863278,
    290.0,
    322.0,
    304.0000003136722,
    fill="#000000",
    outline="")

canvas.create_text(
    377.0,
    354.0,
    anchor="nw",
    text="Enter the Length of the Beam:",
    fill="#000000",
    font=("SourceSerifPro Regular", 22 * -1)
)

canvas.create_text(
    738.0,
    354.0,
    anchor="nw",
    text="m",
    fill="#000000",
    font=("SourceSerifPro Regular", 22 * -1)
)

canvas.create_text(
    373.0,
    420.0,
    anchor="nw",
    text="Default unit of Length: 'm' and Weight: 'N'",
    fill="#000000",
    font=("SourceSerifPro Regular", 22 * -1)
)

canvas.create_text(
    150.0,
    480.0,
    anchor="nw",
    text="Start point of load",
    fill="#000000",
    font=("SourceSerifPro Regular", 16 * -1)
)

canvas.create_text(
    515.0,
    480.0,
    anchor="nw",
    text="End point of load",
    fill="#000000",
    font=("SourceSerifPro Regular", 16 * -1)
)

canvas.create_text(
    830.0,
    480.0,
    anchor="nw",
    text="Magnitude of load (in N/m)",
    fill="#000000",
    font=("SourceSerifPro Regular", 16 * -1)
)




# Beam length input
entry_1 = Entry(
    window,
    bd=1, 
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=683.0,
    y=354.0,
    width=40.0,
    height=23.0
)

# Start Length input
entry_2 = Entry(
    window,
    bd=1,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=152.0,
    y=516.0,
    width=115.0,
    height=23.0
)

# End Length input
entry_4 = Entry(
    window,
    bd=1,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=515.0,
    y=516.0,
    width=115.0,
    height=23.0
)

# Load input
entry_6 = Entry(
    window,
    bd=1,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_6.place(
    x=850.0,
    y=516.0,
    width=115.0,
    height=23.0
)

button_1 = Button(
    window,
    text="Calculate",
    borderwidth=1,
    highlightthickness=0,
    command=calculate,
    relief="flat",
    bg="#FFFFFF",
    fg="#000716",
    font=("SourceSerifPro Regular", 12)
)
button_1.place(
    x=527.0,
    y=740.0,
    width=81.0,
    height=26.0
)

button_2 = Button(
    window,
    text="Exit",
    borderwidth=1,
    highlightthickness=0,
    command=exit_program,
    relief="flat",
    bg="#FFFFFF",
    fg="#000716",
    font=("SourceSerifPro Regular", 12)
)
button_2.place(
    x=119.0,
    y=740.0,
    width=97.0,
    height=26.0
)
button_3 = Button(
    window,
    text="Add More",
    borderwidth=1,
    highlightthickness=0,
    command=add_more,
    relief="flat",
    bg="#FFFFFF",
    fg="#000716",
    font=("SourceSerifPro Regular", 12)
)
button_3.place(
    x=923.0,
    y=740.0,
    width=97.0,
    height=26.0
)

window.resizable(False, False)
window.mainloop()
