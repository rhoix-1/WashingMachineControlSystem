from tkinter import *

root = Tk()

# Input boxes
entry = Entry(root, width=50)
entry.pack()
entry.insert(0, "Enter Your Name: ")


def myClick():
    inputedName = "Hello " + entry.get()
    myLabel = Label(root, text=inputedName)
    myLabel.pack()

# "state=DISABLED" add that where the padx is to disable it
myButton = Button(root, text="Enter Your Name", command=myClick, fg="orange", bg="blue")
myButton.pack()

root.mainloop()