import tkinter as tk
window = tk.Tk()


label = tk.Label(
    text="Hello, Tkinter",
    fg="white",  # Set the text color to white
    bg="black",
    width = 10,
    height = 5# Set the background color to black
)

label.pack()


button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)
button.pack()


window.mainloop()

