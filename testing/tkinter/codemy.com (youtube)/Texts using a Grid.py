from tkinter import *

root = Tk()

# Creating a Label Widget
myLabel1 = Label(root, text="Hello World!")
myLabel2 = Label(root, text="My Name Is Josepher Shunaula")
# "Packs" it onto the screen
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=5)
'''
# You can also do this, but keep it cleaner using the first way
myLabel1 = Label(root, text="Hello World!").grid(row=0, column=0)
myLabel2 = Label(root, text="My Name Is Josepher Shunaula").grid(row=1, column=5)
'''

root.mainloop()