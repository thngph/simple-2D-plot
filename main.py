from tkinter import *

from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
)
import numpy as np
from numpy import ones,vstack
from numpy.linalg import norm, lstsq

root = Tk()

def on_closing():
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		root.destroy()
		root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("Distance of two lines")

dtext = StringVar()


def parser(string):
	return list(map(lambda x: float(x), string.split(",")))[:2]

def dir_vector(point_1, point_2):
    return [x - y for x,y in zip(point_1, point_2)]
	
def distance(p1,p2,p3):
	p1 = np.array(p1)
	p2 = np.array(p2)
	p3 = np.array(p3)
	return np.abs(norm(np.cross(p2-p1, p1-p3)))/norm(p2-p1)

def is_parallel(u1, u2):
	return np.dot(u1,u2)/(norm(u1)*norm(u2)) == 1

def is_on(p1, p2, p3):
	x_coords, y_coords = zip(*(p1,p2))
	A = vstack([x_coords,ones(len(x_coords))]).T
	m, c = lstsq(A, y_coords, rcond=None)[0]
	return p3[1] == ((m * p3[0]) + c)

def draw(p1,p2,ax,d):
  x, y= [p1[0], p2[0]], [p1[1], p2[1]]
  t = np.arange(0,1)

  ax.scatter(x, y, c='black', s=100)
  ax.plot(x,y, c=np.random.rand(3,), label=f'd{d}')
  #ax.plot(p1[0] + t*(p2[0] - p1[0]), p1[1] + t*(p2[1] - p1[1]), p1[2] + t*(p2[2] - p1[2]), c=np.random.rand(3,), label=f'd{d}')
  ax.legend()


def calc():
	try:
		p1 = parser(P1.get())
		p2 = parser(P2.get())
		p3 = parser(P3.get())
		p4 = parser(P4.get())
	except:
		dtext.set("Invalid input")
		return
	finally:
		if len(p1) != 2 or len(p2) != 2 or len(p3) != 2 or len(p4) != 2:
			dtext.set("Invalid input length")
			return
		
	u1 = dir_vector(p1, p2)
	u2 = dir_vector(p3, p4)
	
	if not is_parallel(u1, u2):
		dtext.set("Distance: 0 (intersect)")
	elif is_on(p1,p2,p3):
		dtext.set("Distance: 0 (overlap)")
	else:
		dtext.set("Distance: " + "%.5f" %distance(p1,p2,p3))
	fig = plt.figure()
	ax = plt.axes(projection ='3d')
	draw(p1,p2,ax,1)
	draw(p3,p4,ax,2)
	canvas = FigureCanvasTkAgg(fig, master=root)
	canvas.draw()
	canvas.get_tk_widget().grid(row=7, column=0, ipadx=10, ipady=10)


L1 = Label(root, font=('arial', 18, 'bold'),text="1st point").grid(row=0, column=0, padx=10, pady=10)
P1 = Entry(root, font=('arial', 20, 'bold'), 
		text="point 1", width=10,bg="#eee", bd=0, justify=RIGHT)
P1.grid(row=0, column=1, padx=10, pady=10)

L2 = Label(root, font=('arial', 18, 'bold'), text="2nd point").grid(row=1, column=0)
P2 = Entry(root, font=('arial', 20, 'bold'), 
		text="point 2", width=10,bg="#eee", bd=0, justify=RIGHT)
P2.grid(row=1, column=1, padx=10, pady=10)

L3 = Label(root, font=('arial', 18, 'bold'), text="3rd point").grid(row=2, column=0)
P3 = Entry(root, font=('arial', 20, 'bold'),
		text="point 3", width=10,bg="#eee", bd=0, justify=RIGHT)
P3.grid(row=2, column=1, padx=10, pady=10)

L4 = Label(root, font=('arial', 18, 'bold'), text="4th point").grid(row=3, column=0)
P4 = Entry(root, font=('arial', 20, 'bold'),
		text="point 4", width=10,bg="#eee", bd=0, justify=RIGHT)
P4.grid(row=3, column=1, padx=10, pady=10)

B = Button(root, text = "Plot", command =calc)
B.grid(row=4, columnspan=4)

input_field = Label(root, font=('arial', 18, 'bold'), textvariable=dtext, width=20, bg="#eee", bd=0, justify=RIGHT)
input_field.grid(row=5, columnspan=2,padx=10)

root.mainloop()
