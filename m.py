import tkinter as tk
import pickle
import numpy as np



# create the GUI interface
root = tk.Tk()
root.title('Linear Regression Model')

# create the input fields
x_label = tk.Label(root, text='X:')
x_label.grid(row=0, column=0)
x_entry = tk.Entry(root)
x_entry.grid(row=0, column=1)

# create the output field
y_label = tk.Label(root, text='Y:')
y_label.grid(row=1, column=0)
y_output = tk.Label(root, text='')
y_output.grid(row=1, column=1)


predict_button = tk.Button(root, text='Predict')
predict_button.grid(row=2, column=0, columnspan=2)

root.mainloop()
