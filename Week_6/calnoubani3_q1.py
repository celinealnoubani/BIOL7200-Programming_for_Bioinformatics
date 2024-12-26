#!/usr/bin/env python3

import sys

def draw_triangle(char: str, size: int) -> None:
    """
    Draws a triangle of a given size using a specified character

    Arguments:
        char: character to build the triangle 
        size: height of the triangle

    Returns:
        None (prints the triangle directly to the console)
    """
    rows = []
    
    # Builds the upper part of the triangle
    for i in range(1, size//2 + 1):
        rows.append(char)
        print(char * i)
    
    # Adds a middle row if the size is odd
    if size % 2 != 0:
        print(char * (size//2 + 1))
    
    # Builds the lower part of the triangle
    for i in range(size//2, 0, -1):
        print(char * i)

# Main function call with command-line arguments
draw_triangle(sys.argv[1], int(sys.argv[2]))
