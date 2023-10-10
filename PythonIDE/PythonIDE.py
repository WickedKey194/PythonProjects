import subprocess
import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import sys
import tkinter as tk #pentru "Text Editor" sa deschida o noua fereastra
from tkinter import filedialog #pentru butonul "Save" de la Text Editor


root = Tk()
root.title("Python IDE")
root.geometry("1280x720+10+10")
root.configure(bg="#323846")
root.resizable(False, False)


label = Label(root, bg="#323846")
label.place(x=180, y=0)


file_path = ''

def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    global file_path, label
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        code_input.delete('1.0', END)
        code_input.insert('1.0', code)
        file_path = path
        
    file_name = os.path.basename(path)
    #label = Label(root, text=file_name, bg="cyan")
    #label.place(x=180, y=0)
    label.config(text=file_name)
    label.config(bg="cyan")
    
    
def save():
    global file_path, label
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
        
    with open(path, 'w') as file:
        code = code_input.get('1.0', END)
        file.write(code)
        set_file_path(path)
        
    file_name = os.path.basename(path)
    #print(file_name)
    #label = Label(root, text=file_name, bg="cyan")
    #label.place(x=180, y=0)
    label.config(text=file_name)
    label.config(bg="cyan")


'''   
def save_whiteboard():
    path = asksaveasfilename(filetypes=[('PNG', '*.png')])
    canvas.postscript(file=path, colormode='color')
'''
    
def run():
    global file_path, label
    if file_path == '':
        messagebox.showerror("Python IDE Request Window", "Please save your code before running.")
        return
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0', error)
    
    path=file_path #daca nu puneam aceasta linie de cod, mi-ar fi functionat la fel de bine codul, dar imi dadea eroare ca nu gaseste sau ca "path" nu este definit
    file_name = os.path.basename(path)
    #print(file_name)
    #label = Label(root, text=file_name, bg="cyan")
    #label.place(x=180, y=0)
    label.config(text=file_name)
    label.config(bg="cyan")



def on_closing():
    if messagebox.askyesnocancel("Python IDE Request Window", "Do you want to save your work before exiting?"):
        save()
    root.destroy()
    

def open_whiteboard():
    whiteboard = Toplevel(root)
    whiteboard.title("Whiteboard")
    whiteboard.geometry("800x600+700+100")
    whiteboard.resizable(False, False)

    canvas = Canvas(whiteboard, bg="white")
    canvas.place(x=0, y=0, width=800, height=600)

    def draw(event):
        x, y = event.x, event.y
        canvas.create_line(x, y, x+1, y+1)
    
    canvas.bind("<B1-Motion>", draw)
    
    
def open_text_editor():
    text_editor = tk.Toplevel(root)
    text_editor.title("Text Editor")
    text_editor.geometry("500x500+18+50")
    
    text_area = tk.Text(text_editor)
    text_area.pack(fill='both', expand=True)
    
    save_button = tk.Button(text_editor, text="Save", background="lightgreen", activebackground="green", command=lambda: save_file_TE(text_area)) #comanda pentru a accesa functia cu tot cu parametrii
    save_button.pack(side='right')
  
    
def save_file_TE(text_area):
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if file is None:
        return
    text = text_area.get("1.0", "end-1c")
    file.write(text)
    file.close()
    #daca nu puneam "def save_file_TE(text_area):", programul imi dadea eroare pentru ca "text_area" nu este definit, dar el era deja definit in functia "open_text_filr()"
  

def on_closing1():
    if messagebox.askokcancel("Warning Window", "Do you want to quit?"):
        root.destroy()


def highlight_line(event):
    code_input.tag_remove("active_line", 1.0, "end")
    code_input.tag_add("active_line", "insert linestart", "insert lineend+1c")
    code_input.tag_config("active_line", background="#AEB1B1")


def update_line_numbers(event):
    txt = event.widget
    txt.update_idletasks()
    lineno = txt.index("@0,0").split(".")[0]
    lineend = txt.index("end-1c")
    lines = int(lineend.split(".")[0]) - int(lineno)
    line_number_bar.config(state="normal")
    line_number_bar.delete("1.0", "end")
    line_number_bar.insert("end", "\n".join(str(i) for i in range(1, lines + 1)))
    line_number_bar.config(state="disabled")
    

def NEW():
    global file_path, label
    code_input.delete('1.0', END)
    code_output.delete('1.0', END)
    file_path = ''
    if label:
        label.config(text="")
        label.config(bg="#323846")



#icon
image_icon = PhotoImage(file="logo.png")
root.iconphoto(False, image_icon)

#code input
code_input = Text(root, font="consolas 18", bg="#EAEAEA", wrap="word")
code_input.place(x=180, y=20, width=680, height=720)

#output code
code_output = Text(root, font="consolas 15", bg="#323846", fg="cyan")
code_output.place(x=860, y=0, width=420, height=720)
#code_output.config(state="disabled")

#buttons
Open = PhotoImage(file="open.png")
Save = PhotoImage(file="save.png")
Run = PhotoImage(file="run.png")
EXIT = PhotoImage(file="EXIT.png")
WB = PhotoImage(file="WhiteBoard.png")
#SaveWB = PhotoImage(file="SaveWB.png")
TE = PhotoImage(file="TextEditor.png")
new = PhotoImage(file="new.png")

Button(root, image=Open, bg="#323846", bd=0, command=open_file).place(x=30, y=30)
Button(root, image=Save, bg="#323846", bd=0, command=save).place(x=30, y=145)
Button(root, image=Run, bg="#323846", bd=0, command=run).place(x=30, y=260)
Button(root, image=EXIT, bg="#323846", bd=0, command=on_closing).place(x=30, y=650)
Button(root, image=WB, bg="#323846", bd=0, command=open_whiteboard).place(x=30, y=510)
#Button(root, image=SaveWB, bg="white", bd=0, command=save_whiteboard).place(x=20, y=20)
Button(root, image=TE, bg="#323846", bd=0, command=open_text_editor).place(x=30, y=390)
Button(root, image=new, bg="#323846", bd=0, command=NEW).place(x=30, y=580)

#ask if i want to quit/exit the program
root.protocol("WM_DELETE_WINDOW", on_closing1)

#highline of my current line of code
code_input.bind("<Motion>", highlight_line)
code_input.bind("<Key>", highlight_line)

#indentation + scrollbar la code_input
scrollbar = tk.Scrollbar(root, command=code_input.yview)
scrollbar.pack(side="left", fill="y")
code_input.config(yscrollcommand=scrollbar.set)

line_number_bar = tk.Text(root, width=10000, font="consolas 18", bg="#323846", state="disabled", fg="#58F9F9")
line_number_bar.pack(side="left", fill="y")
line_number_bar.place(x=147, y=20, width=30, height=720)

code_input.bind("<Any-KeyRelease>", update_line_numbers)
code_input.bind("<Button-1>", update_line_numbers)


root.mainloop()