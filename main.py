import turtle
import lsystem.lsystem as ls
import lsystem.controlpanel as cp
import lsystem.utils as utils

def draw_system(selected_var, input_entry: int):
    from lsystem import systems as sys_module  # Import systems module properly
    systems = sys_module.systems
    selection = selected_var.get()
    lsys = ls.LSystem(custom_system=systems[selection])
    instructions = lsys.generate(input_entry)
    lsys.draw(instructions)
    
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
    # Create necessary directories using utils
    utils.get_animations_dir()  # Ensures animations directory exists
    utils.get_examples_dir()    # Ensures examples directory exists
    utils.get_custom_dir()      # Ensures custom directory exists
    
    # Set up the turtle screen
    win = setup_turtle_screen()
    
    # Get the toplevel widget for the Toplevel parent
    root = win.getcanvas().winfo_toplevel()
    
    # Create the control panel as a class instance
    cp.LSystemControlPanel(root)
    
    win.update()
    win.exitonclick()

if __name__ == "__main__":
    main()