import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import re

def init_folder(verbose=False):
    current_dir = os.getcwd()
    datasets_path = os.path.join(os.path.dirname(current_dir), "Datasets")
    if verbose:
        print(f"Datasets folder path: {datasets_path}")
        print(f"5 text files:")
        for i in range(5):
            print(files[i])

    filenames = os.listdir(datasets_path) 
    txt_pattern = r".+\.txt$"  # Matches any string followed by ".txt" at the end

    # f[:-4] no incluye el ".txt", los ultimos 4 caracteres
    files = [f[:-4] for f in filenames if re.match(txt_pattern, f)]

    return datasets_path, files

def find_matching_file(datasets_path, files, pre_extension='x'):
    """
    Searches for a file in the specified directory that has the same name as a file in the
    provided list, but with an "x" appended before an unknown extension.
    Args:
        datasets_path: The absolute path to the directory containing the files.
        files: A list of filenames (without extensions) to search for.
    Returns:
        A list of matching filenames (including extensions) found in the directory,
        or an empty list if no matches are found.
    """

    matching_files = []

    if type(files) != list:
        files = [files] # little fix to get back list for 1-inputs too

    for filename in files:
        # Construct the matching pattern with a capture group for the extension
        pattern = (
            f"{filename}{pre_extension}\.([^\.]+)"  # Matches filename + 'x' + '.' + any characters
        )

        for entry in os.scandir(datasets_path):
            if entry.is_file() and re.match(pattern, entry.name):
                # Extract the extension from the matched filename
                extension = re.match(pattern, entry.name).group(1)
                matching_files.append(
                    f"{filename}{pre_extension}.{extension}"
                )  # Reconstruct full name with extension
                break  # Stop searching once a match is found for the current filename
    if matching_files:
        return matching_files
    else:
        print("No matching files found.")
        return null



def count_text_stats(txt_path):
    """
    Computes the number of lines, words, and characters in a given text file.
    
    Args:
        txt_path: The path to the text file to be analyzed.
    
    Returns:
        A tuple containing:
            - num_lines: The total number of lines in the file.
            - num_words: The total number of words in the file.
            - num_chars: The total number of characters in the file.
    """
    num_lines = 0
    num_words = 0
    num_chars = 0

    try:
        # Open the text file in read mode with UTF-8 encoding
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Count lines
                num_lines += 1

                # Count words
                words = line.split()
                num_words += len(words)

                # Count characters
                num_chars += len(line)
    except Exception as e:
        print(f"Error processing file {txt_path}: {e}")

    return num_lines, num_words, num_chars

# def convert_to_path(datasets_path, files_label_path):
#     list(map)
#     return label_path = os.path.join(datasets_path, label_path)

# if main
#matching_files = find_matching_file(datasets_path, files)