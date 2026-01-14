import turtle

def koch_inward(length: float, depth: int) -> None:
    """
    Deraw one "inward Koch" edge.

    Depth 0: draw a straight line of the given length.
    Depth > 0:
    1) split the edge into thirds
    2) replace the middle third with two side of an equilateral triangle 
    3) recurse on each of the 4 new segments
    """
# uses turtle graphics to draw a recursive Koch style pattern
"""
Purpose:
- Draw a polygon where each side is a Koch-style curve with an inward indentation.

Input:
- sides (int): number of polygon sides (>= 3)
- length (float): length of each polygon side (> 0)
- depth (int): recursion depth (>= 0)

How it works:
- Base case (depth == 0): draw a straight line.
- Each recursive level replaces 1 segment with 4 segments.
  Segments per side = 4**depth
  Total segments = sides * (4**depth)
"""

MAX_DEPTH = 7  # This prevents very slow drawings/freezing at high depth
# recursively draws a Koch style curve with an inward indentation
def koch_inward(length, depth):
    """Draw a Koch-style curve segment with an inward equilateral indentation."""
    if depth == 0:
        turtle.forward(length)
        return

    third = length / 3.0

    koch_inward(third, depth - 1)
    turtle.right(60)                 # turn inward

    # The angles (R60, L120, R60) form an equilateral "dent" pointing inward.
    turtle.right(60)
    koch_inward(third, depth - 1)
    turtle.left(120)                 # peak of the indentation
    koch_inward(third, depth - 1)
    turtle.right(60)                 # retuurn to original heading
    koch_inward(third, depth - 1)

def draw_polygon(sides: int, length: float, depth: int) -> None:
  exterior_angle = 360.0 / sides
  for _ in range(sides):
def draw_polygon(sides, length, depth):
    # Draw a polygon with `sides`, each side drawn using koch_inward.
    exterior_angle = 360.0 / sides
    for _ in range(sides):
        koch_inward(length, depth)
        turtle.right(exterior_angle)
# get and validate user input
def get_inputs():
    # Read and validate user input.
    sides = int(input("Enter the number of sides (>= 3): "))
    length = float(input("Enter the side length (> 0): "))
    depth = int(input("Enter the recursion depth (>= 0): "))

    if sides < 3:
        raise ValueError("Number of sides must be at least 3.")
    if length <= 0:
        raise ValueError("Side length must be greater than 0.")
    if depth < 0:
        raise ValueError("Recursion depth must be 0 or greater.")
    if depth > MAX_DEPTH:
        raise ValueError(f"Depth too large. Please use depth <= {MAX_DEPTH}.")

    return sides, length, depth

def main() -> None:
    # user input
    try:
        sides = int(input("Enter the number of sides (>=3): "))
        length = float(input("Enter the side length (>0): "))
        depth = int(input("Enter the recursion depth (>=0): "))
    except ValueError:
        print("Invalid input. Please enter whole numbers for sides/depth and a number for length")
        return

    # Basic Validation
    if sides < 3:
        print("Number of sides must be at least 3.")
        return
    if length <= 0:
        print("Side length must be greater than 0.")
        return
    if depth < 0:
        print("Recursive depth must be 0 or greater.")
        return

    # Turtle Setup
# main program entry point
def main():
    try:
        sides, length, depth = get_inputs()
    except ValueError as e:
        print(f"Input error: {e}")
        return

    screen = turtle.Screen()
    turtle.title("HIT137 - Question 3 Pattern")

    turtle.speed(0)
    turtle.hideturtle()

    # For testing - show animation
    screen.tracer(1)

    # Optional: centre the drawing a bit (approximate)
    turtle.penup()
    turtle.goto(-length / 2.0, length / 3.0)
    turtle.setheading(0)
    turtle.pendown()

    # Draw
    draw_polygon(sides, length, depth)

    turtle.update()
    # Optional: show complexity estimate
    segments_per_side = 4 ** depth
    total_segments = sides * segments_per_side
    print(f"Segments per side: {segments_per_side}, Total segments: {total_segments}")

    draw_polygon(sides, length, depth)

    screen.update()
    turtle.done()


if __name__ == "__main__":
    main()
