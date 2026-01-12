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
    if depth == 0:
        turtle.forward(length)
        return

    third = length / 3.0

    koch_inward(third, depth - 1)
    turtle.right(60)                 # turn inward
    koch_inward(third, depth - 1)
    turtle.left(120)                 # peak of the indentation
    koch_inward(third, depth - 1)
    turtle.right(60)                 # retuurn to original heading
    koch_inward(third, depth - 1)

def draw_polygon(sides: int, length: float, depth: int) -> None:
  exterior_angle = 360.0 / sides
  for _ in range(sides):
        koch_inward(length, depth)
        turtle.right(exterior_angle)

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
    turtle.title("HIT137 - Question 3 Pattern")
    turtle.speed(0)
    turtle.hideturtle()

    # Optional: centre the drawing a bit (not perfect but helps)
    turtle.penup()
    turtle.goto(-length / 2.0, length / 3.0)
    turtle.pendown()

    # Draw
    draw_polygon(sides, length, depth)

    turtle.update()
    turtle.done()

if __name__ == "__main__":
    main()
