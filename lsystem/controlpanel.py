import turtle
import tkinter as tk
import os
from PIL import Image
from datetime import datetime
from . import gif
from . import systems
from . import lsystem
from . import utils


class LSystemControlPanel:
    def __init__(self, root):
        """Initialize the control panel with all UI elements and handlers"""
        self.root = root
        self.new_win = tk.Toplevel(root)
        self.new_win.title("Control Panel")
        
        # Use utility functions for consistent path handling
        example_systems = systems.load_systems_from_folder(utils.get_examples_dir()) 
        custom_systems = systems.load_systems_from_folder(utils.get_custom_dir())
        
        self.systems = example_systems if example_systems else {}
        if custom_systems:
            self.systems.update(custom_systems)
        if not self.systems:
            self.systems = {"Custom": {
                "axiom": "F",
                "variables": {"var1": "F", "var2": "F"},
                "rules": {"r1": "F+F-F-F+F", "r2": "f"},
                "settings": {"angle": 90, "distance": 5, "headingAngle": 0, "turnLeftStack": 0, "turnRightStack": 0},
                "goto": {"x": 0, "y": 0}
            }}
        
        # Create a control variable initialized with a default key
        self.selected_var = tk.StringVar(self.new_win)
        self.selected_var.set(list(self.systems.keys())[0])
        
        # Set up UI components and entry fields
        self.setup_ui()
    
    def __update_text(self, text_input, parameter1, parameter2=None, *args):
        """Update the text in an input field based on the selected L-system"""
        text_input.delete("1.0", tk.END)
        if parameter2:
            text_input.insert(tk.END, self.systems[self.selected_var.get()][parameter1][parameter2])
        else:
            text_input.insert(tk.END, self.systems[self.selected_var.get()][parameter1])
            
    def __create_input(self, window, label_text, parameter, parameter2=None, column=0, row=7, *args):
        """Create a labeled text input field and initialize it with the current system's value"""
        label = tk.Label(window, text=label_text)
        label.grid(row=row, column=column, padx=5, pady=5)
        
        text_input = tk.Text(window, height=1, width=20)
        text_input.grid(row=row, column=column+1, padx=5, pady=5)
        
        if parameter2:
            text_input.insert(tk.END, self.systems[self.selected_var.get()][parameter][parameter2])
        else:
            text_input.insert(tk.END, self.systems[self.selected_var.get()][parameter])
        
        return text_input
    
    def __create_system_from_input(self):
        """Read all input fields and update the current L-system configuration"""
        self.systems[self.selected_var.get()]["axiom"] = self.input_text_axiom.get("1.0", tk.END).strip()
        self.systems[self.selected_var.get()]["variables"]["var1"] = self.input_text_var1.get("1.0", tk.END).strip()
        self.systems[self.selected_var.get()]["variables"]["var2"] = self.input_text_var2.get("1.0", tk.END).strip()
        self.systems[self.selected_var.get()]["rules"]["r1"] = self.input_text_rule1.get("1.0", tk.END).strip()
        self.systems[self.selected_var.get()]["rules"]["r2"] = self.input_text_rule2.get("1.0", tk.END).strip()
        self.systems[self.selected_var.get()]["settings"]["angle"] = int(self.input_text_angle.get("1.0", tk.END).strip())
        self.systems[self.selected_var.get()]["settings"]["distance"] = float(self.input_text_distance.get("1.0", tk.END).strip())
        self.systems[self.selected_var.get()]["settings"]["headingAngle"] = int(self.input_text_headingAngle.get("1.0", tk.END).strip())
        self.systems[self.selected_var.get()]["settings"]["turnLeftStack"] = int(self.input_text_turnLeftStack.get("1.0", tk.END).strip())
        self.systems[self.selected_var.get()]["settings"]["turnRightStack"] = int(self.input_text_turnRightStack.get("1.0", tk.END).strip())
        self.systems[self.selected_var.get()]["goto"]["x"] = float(self.input_text_goto_x.get("1.0", tk.END).strip())
        self.systems[self.selected_var.get()]["goto"]["y"] = float(self.input_text_goto_y.get("1.0", tk.END).strip())

        return self.systems[self.selected_var.get()]
    
    def update_instructions(self):
        """Generate and display the instruction string in the preview area"""
        self.instructions_.config(state=tk.NORMAL)
        self.instructions_.delete("1.0", tk.END)
        iterations = int(self.input_entry_iterations.get())
        instructions = lsystem.LSystem(custom_system=self.systems[self.selected_var.get()]).generate(iterations)
        self.instructions_.insert(tk.END, instructions)
        self.instructions_.config(state=tk.DISABLED)
    
    
    def __export_custom_system(self):
        """Export the current custom system to a JSON file"""
        custom_system = self.__create_system_from_input()
        filename = systems.export_systems_to_json(custom_system)
        self.instructions_.config(state=tk.NORMAL)
        self.instructions_.delete("1.0", tk.END)
        self.instructions_.insert(tk.END, f"Custom system exported to {filename}.")
        self.instructions_.config(state=tk.DISABLED)
    
    def __update_systems(self):
            """Update the list of available L-systems"""
            # Use utility functions for path handling
            example_systems = systems.load_systems_from_folder(utils.get_examples_dir()) 
            custom_systems = systems.load_systems_from_folder(utils.get_custom_dir())
            
            if example_systems:
                self.systems = example_systems
            else:
                self.systems = {}
                
            if custom_systems:
                self.systems.update(custom_systems)
                
            if not self.systems:
                self.systems = {"Custom": {
                    "axiom": "F",
                    "variables": {"var1": "F", "var2": "F"},
                    "rules": {"r1": "F+F-F-F+F", "r2": ""},
                    "settings": {"angle": 90, "distance": 5, "headingAngle": 0, "turnLeftStack": 0, "turnRightStack": 0},
                    "goto": {"x": 0, "y": 0}
                }}
            
            # Update the OptionMenu with the new systems
            menu = self.opt["menu"]
            menu.delete(0, "end")
            for system_name in self.systems.keys():
                menu.add_command(label=system_name, command=lambda value=system_name: self.selected_var.set(value))
            self.selected_var.set(list(self.systems.keys())[0])
            
        
    
    def draw_lsystem(self, tracer=False):
        """Update system from inputs, generate instructions, and draw the L-system"""
        try:
            self.__create_system_from_input()
            self.update_instructions()
            # Clear the drawing and completely reset the turtle state
            turtle.clearscreen()
            turtle.resetscreen()  # This resets everything to default
            
            # Re-establish screen properties
            screen = turtle.Screen()
            screen.setup(width=800, height=600)
            screen.title("L-System")
            screen.bgcolor("white")
            if tracer:
                screen.tracer(0)
            
            selection = self.selected_var.get()
            iterations = int(self.input_entry_iterations.get())
            lsys = lsystem.LSystem(custom_system=self.systems[selection])
            instructions = lsys.generate(iterations)
            lsys.draw(instructions)
            turtle.update()  # Update the screen to show the complete drawing

        except ValueError:
            self.instructions_.config(state=tk.NORMAL)
            self.instructions_.delete("1.0", tk.END)
            self.instructions_.insert(tk.END, "Invalid input! Please check your entries.")
            self.instructions_.config(state=tk.DISABLED)
            
            
    def __animate_lsystem(self):
        """Generate an animated GIF showing the evolution of the L-system"""
        try:
            # Get proper path to the root animations folder using utils
            animations_dir = utils.get_animations_dir()
            
            # Create a temporary directory for frames
            temp_dir = os.path.join(animations_dir, "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Get system configuration from input fields
            custom_system = self.__create_system_from_input()
            max_iterations = int(self.input_entry_iterations.get())
            
            # Generate timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            system_name = self.selected_var.get()
            
            # Prepare for animation capture
            frame_files = []
            
            # Update UI to show progress
            self.instructions_.config(state=tk.NORMAL)
            self.instructions_.delete("1.0", tk.END)
            self.instructions_.insert(tk.END, "Creating animation frames...\n")
            self.instructions_.config(state=tk.DISABLED)
            self.root.update()
            
            # For each iteration level, generate a frame
            for i in range(1, max_iterations + 1):
                # Clear the turtle screen
                turtle.clearscreen()
                turtle.resetscreen()
                
                # Configure the turtle screen
                screen = turtle.Screen()
                screen.setup(width=800, height=600)
                screen.title(f"L-System Animation (Iteration {i})")
                screen.bgcolor("white")
                screen.tracer(0)  # Turn off animation for faster drawing
                
                # Create and configure turtle
                t = turtle.Turtle()
                t.speed(0)
                t.hideturtle()
                
                # Generate L-system at current iteration level
                lsys = lsystem.LSystem(custom_system=custom_system)
                instructions = lsys.generate(i)
                
                # Draw the L-system
                lsys.draw(instructions)
                turtle.update()
                
                # Save the frame
                # First save as EPS since PostScript works better with turtle
                eps_path = os.path.join(animations_dir, "temp.eps")
                canvas = turtle.getcanvas()
                canvas.postscript(file=eps_path)
                
                # Convert EPS to PNG
                img = Image.open(eps_path)
                png_path = os.path.join(temp_dir, f"frame_{i:03d}.png")
                img.save(png_path)
                img.close()
                frame_files.append(png_path)
                
                # Update progress
                self.instructions_.config(state=tk.NORMAL)
                self.instructions_.delete("1.0", tk.END)
                self.instructions_.insert(tk.END, f"Creating animation... {i}/{max_iterations}\n")
                self.instructions_.config(state=tk.DISABLED)
                self.root.update()
            
            # Create the animated GIF
            if frame_files:
                output_gif = os.path.join(animations_dir, f"{system_name}_{timestamp}.gif")
                gif.create_animated_gif(frame_files, output_gif, duration=500)
                
                # Update UI with success message
                self.instructions_.config(state=tk.NORMAL)
                self.instructions_.delete("1.0", tk.END)
                self.instructions_.insert(tk.END, f"Animation saved as {output_gif}")
                self.instructions_.config(state=tk.DISABLED)
                
                # Clean up temporary EPS file
                try:
                    os.remove(eps_path)
                except:
                    pass
                    
                # Optionally remove the temp directory
                try:
                    os.rmdir(temp_dir)
                except:
                    pass
                    
                # Redraw the final result
                self.draw_lsystem(tracer=True)
                
        except Exception as e:
            self.instructions_.config(state=tk.NORMAL)
            self.instructions_.delete("1.0", tk.END)
            self.instructions_.insert(tk.END, f"Error creating animation: {str(e)}")
            self.instructions_.config(state=tk.DISABLED)    
            
    def __update_mode_display(self, *args):
        """Update the display label based on the slider value"""
        mode = int(self.mode_slider.get())
        if mode == 1:
            self.state_display.config(text="Normal Drawing", bg="white")
        elif mode == 2:
            self.state_display.config(text="Fast Drawing", bg="lightgreen")
        elif mode == 3:
            self.state_display.config(text="Animation (GIF)", bg="lightblue")

    def __process_based_on_mode(self):
        """Execute the appropriate function based on the slider value"""
        mode = int(self.mode_slider.get())
        if mode == 1:
            # Normal drawing
            self.draw_lsystem(tracer=False)
        elif mode == 2:
            # Fast drawing with tracer
            self.draw_lsystem(tracer=True)
        elif mode == 3:
            # Animation mode - create GIF
            self.__animate_lsystem()
        
    def setup_ui(self):
        """Create all UI controls, fields, and bind event handlers"""
        # OptionMenu for selecting the L-system
        self.opt = tk.OptionMenu(self.new_win, self.selected_var, *self.systems.keys())
        self.opt.config(width=20, font=("Arial", 12))
        self.opt.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E, columnspan=4)
        
        # Number of iterations
        input_label_iterations = tk.Label(self.new_win, text="Iterations:")
        input_label_iterations.grid(row=1, column=0, padx=5, pady=5)
        
        self.input_entry_iterations = tk.Entry(self.new_win, width=5)
        self.input_entry_iterations.grid(row=1, column=1, padx=5, pady=5)
        self.input_entry_iterations.insert(0, "6")
        
        if self.input_entry_iterations.get() == "" or not self.input_entry_iterations.get().isdigit():
            self.input_entry_iterations.delete(0, tk.END)
            self.input_entry_iterations.insert(0, "6")
        
        # Axiom and variables
        self.input_text_axiom = self.__create_input(self.new_win, "Axiom:", "axiom", column=0, row=2)
        self.input_text_var1 = self.__create_input(self.new_win, "Variable 1:", "variables", "var1", column=0, row=3)
        self.input_text_var2 = self.__create_input(self.new_win, "Variable 2:", "variables", "var2", column=0, row=4)
        
        # Rules
        self.input_text_rule1 = self.__create_input(self.new_win, "Rule 1:", "rules", "r1", column=0, row=5)
        self.input_text_rule2 = self.__create_input(self.new_win, "Rule 2:", "rules", "r2", column=0, row=6)

        
        # export custom system button
        export_button = tk.Button(self.new_win, text="Export Custom System", command=lambda: self.__export_custom_system())
        export_button.config(width=20, font=("Arial", 12))
        export_button.grid(row=9, column=0, padx=5, pady=5, sticky=tk.E+tk.W, columnspan=2)
        
        # refresh system menu button
        refresh_button = tk.Button(self.new_win, text="Refresh Systems", command=lambda: self.__update_systems())
        refresh_button.config(width=20, font=("Arial", 12))
        refresh_button.grid(row=9, column=2, padx=5, pady=5, sticky=tk.E+tk.W, columnspan=2)
        
        
        # Settings
        self.input_text_angle = self.__create_input(self.new_win, "Angle:", "settings", "angle", column=2, row=1)
        self.input_text_distance = self.__create_input(self.new_win, "Distance:", "settings", "distance", column=2, row=2)
        self.input_text_headingAngle = self.__create_input(self.new_win, "Heading Angle:", "settings", "headingAngle", column=2, row=3)
        self.input_text_turnLeftStack = self.__create_input(self.new_win, "Turn Left Stack:", "settings", "turnLeftStack", column=2, row=4)
        self.input_text_turnRightStack = self.__create_input(self.new_win, "Turn Right Stack:", "settings", "turnRightStack", column=2, row=5)
        self.input_text_goto_x = self.__create_input(self.new_win, "Goto X:", "goto", "x", column=2, row=6)
        self.input_text_goto_y = self.__create_input(self.new_win, "Goto Y:", "goto", "y", column=2, row=7)
        
        # Bind the update function to selection changes
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_axiom, parameter1="axiom"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_var1, parameter1="variables", parameter2="var1"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_var2, parameter1="variables", parameter2="var2"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_rule1, parameter1="rules", parameter2="r1"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_rule2, parameter1="rules", parameter2="r2"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_angle, parameter1="settings", parameter2="angle"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_distance, parameter1="settings", parameter2="distance"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_headingAngle, parameter1="settings", parameter2="headingAngle"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_turnLeftStack, parameter1="settings", parameter2="turnLeftStack"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_turnRightStack, parameter1="settings", parameter2="turnRightStack"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_goto_x, parameter1="goto", parameter2="x"))
        self.selected_var.trace_add("write", lambda *args: self.__update_text(text_input=self.input_text_goto_y, parameter1="goto", parameter2="y"))
        
        # Generate instructions area
        instructions_label = tk.Label(self.new_win, text="Instructions:")
        instructions_label.grid(row=10, column=0, padx=5, pady=5)
        
        self.instructions_ = tk.Text(self.new_win, height=10, width=50)
        self.instructions_.grid(row=11, column=0, columnspan=4, padx=5, pady=5, sticky=tk.W+tk.E)
        self.instructions_.insert(tk.END, "Instructions will be generated here.")
        self.instructions_.config(state=tk.DISABLED)
        
        # Create a frame for the slider and its label
        slider_frame = tk.Frame(self.new_win)
        slider_frame.grid(row=8, column=2, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # State display label
        self.state_display = tk.Label(slider_frame, text="Normal Drawing", width=15, 
                                    font=("Arial", 10), relief=tk.SUNKEN)
        self.state_display.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create the slider
        self.mode_slider = tk.Scale(slider_frame, from_=1, to=3, orient=tk.HORIZONTAL, showvalue=False,
                                    command=self.__update_mode_display)
        self.mode_slider.set(1)
        self.mode_slider.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Button to perform action based on slider value
        btn = tk.Button(self.new_win, text="Draw L-System", 
                        command=self.__process_based_on_mode)
        btn.config(width=20, font=("Arial", 12), bg="lightblue", activebackground="lightgreen")
        btn.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W+tk.E, columnspan=2)
