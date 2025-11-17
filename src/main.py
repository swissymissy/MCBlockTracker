import os
from mcstructure import Block, Structure
import csv
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# let user browse files and pick one
def browse_file():
    file_path = filedialog.askopenfilename()
    # user cancelled
    if not file_path:
        return
    parsing_file(file_path)

# parsing the input file
def parsing_file(input_file):
    p = Path(input_file)

    # case: the input file is not .mcstructure file
    if p.suffix != ".mcstructure":
        messagebox.showerror("Invalid File", "This does not apprear to be a valid .mcstructure file")
        print("Must be .mcstructure file")
        return None
    
    try:
        with open(input_file, "rb") as f: # read binary mode
            struct = Structure.load(f)
    except Exception:
        messagebox.showerror("Invalid File", text="This does not apprear to be a valid .mcstructure file")
        print ("Could not parse file. This does not appear to be a valid .mcstructure file")
        return
    
    layers = struct.get_structure() #numpy array of structure

    mat_dic = {} # material dictionary
    for layer in layers:
        for row in layer:
            for block in row:
                if block.name == 'air' or block.name == 'water' or block.name == 'structure_block':
                    continue # skip
                if block.name in mat_dic:
                    total , stacks , remain = mat_dic[block.name]
                    total += 1
                    stacks = total // 64
                    remain = total % 64
                    mat_dic[block.name] = (total, stacks, remain)
                else:
                    mat_dic[block.name] = (1,0,1) # total, stacks, remain

    # sort by alphabet order
    output = sorted(mat_dic.items())
    print(output)

    # creating output folder and output name 
    output_folder = os.path.abspath("../output")
    os.makedirs(output_folder, exist_ok=True) # make output folder if not exist
    output_name = p.stem+".csv"
    output_path = os.path.join(output_folder,output_name)

    # writing to output folder
    with open(output_path, "w" , newline='') as f:
        csvfile = csv.writer(f)

        csvfile.writerow(["Block_name", "Total Count", "Stacks", "Remain"]) # header row
        for block_name, (total, stacks, remain) in output:
            csvfile.writerow([block_name, total, stacks, remain])           # write row by row
    
    messagebox.showinfo(title="Success!", message=f"Output is saved in {output_path}")


def main():
    # open a window 
    window = tk.Tk()
    window.title("Minecraft Block Tracker")
    window.minsize(300,300)
    window.maxsize(500,500)

    # adding a fox icon
    icon = tk.PhotoImage(file="mc_fox.png")
    window.iconphoto(True, icon)

    # adding a cat background
    back_ground = tk.PhotoImage(file="mc_cat.png")
    window.bg_image = back_ground   # prevent garbage-collector collect it
    bg_label = tk.Label(window, image=back_ground)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # create labels, button
    tk.Label(
        window,
        text="Select an exported file from Minecraft:",
        bg="white",
        highlightbackground="black",
        highlightthickness=1).grid(column=0,row=0)
    tk.Label(
        window,
        text="Expand window to see cat. Thank you!",
        bg="white",
        highlightbackground="black",
        highlightthickness=1).grid(column=0, row=3)
    tk.Button(
        window,
        text="Browse file",
        command=browse_file,
        bg="white",
        highlightbackground="black",
        highlightthickness=2).grid(column=0,row=2)

    # keep the window open (infinite loop)
    window.mainloop()

if __name__ == "__main__":
    main()
