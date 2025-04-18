import turtle
import re
import tkinter as tk
from systems import get_systems


class LSystem:
    def __init__(self, axiom: str = "F", angle: int = 60, distance: float = 5, 
                 headingAngle:int = 0, rule1: str = "F-F++F-F", rule2: str = "F", 
                 custom_system: dict = None):

        self.lSystem = {
            "axiom": axiom,
            "variables": {"var1": "F", "var2": "f"},
            "rules": {"r1": rule1, "r2": rule2},
            "settings": {
                "angle": angle,
                "distance": distance,
                "headingAngle": headingAngle,
                "turnLeftStack": 0,
                "turnRightStack": 0,
            },
            "goto" : {"x": 0, "y": 0}
        }
        
        if custom_system:
            self.lSystem.update(custom_system)

        # Regex patterns for character transformation
        self.re_1 = re.compile(r'[A-U]|[1-9]')  # draw forward              
        self.re_2 = re.compile(r'[a-u]')  # Move forward without drawing    
        self.re_3 = re.compile(r'[V-Z]|[v-z]')  # Don't do anything         
        self.re_4 = re.compile(r'[+-\|\[\]]')  # Turn left, turn right, save state, restore state              

    def apply_rules(self, char: str) -> str:
        """Apply transformation rules to a single character"""
        # If the character equals var2 (for our tree "0"), then return rule2.
        if char == self.lSystem["variables"]["var2"]:
            return self.lSystem["rules"]["r2"]
        if bool(self.re_1.search(char)):
            return self.lSystem["rules"]["r1"]
        elif bool(self.re_2.search(char)):
            return self.lSystem["rules"]["r2"]
        elif bool(self.re_3.search(char)):
            return ""
        elif bool(self.re_4.search(char)):
            return char
        else:
            return char
        

    def __process_string(self, string: str) -> str:
        """Process a string by applying rules to each character"""
        return "".join(self.apply_rules(char) for char in string)

    def generate(self, iterations: int) -> str:
        """Generate the L-system string after the specified number of iterations"""
        current_string = self.lSystem["axiom"]
        for _ in range(iterations):
            current_string = self.__process_string(current_string)
        return current_string

    def draw(self, instructions: str):
        """Draw the L-system using turtle graphics"""
        stack = []
        t = turtle.Turtle()
        t.setheading(self.lSystem["settings"]["headingAngle"])
        t.speed(0)
        t.penup()
        t.goto(self.lSystem["goto"]["x"], self.lSystem["goto"]["y"])
        t.pendown()

        for char in instructions:
            if char == self.lSystem["variables"]["var1"]:  # Move forward and draw
                t.forward(self.lSystem["settings"]["distance"])
            elif char == self.lSystem["variables"]["var2"]:  # Move forward without drawing
                #t.penup()
                t.forward(self.lSystem["settings"]["distance"])
                #t.pendown()
            elif char == '+':  # Turn right
                t.right(self.lSystem["settings"]["angle"])
            elif char == '-':  # Turn left
                t.left(self.lSystem["settings"]["angle"])
            elif char == '|':  # Turn 180 degrees
                t.right(180)
            elif char == '[':  # Save current state
                stack.append((t.position(), t.heading()))
                t.left(self.lSystem["settings"]["turnLeftStack"])
            elif char == ']':  # Restore last saved state
                if stack:
                    pos, head = stack.pop()
                    t.penup()
                    t.goto(pos)
                    t.setheading(head)
                    t.right(self.lSystem["settings"]["turnRightStack"])
                    t.pendown()
        return t


def draw_system(selected_var, input_entry: int):
    systems = get_systems()
    selection = selected_var.get()
    lsys = LSystem(custom_system=systems[selection])
    instructions = lsys.generate(input_entry)
    lsys.draw(instructions)
    

class LSystemControlPanel:
    def __init__(self, root):
        """Initialize the control panel with all UI elements and handlers"""
        self.root = root
        self.new_win = tk.Toplevel(root)
        self.new_win.title("Control Panel")
        self.systems = get_systems()
        
        # Create a control variable initialized with a default key
        self.selected_var = tk.StringVar(self.new_win)
        self.selected_var.set(list(self.systems.keys())[0])
        
        # Set up UI components and entry fields
        self.setup_ui()
    
    def update_text(self, text_input, parameter1, parameter2=None, *args):
        """Update the text in an input field based on the selected L-system"""
        text_input.delete("1.0", tk.END)
        if parameter2:
            text_input.insert(tk.END, self.systems[self.selected_var.get()][parameter1][parameter2])
        else:
            text_input.insert(tk.END, self.systems[self.selected_var.get()][parameter1])
            
    def create_input(self, window, label_text, parameter, parameter2=None, column=0, row=7, *args):
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
    
    def create_system_from_input(self):
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
        instructions = LSystem(custom_system=self.systems[self.selected_var.get()]).generate(iterations)
        self.instructions_.insert(tk.END, instructions)
        self.instructions_.config(state=tk.DISABLED)
    
    def draw_lsystem(self):
        """Update system from inputs, generate instructions, and draw the L-system"""
        self.create_system_from_input()
        self.update_instructions()
        turtle.clearscreen()
        
        selection = self.selected_var.get()
        iterations = int(self.input_entry_iterations.get())
        lsys = LSystem(custom_system=self.systems[selection])
        instructions = lsys.generate(iterations)
        lsys.draw(instructions)
        
    def setup_ui(self):
        """Create all UI controls, fields, and bind event handlers"""
        # OptionMenu for selecting the L-system
        opt = tk.OptionMenu(self.new_win, self.selected_var, *self.systems.keys())
        opt.config(width=20, font=("Arial", 12))
        opt.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E, columnspan=4)
        
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
        self.input_text_axiom = self.create_input(self.new_win, "Axiom:", "axiom", column=0, row=2)
        self.input_text_var1 = self.create_input(self.new_win, "Variable 1:", "variables", "var1", column=0, row=3)
        self.input_text_var2 = self.create_input(self.new_win, "Variable 2:", "variables", "var2", column=0, row=4)
        
        # Rules
        self.input_text_rule1 = self.create_input(self.new_win, "Rule 1:", "rules", "r1", column=0, row=5)
        self.input_text_rule2 = self.create_input(self.new_win, "Rule 2:", "rules", "r2", column=0, row=6)
        
        # Settings
        self.input_text_angle = self.create_input(self.new_win, "Angle:", "settings", "angle", column=2, row=1)
        self.input_text_distance = self.create_input(self.new_win, "Distance:", "settings", "distance", column=2, row=2)
        self.input_text_headingAngle = self.create_input(self.new_win, "Heading Angle:", "settings", "headingAngle", column=2, row=3)
        self.input_text_turnLeftStack = self.create_input(self.new_win, "Turn Left Stack:", "settings", "turnLeftStack", column=2, row=4)
        self.input_text_turnRightStack = self.create_input(self.new_win, "Turn Right Stack:", "settings", "turnRightStack", column=2, row=5)
        self.input_text_goto_x = self.create_input(self.new_win, "Goto X:", "goto", "x", column=2, row=6)
        self.input_text_goto_y = self.create_input(self.new_win, "Goto Y:", "goto", "y", column=2, row=7)
        
        # Bind the update function to selection changes
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_axiom, parameter1="axiom"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_var1, parameter1="variables", parameter2="var1"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_var2, parameter1="variables", parameter2="var2"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_rule1, parameter1="rules", parameter2="r1"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_rule2, parameter1="rules", parameter2="r2"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_angle, parameter1="settings", parameter2="angle"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_distance, parameter1="settings", parameter2="distance"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_headingAngle, parameter1="settings", parameter2="headingAngle"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_turnLeftStack, parameter1="settings", parameter2="turnLeftStack"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_turnRightStack, parameter1="settings", parameter2="turnRightStack"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_goto_x, parameter1="goto", parameter2="x"))
        self.selected_var.trace_add("write", lambda *args: self.update_text(text_input=self.input_text_goto_y, parameter1="goto", parameter2="y"))
        
        # Generate instructions area
        instructions_label = tk.Label(self.new_win, text="Instructions:")
        instructions_label.grid(row=9, column=0, padx=5, pady=5)
        
        self.instructions_ = tk.Text(self.new_win, height=10, width=50)
        self.instructions_.grid(row=10, column=0, columnspan=4, padx=5, pady=5, sticky=tk.W+tk.E)
        self.instructions_.insert(tk.END, "Instructions will be generated here.")
        self.instructions_.config(state=tk.DISABLED)
        
        # Button to update the system and then draw the selected L-system 
        btn = tk.Button(self.new_win, text="Draw L-System", command=self.draw_lsystem)
        btn.config(width=20, font=("Arial", 12))
        btn.grid(row=8, column=0, padx=5, pady=5, columnspan=4, sticky=tk.W+tk.E)

def setup_turtle_screen():
    """
    Set up the turtle screen.
    """
    win = turtle.Screen()
    win.setup(width=800, height=600)
    win.title("L-System")
    win.bgcolor("white")
    win.tracer(0)
    return win

def main():
    # Set up the turtle screen
    win = setup_turtle_screen()
    
    # Get the toplevel widget for the Toplevel parent
    root = win.getcanvas().winfo_toplevel()
    
    # Create the control panel as a class instance
    control_panel = LSystemControlPanel(root)
    
    win.update()
    win.exitonclick()

if __name__ == "__main__":
    main()