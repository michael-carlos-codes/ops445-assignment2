#!/usr/bin/env python3
# Student ID: Michael Carlos

import subprocess
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

def human_readable_size(size_in_bytes):
    """
    Converts bytes into human-readable format.
    
    :param size_in_bytes: Size in bytes
    :return: A string with size in human-readable format (e.g., '1K', '1M')
    """
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f}{unit}"
        size_in_bytes /= 1024

    return f"{size_in_bytes:.1f}T"

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

def display_results(directory_dict, human_readable, bar_length):
    """
    Displays the directory sizes with optional human-readable format and bar chart.
    
    :param directory_dict: A dictionary with directory paths as keys and sizes as values
    :param human_readable: Boolean flag to indicate whether to print human-readable sizes
    :param bar_length: The maximum length of the bar graph
    """
    max_size = max(directory_dict.values())
    for path, size in directory_dict.items():
        if human_readable:
            size_str = human_readable_size(size)
        else:
            size_str = str(size)
        
        percent = (size / max_size) * 100
        graph = percent_to_graph(percent, bar_length)
        
        print(f"{size_str}\t{path}\t{graph}")

def parse_command_args():
    """
    Parses command line arguments.
    
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts")
    
    parser.add_argument('target', nargs='?', default='.', help="The directory to scan (default is current directory)")
    parser.add_argument('-H', '--human-readable', action='store_true', help="Print sizes in human-readable format")
    parser.add_argument('-l', '--length', type=int, default=20, help="Specify the length of the graph (default is 20)")
    
    return parser.parse_args()

def main():
    args = parse_command_args()
    
    # Call the `du` command
    du_output_list = call_du_sub(args.target)
    
    # Create the directory dictionary from the output
    dir_dict = create_dir_dict(du_output_list)
    
    # Display results
    display_results(dir_dict, args.human_readable, args.length)

if __name__ == "__main__":
    main()

