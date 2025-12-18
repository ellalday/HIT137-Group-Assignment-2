import turtle
import math

def koch_inward(length, depth):
    """
    Depth 0: draw a straight line.
    Depth > 0: split into thirds and replace the middle third with two
    sides of an equilateral triangle pointing inward.
    """
    if depth == 0:
        turtle.forward(length)
        return

    third = length / 3.0

    koch_inward(third, depth - 1)
    turtle.right(60)                 # inward indentation
    koch_inward(third, depth - 1)
    turtle.left(120)
    koch_inward(third, depth - 1)
    turtle.right(60)
    koch_inward(third, depth - 1)

def draw_polygon(sides, length, depth):
    exterior_angle = 360.0 / sides
    for _ in range(sides):
        koch_inward(length, depth)
        turtle.right(exterior_angle)

def main():
    sides = int(input("Enter the number of sides: "))
    length = float(input("Enter the side length: "))
    depth = int(input("Enter the recursion depth: "))

    turtle.title("HIT137 - Question 3 Pattern")
    turtle.speed(0)
    turtle.hideturtle()

    # Optional: centre the drawing a bit (not perfect but helps)
    turtle.penup()
    turtle.goto(-length / 2.0, length / 3.0)
    turtle.pendown()

    draw_polygon(sides, length, depth)

    turtle.done()

if __name__ == "__main__":
    main()
