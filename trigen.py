import itertools

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.patches import Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
min_side_length = 1
max_side_length = 10
def generate_triangle_lists():
    global scalene_triangles, right_triangles
    scalene_triangles = [t for t in itertools.combinations_with_replacement(range(min_side_length, max_side_length + 1), 3) if sum(t) > 2 * max(t)]
    right_triangles = [t for t in itertools.combinations_with_replacement(range(min_side_length, max_side_length + 1), 3) if max(t)**2 == sum(x**2 for x in t if x != max(t))]

generate_triangle_lists()

# Initialize the mode, index, and filter
mode = 'scalene'
index = 0
filter = 'both'
# Initialize the side length and angle filters
side_filters = [None, None, None]


def calculate_angle(t, i):
    a, b, c = t
    if i == 0:
        return sp.acos((b**2 + c**2 - a**2) / (2 * b * c))
    elif i == 1:
        return sp.acos((a**2 + c**2 - b**2) / (2 * a * c))
    elif i == 2:
        return sp.acos((a**2 + b**2 - c**2) / (2 * a * b))

def set_side_filter(i, value):
    global side_filters
    try:
        side_filters[i] = int(value)
    except ValueError:
        side_filters[i] = None
    draw_triangle()



def filter_triangles(triangles):
    # Filter out triangles that don't satisfy the triangle inequality theorem
    triangles = [t for t in triangles if t[0] + t[1] >= t[2] and t[0] + t[2] >= t[1] and t[1] + t[2] >= t[0]]
    if filter == 'acute':
        triangles = [t for t in triangles if max(t)**2 < sum(x**2 for x in t if x != max(t))]
    elif filter == 'obtuse':
        triangles = [t for t in triangles if max(t)**2 > sum(x**2 for x in t if x != max(t))]
    for i in range(3):
        if side_filters[i] is not None:
            triangles = [t for t in triangles if t[i] == side_filters[i]]
    return triangles


def update_index_entry():
    global index
    # Update the index entry with the current index
    index_entry.delete(0, tk.END)
    index_entry.insert(0, f"{index + 1}")
    
def set_index():
    global index
    # Get the index from the Entry widget and update the triangle
    try:
        new_index = int(index_entry.get().split(' ')[0]) - 1
        triangles = filter_triangles(scalene_triangles if mode == 'scalene' else right_triangles)
        if 0 <= new_index < len(triangles):
            index = new_index
            draw_triangle()
        else:
            update_index_entry()  # Reset the Entry widget if the input is out of range
    except ValueError:
        update_index_entry()  # Reset the Entry widget if the input is not a valid integer

def draw_triangle():
    global index
    root.focus()

    # Clear the previous plot
    ax.clear()

    

    # Select one of the triangles based on the mode, index, and filter
    triangles = filter_triangles(scalene_triangles if mode == 'scalene' else right_triangles)


    if not triangles:
        canvas.draw()
        index_label.config(text='No possible triangles')
        return

    a, b, c = triangles[index]

    # Calculate the angles of the triangle
    angle_A = sp.acos((b**2 + c**2 - a**2) / (2 * b * c))
    angle_B = sp.acos((a**2 + c**2 - b**2) / (2 * a * c))
    angle_C = sp.acos((a**2 + b**2 - c**2) / (2 * a * b))

    # Calculate the coordinates of the vertices
    vertex_A = (0, 0)
    vertex_B = (a, 0)
    vertex_C = (b * np.cos(float(angle_C)), b * np.sin(float(angle_C)))

    # Draw the triangle with colored sides
    triangle_AB = Polygon([vertex_A, vertex_B], closed=None, fill=None, edgecolor='r',linewidth=line_width.get())
    triangle_BC = Polygon([vertex_B, vertex_C], closed=None, fill=None, edgecolor='g',linewidth=line_width.get())
    triangle_CA = Polygon([vertex_C, vertex_A], closed=None, fill=None, edgecolor='b',linewidth=line_width.get())
    ax.add_patch(triangle_AB)
    ax.add_patch(triangle_BC)
    ax.add_patch(triangle_CA)

    # Display the measures of the sides and angles in their corresponding colors
    label_a.config(text=f'a={a}\nA={sp.deg(angle_A).evalf():.2f}')
    label_b.config(text=f'b={b}\nB={sp.deg(angle_B).evalf():.2f}')
    label_c.config(text=f'c={c}\nC={sp.deg(angle_C).evalf():.2f}')

    # Set the limits of the axes with a margin
    ax.set_xlim(-1, max(a, b, c) + 3)
    ax.set_ylim(-3, max(a, b, c) + 2)

    ax.axis('equal')  # Ensure the aspect ratio is correct

    # Redraw the plot
    canvas.draw()

    update_index_entry()
    
    # Update the index label
    index_label.config(text=f'Triangle {index + 1} of {len(triangles)}')

def set_mode(new_mode):
    global mode, index
    mode = new_mode
    index = 0  # Reset the index when the mode changes
    draw_triangle()

def change_index(delta):
    global index
    triangles = filter_triangles(scalene_triangles if mode == 'scalene' else right_triangles)
    index = (index + delta) % len(triangles)  # Use modulo to wrap around the list
    draw_triangle()

def set_filter(new_filter):
    global filter, index
    filter = new_filter
    index = 0  # Reset the index when the filter changes
    draw_triangle()

entry_sides = []
entry_angles = []

def generate_triangles():
    global index, min_side_length, max_side_length, scalene_triangles, right_triangles
    index = 0  # Reset the index
    
    min_input = entry_min_side_length.get()
    max_input = entry_max_side_length.get()
    
    if min_input:
        try:
            min_side_length = int(min_input)
        except ValueError:
            min_side_length = 1
            print("Invalid input for min side length. Using default value of 1.")
    else:
        min_side_length = 1
        print("No input for min side length. Using default value of 1.")
    
    if max_input:
        try:
            max_side_length = int(max_input)
        except ValueError:
            max_side_length = 10
            print("Invalid input for max side length. Using default value of 10.")
    else:
        max_side_length = 10
        print("No input for max side length. Using default value of 10.")
    
    # Regenerate triangle lists
    generate_triangle_lists()
    
    for i in range(3):
        set_side_filter(i, entry_sides[i].get())
    draw_triangle()
# Create a Tkinter window
root = tk.Tk()
line_width = tk.DoubleVar(value=1)
# Create a matplotlib figure and a canvas to draw on
fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the size as needed
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0)  # Use grid instead of pack

# Create a parent frame to contain all the other frames
frame_parent = tk.Frame(root)
frame_parent.grid(row=1, column=0)  # Use grid instead of pack

# Create frames for the filter buttons, navigation buttons, and mode buttons
frame_filter = tk.Frame(frame_parent)
frame_filter.pack(side=tk.LEFT, padx=20)
frame_nav = tk.Frame(frame_parent)
frame_nav.pack(side=tk.LEFT, padx=20,pady=10)
frame_jump = tk.Frame(frame_nav)
frame_jump.pack(side=tk.BOTTOM, padx=20, pady=20)
frame_jump_to = tk.Frame(frame_jump)
frame_jump_to.pack(side=tk.BOTTOM, pady= 10)
frame_mode = tk.Frame(frame_parent)
frame_mode.pack(side=tk.LEFT, padx=20)

# Add buttons for changing the filter
button_acute = tk.Button(master=frame_filter, text="Acute filter", command=lambda: set_filter('acute'))
button_acute.pack(side=tk.TOP)
button_obtuse = tk.Button(master=frame_filter, text="Obtuse filter", command=lambda: set_filter('obtuse'))
button_obtuse.pack(side=tk.TOP)
button_both = tk.Button(master=frame_filter, text="Both filter", command=lambda: set_filter('both'))
button_both.pack(side=tk.TOP)

# Add a label to display the current index and buttons for navigating through the list of triangles
button_prev = tk.Button(master=frame_nav, text="Previous triangle", command=lambda: change_index(-1))
button_prev.pack(side=tk.LEFT)
index_label = tk.Label(master=frame_nav)
index_label.pack(side=tk.LEFT)
button_next = tk.Button(master=frame_nav, text="Next triangle", command=lambda: change_index(1))
button_next.pack(side=tk.LEFT)
# Add a label and an Entry widget to display and change the current index
button_set_index = tk.Button(master=frame_jump_to, text="Go to triangle", command=set_index)
button_set_index.pack(side=tk.BOTTOM)

index_entry = tk.Entry(master=frame_jump)
index_entry.pack(side=tk.BOTTOM)

# Add buttons for changing the mode
button_scalene = tk.Button(master=frame_mode, text="Scalene mode", command=lambda: set_mode('scalene'))
button_scalene.pack(side=tk.TOP)
button_right = tk.Button(master=frame_mode, text="Right mode", command=lambda: set_mode('right'))
button_right.pack(side=tk.TOP)

# Create a frame for the labels
frame_labels = tk.Frame(root)
frame_labels.grid(row=0, column=1)  # Use grid instead of pack

# Add labels for the sides and angles
label_a = tk.Label(master=frame_labels, text="", bg="red", fg="white")
label_a.pack(side=tk.TOP)
label_b = tk.Label(master=frame_labels, text="", bg="green", fg="white")
label_b.pack(side=tk.TOP)
label_c = tk.Label(master=frame_labels, text="", bg="blue", fg="white")
label_c.pack(side=tk.TOP)
# Add a slider for the line width
slider_line_width = ttk.Scale(master=frame_labels, from_=1, to=10, variable=line_width, command=lambda _: draw_triangle())
slider_line_width.pack(side=tk.BOTTOM)

for i, color in enumerate(['red', 'green', 'blue']):
    frame_filter = tk.Frame(frame_labels, bg=color)
    frame_filter.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
    label_side = tk.Label(master=frame_filter, text="Side length:")
    label_side.pack(side=tk.LEFT)
    entry_side = tk.Entry(master=frame_filter)
    entry_side.pack(side=tk.LEFT)
    entry_sides.append(entry_side)


button_generate = tk.Button(master=frame_labels, text="Generate", command=generate_triangles)
button_generate.pack(side=tk.BOTTOM)

frame_side_length = tk.Frame(frame_labels)
frame_side_length.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
label_min_side_length = tk.Label(master=frame_side_length, text="Min side length:")
label_min_side_length.pack(side=tk.LEFT)
entry_min_side_length = tk.Entry(master=frame_side_length)
entry_min_side_length.pack(side=tk.LEFT)
label_max_side_length = tk.Label(master=frame_side_length, text="Max side length:")
label_max_side_length.pack(side=tk.LEFT)
entry_max_side_length = tk.Entry(master=frame_side_length)
entry_max_side_length.pack(side=tk.LEFT)
    

# Draw the initial triangle
draw_triangle()

tk.mainloop()