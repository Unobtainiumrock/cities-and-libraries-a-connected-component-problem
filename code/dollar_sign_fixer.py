# Copyright 2024 Nicholas Fleischhauer
# SPDX-License-Identifier: GPL-3.0-or-later

import re


# Removes $ pairs and replaces them with \( \) and removes $$ pairs and replaced them with \[ \]

def convert_tex_math(file_path, output_file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace pairs of $$ with \[ and \]
    content = re.sub(r'\$\$(.*?)\$\$', r'\\[\1\\]', content, flags=re.DOTALL)

    # Replace pairs of $ with \( and \)
    # Ensure this is not replacing already replaced parts
    content = re.sub(r'(?<!\$)\$(.+?)\$(?!\$)', r'\\(\1\\)', content, flags=re.DOTALL)

    with open(output_file_path, 'w') as output_file:
        output_file.write(content)

    print(f"Converted file saved to: {output_file_path}")

# Example usage:
input_file = 'main.tex'  
output_file = 'fixed.tex'  

convert_tex_math(input_file, output_file)
