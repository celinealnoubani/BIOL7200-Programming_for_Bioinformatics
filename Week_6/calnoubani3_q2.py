#!/usr/bin/env python
import sys

def check_parenthesis(case: str) -> None:
    count = 0
    for char in case:
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
            if count < 0:
                print("NOT PAIRED")
                return
    if count == 0:
        print("PAIRED")
    else:
        print("NOT PAIRED")
check_parenthesis(sys.argv[1])