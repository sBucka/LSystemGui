import turtle
import re
import os
from . import gif 

class LSystem:
    def __init__(self, custom_system: dict):

        self.lSystem = {
                "axiom": "F",
                "variables": {"var1": "F", "var2": "F"},
                "rules": {"r1": "F+F-F-F+F", "r2": ""},
                "settings": {"angle": 90, "distance": 5, "headingAngle": 0, "turnLeftStack": 0, "turnRightStack": 0},
                "goto": {"x": 0, "y": 0}
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

    def draw(self, instructions: str, generate_gif: bool = False) -> turtle.Turtle:
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


