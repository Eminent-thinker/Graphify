import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import math
import json
import time, os


class MoveDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Enter X coordinate to move:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(master, text="Enter Y coordinate to move:").grid(row=1, column=0, sticky=tk.W)

        self.x_move_entry = ttk.Entry(master)
        self.y_move_entry = ttk.Entry(master)

        self.x_move_entry.grid(row=0, column=1)
        self.y_move_entry.grid(row=1, column=1)

        return self.x_move_entry  # initial focus

    def apply(self):
        x_move = int(self.x_move_entry.get())
        y_move = int(self.y_move_entry.get())

        # Move the selected shape
        app.move_node_shape(x_move, y_move)


class DrawDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Enter the node name:").grid(row=3, column=0, sticky=tk.W)
        tk.Label(master, text="Enter X coordinate:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(master, text="Enter Y coordinate:").grid(row=1, column=0, sticky=tk.W)
        tk.Label(master, text="Select a shape:").grid(row=2, column=0, sticky=tk.W)

        self.x_entry = ttk.Entry(master)
        self.y_entry = ttk.Entry(master)
        self.shape_choice = ttk.Combobox(master, values=["circle", "line", "triangle", "quadrilateral", "pentagon", "rectangle", "square"])
        self.name_entry = ttk.Entry(master)

        self.x_entry.grid(row=0, column=1)
        self.y_entry.grid(row=1, column=1)
        self.shape_choice.grid(row=2, column=1)
        self.name_entry.grid(row=3, column=1)

        return self.x_entry  # initial focus

    def apply(self):
        x = int(self.x_entry.get())
        y = int(self.y_entry.get())
        shape_name = self.shape_choice.get()
        name = self.name_entry.get()  # User entry name
        color = random.choice(["red", "orange", "yellow", "green", "blue"])

        # Draw the shape on the canvas
        shape = app.draw_node_shape_on_canvas(shape_name, x, y, color, name)
        app.node_shapes.append(shape)

        # Update the listbox with shape names
        app.update_node_shapes_listbox()

        # Show notification
        messagebox.showinfo("Notification", f"Shape {shape_name} with name '{name}' drawn at coordinates ({x}, {y}).")

        # Save the nodes to JSON after drawing a shape
        app.save_nodes_to_json()

class Graphify:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphify")

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame for the right-side widgets
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Buttons
        self.move_button = ttk.Button(self.right_frame, text="Move", command=self.open_move_dialog)
        self.find_closest_button = ttk.Button(self.right_frame, text="Find Closest", command=self.find_closest_node)
        self.draw_button = ttk.Button(self.right_frame, text="Add Node", command=self.open_draw_dialog)
        self.quit_button = ttk.Button(self.right_frame, text="Quit", command=root.destroy)  # quit button
        self.load_shapes_button = ttk.Button(self.right_frame, text="Load Nodes", command=self.load_shapes_with_interval)


        # Label for the listbox
        self.label_listbox = tk.Label(self.right_frame, text="Node Shapes:")
        self.label_listbox.pack(side=tk.TOP, pady=5)

        # Listbox for selecting nodes_shapes
        self.node_shapes_listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE)
        self.node_shapes_listbox.pack(side=tk.TOP, padx=5, pady=5)

        # Pack the widgets on the right side with vertical arrangement
        self.label_listbox.pack(side=tk.TOP, pady=5)
        self.node_shapes_listbox.pack(side=tk.TOP, pady=5)
        self.draw_button.pack(side=tk.TOP, pady=5)
        self.move_button.pack(side=tk.TOP, pady=5)
        self.find_closest_button.pack(side=tk.TOP, pady=5)
        self.load_shapes_button.pack(side=tk.TOP, pady=5)
        self.quit_button.pack(side=tk.TOP, padx=5, pady=5)

        self.node_shapes = []

    def set_placeholder_text(self, entry, text):
        entry.insert(0, text)
        entry.config(foreground="grey")

        def clear_placeholder(event):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(foreground="black")

        def restore_placeholder(event):
            if not entry.get():
                entry.insert(0, text)
                entry.config(foreground="grey")

        entry.bind("<FocusIn>", clear_placeholder)
        entry.bind("<FocusOut>", restore_placeholder)

    def open_draw_dialog(self):
        DrawDialog(self.root)

    def open_move_dialog(self):
        MoveDialog(self.root)

    def draw_node_shape_on_canvas(self, shape_name, x, y, color, name):
        # Adjust drawing coordinates
        x += self.canvas.winfo_reqwidth() / 2
        y += self.canvas.winfo_reqheight() / 2

        if shape_name == "circle":
            draw = self.canvas.create_oval(x, y, x + 50, y + 50, outline=color, width=2)
        elif shape_name == "line":
            draw = self.canvas.create_line(x, y, x + 50, y + 50, fill=color, width=2)
        elif shape_name == "triangle":
            draw = self.canvas.create_polygon(x, y, x + 50, y + 50, x + 100, y, outline=color, width=2)
        elif shape_name == "quadrilateral":
            draw = self.canvas.create_polygon(x, y, x + 50, y + 50, x + 100, y + 50, x + 50, y, outline=color, width=2)
        elif shape_name == "pentagon":
            draw = self.canvas.create_polygon(x, y, x + 50, y, x + 75, y + 50, x + 25, y + 75, x - 25, y + 25,
                                              outline=color, width=2)
        elif shape_name == "rectangle":
            draw = self.canvas.create_rectangle(x, y, x + 50, y + 75, outline=color, width=2)
        elif shape_name == "square":
            draw = self.canvas.create_rectangle(x, y, x + 50, y + 50, outline=color, width=2)
        else:
            return None

        return {"id": draw, "node_name": name, "shape": shape_name,  "x": x, "y": y, "color": color}

    def draw_node_shape(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            shape_name = self.shape_choice.get()
            color = random.choice(["red", "orange", "yellow", "green", "blue"])

            # Draw the shape on the canvas
            shape = self.draw_node_shape_on_canvas(shape_name, x, y, color)
            self.node_shapes.append(shape)

            # Update the listbox with shape names
            self.update_node_shapes_listbox()

            # Show notification
            messagebox.showinfo("Notification", f"Shape {shape_name} drawn at coordinates ({x}, {y}).")

            # Save the nodes to JSON after drawing a shape
            self.save_nodes_to_json()

            # Clear the entry fields
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
            self.shape_choice.set("Select a shape")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid coordinates.")


    def move_node_shape(self, x_move, y_move):
        try:
            selected_index = self.node_shapes_listbox.curselection()
            if selected_index:
                selected_shape = self.node_shapes[selected_index[0]]

                # Adjust movement coordinates
                x_move += self.canvas.winfo_reqwidth() / 2
                y_move += self.canvas.winfo_reqheight() / 2

                # Move the selected shape
                self.canvas.move(selected_shape["id"], x_move - selected_shape["x"], y_move - selected_shape["y"])
                selected_shape["x"], selected_shape["y"] = x_move, y_move

                # Update the listbox with updated shape names
                self.update_node_shapes_listbox()

                # Update the JSON file after moving shapes
                self.save_nodes_to_json()

                # Show notification
                messagebox.showinfo("Notification", f"Shape {selected_shape['node_name']} moved to coordinates ({x_move}, {y_move}).")
            else:
                messagebox.showwarning("Warning", "Please select a shape from the list.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid coordinates.")


    def load_shapes_with_interval(self):
        try:
            # Check if the file exists before opening
            if os.path.exists("main_db.json"):
                with open("main_db.json", "r") as file:
                    shapes_data = json.load(file)

                for shape_data in shapes_data:
                    shape_name = shape_data["shape"]
                    x = shape_data["x"] - self.canvas.winfo_reqwidth() / 2
                    y = shape_data["y"] - self.canvas.winfo_reqheight() / 2
                    color = shape_data["color"]
                    user_entry_name = shape_data["node_name"]

                    # Draw the shape on the canvas
                    shape = self.draw_node_shape_on_canvas(shape_name, x, y, color, user_entry_name)
                    self.node_shapes.append(shape)
                    # self.node_shapes.append({"shape": shape, "user_entry_name": user_entry_name})

                    # Update the listbox with shape names
                    self.update_node_shapes_listbox()

                    # Pause for 1 second
                    time.sleep(1)

            else:
                messagebox.showinfo("Notification", "No existing main_db.json file.")

        except Exception as e:
            messagebox.showerror("Error", f"Error loading shapes: {e}")


    def find_closest_node(self):
        try:
            selected_index = self.node_shapes_listbox.curselection()
            if selected_index:
                selected_node_shape = self.node_shapes[selected_index[0]]
                x_search = selected_node_shape["x"]
                y_search = selected_node_shape["y"]

                # Exclude the selected shape from the search
                other_node_shapes = [node_shape for node_shape in self.node_shapes if node_shape != selected_node_shape]

                if other_node_shapes:
                    # Find the closest shape to the selected shape
                    closest_node = min(other_node_shapes,
                                       key=lambda s: math.sqrt((s["x"] - x_search) ** 2 + (s["y"] - y_search) ** 2))
                    messagebox.showinfo("Notification",
                                        f"The closest node to {selected_node_shape['node_name']} is {closest_node['node_name']} at coordinates ({closest_node['x']}, {closest_node['y']}).")
                else:
                    messagebox.showwarning("Warning", "There are no other shapes to compare.")
            else:
                messagebox.showwarning("Warning", "Please select a shape from the list.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid coordinates.")

    def save_nodes_to_json(self):
        try:
            file_path = "main_db.json"
            if not os.path.isfile(file_path):
                with open(file_path, "w") as file:
                    file.write("[]\n")  # Write an empty list to start the JSON file
            
            # Write the updated data back to the file
            with open(file_path, "w") as file:
                json.dump(self.node_shapes, file, indent=2)

            messagebox.showinfo("Notification", "Nodes saved to main_db.json")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving nodes: {e}")


    def update_node_shapes_listbox(self):
        # Clear the listbox and add updated shape names
        self.node_shapes_listbox.delete(0, tk.END)
        for node_shape in self.node_shapes:
            self.node_shapes_listbox.insert(tk.END, node_shape["node_name"])


if __name__ == "__main__":
    root = tk.Tk()
    app = Graphify(root)
    root.mainloop()
