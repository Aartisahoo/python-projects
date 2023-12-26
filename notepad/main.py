from tkinter import *
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

def newfile():
    global file
    root.title("Untitled-Notepad")
    file=None
    TextArea.delete(1.0, END)
def openfile():
    global file
    file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if file == "":
        file= None
    else:
        root.title(os.path.basename(file)+ "- Notepad")
        TextArea.delete(1.0,END)
        f=open(file,"r")
        TextArea.insert(1.0, f.read())
        f.close()


def savefile():
    global file
    if file==None:
        file = asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt", filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])
        if file=="":
            file=None
        else:
            f=open(file,"w")
            f.write(TextArea.get(1.0,END))
            f.close()

            root.title(os.path.basename(file)+ "-Notepad")
            f=open(file,"w")
            f.write(TextArea.get(1.0,END))
            f.close()

def cut():
    TextArea.event_generate(("<<Cut>>"))
def copy():
    TextArea.event_generate(("<<Copy>>"))
def paste():
    TextArea.event_generate(("<<Paste>>"))
def about():
    showinfo("Notepad","Notepad by Aarti")

if __name__ == "__main__":
    root = Tk()
    root.title("Untitled-Notepad")
    img = Image.open(r"notepad\ntpdic.png")
    root.iconphoto(False, ImageTk.PhotoImage(img))
    root.geometry("500x400")

    TextArea = Text(root, font="lucida 13") #adding TextArea to write text
    file=None #initially file is none
    TextArea.pack(expand=True, fill=BOTH) #packing TextArea

    menu=Menu(root) #creating menu bar
    filemenu=Menu(menu, tearoff=0) #creating file menu
    # adding file fns
    filemenu.add_command(label="New", command=newfile) #adding new file option
    filemenu.add_command(label="Open", command=openfile) #adding open file option
    filemenu.add_command(label="Save", command=savefile) #adding save file option
    filemenu.add_separator() #adding separator
    filemenu.add_command(label="Exit", command=root.quit) #adding exit option
    menu.add_cascade(label="File", menu=filemenu) #adding file menu to menu bar

    editmenu=Menu(menu, tearoff=0) #creating edit menu
    # adding edit fn
    editmenu.add_command(label="Cut", command=cut) #adding cut option
    editmenu.add_command(label="Copy", command=copy) #adding copy option
    editmenu.add_command(label="Paste", command=paste) #adding paste option
    menu.add_cascade(label="Edit", menu=editmenu) #adding edit menu to menu bar
    
    helpmenu=Menu(menu, tearoff=0) #creating help menu
    # adding help fn
    helpmenu.add_command(label="About Notepad", command=about) #adding about option
    menu.add_cascade(label="Help", menu=helpmenu) #adding help menu to menu bar

    
    root.config(menu=menu) #configuring menu bar
    Scroll = Scrollbar(TextArea) #adding scrollbar
    Scroll.pack(side=RIGHT, fill=Y) #packing scrollbar
    Scroll.config(command=TextArea.yview) #configuring scrollbar
    TextArea.config(yscrollcommand=Scroll.set) #configuring TextArea


    root.mainloop()