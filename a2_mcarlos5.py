#!/usr/bin/env python3
# Student ID: Michael Carlos

import subprocess
import os
import argparse

'''
OPS445 Assignment 2 - Winter 2025
Program: duim.py 
Author: Michael Carlos
The python code in this file (duim.py) is original work written by
Michael Carlos. No code in this file is copied from any other source 
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
import os
import argparse

def parse_command_args():
    """
    Parse the command-line arguments.
    """
    parser = argparse.ArgumentParser(description='DU Improved - Show Disk Usage with Graphs')
    parser.add_argument('target', nargs='?', default=os.getcwd(), help='The target directory to scan')
    parser.add_argument('-H', '--human-readable', action='store_true', help='Display sizes in human-readable format')
    parser.add_argument('-l', '--length', type=int, default=20, help='Length of the bar graph')
    args = parser.parse_args()
    
    # Check if the directory exists
    if not os.path.isdir(args.target):
        print(f"Error: The directory {args.target} is not valid.")
        exit(1)
    
    return args

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

def display_results(target_dir, dir_dict, graph_length):
    """
    Displays the results in a human-readable format, with a bar graph for each subdirectory.
    
    :param target_dir: Target directory path
    :param dir_dict: Dictionary of directories and their sizes
    :param graph_length: Length of the bar graph
    """
    total_size = sum(dir_dict.values())
    
    # Print the target directory size (without bar graph)
    print(f"{dir_dict[target_dir]}    {target_dir}")
    
    for sub_dir, size in dir_dict.items():
        if sub_dir == target_dir:
            continue
        
        # Calculate percentage for subdirectory
        percent = (size / total_size) * 100
        graph = percent_to_graph(percent, graph_length)
        
        # Print the results for subdirectory
        print(f"{size:<8} {sub_dir}  {graph}")

if __name__ == '__main__':
    # Step 1: Parse command-line arguments
    args = parse_command_args()
    
    # Step 2: Call `du` and get the output
    du_output_list = call_du_sub(args.target)
    
    # Step 3: Create the directory dictionary
    dir_dict = create_dir_dict(du_output_list)
    
    # Step 4: Display the results
    display_results(args.target, dir_dict, args.length)
