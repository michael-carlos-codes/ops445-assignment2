#!/usr/bin/env python3
# Student ID: Michael Carlos

import subprocess
import argparse


'''
OPS445 Assignment 2 - Winter 2025
Program: duim.py 
Author: Michael Carlos
The python code in this file (duim.py) is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or online resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script mimics the behavior of the `du` command but 
             includes additional functionality such as graphical representation.

Date: 03/13/2025
'''

import subprocess

def call_du_sub(directory):
    """
    Runs the `du -d 1` command on the given directory.
    Returns a list of strings, each containing size and directory path.
    """
    process = subprocess.Popen(["du", "-d", "1", directory], stdout=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    
    # Split lines and remove newline characters
    return output.strip().split("\n")

def percent_to_graph(percent, total_chars):
    """
    Converts a percentage into a visual bar graph.
    Example: percent_to_graph(50, 10) → '=====     '
    
    :param percent: Percentage value (0 to 100)
    :param total_chars: Total length of the graph (e.g., 10 characters)
    :return: A string representing the percentage as a graph
    """
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100")

    filled_chars = round((percent / 100) * total_chars)
    return "=" * filled_chars + " " * (total_chars - filled_chars)

def create_dir_dict(du_output_list):
    """
    Converts the `du` output list into a dictionary with directory paths as keys
    and their sizes (in bytes) as integer values.
    
    :param du_output_list: List of strings from `call_du_sub()` output
    :return: Dictionary {directory_path: size_in_bytes}
    """
    dir_dict = {}
    
    for entry in du_output_list:
        size, path = entry.split("\t")  # 'du' output format: "size<TAB>path"
        dir_dict[path] = int(size)
    
    return dir_dict

