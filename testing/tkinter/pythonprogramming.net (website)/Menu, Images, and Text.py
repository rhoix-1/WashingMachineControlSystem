from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
    def init_window(self):
        self.master.title("GUI")
        # Tkinter adding padding by default and this expands and fills everything in 
        self.pack(fill=BOTH, expand=YES)

        '''
        quitButton = Button(self, text="Quit", command=self.client_exit)
        quitButton.place(x=0, y=0)
        '''

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Show Image", command=self.show_image)
        edit.add_command(label="Show Text", command=self.show_text)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)

    def show_image(self):
        load = Image.open("hi.gif")
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    def show_text(self):
        text = Label(self, text="hi, i'm steve")
        text.pack()

    def client_exit(self):
        exit()

root = Tk()
root.geometry("400x300")

app = Window(root)

root.mainloop()