#!/bin/bash

# --- Function to recursively print the directory tree with proper lines ---
# $1: The path to the directory/file to be listed
# $2: The prefix string (e.g., "│   " or "    ") for indentation
tree_recursive() {
    local target="$1"
    local prefix="$2"
    
    # Use glob to find all non-hidden contents (files and directories)
    # The 'shopt -s nullglob' ensures nothing happens if no files are found
    shopt -s nullglob dotglob
    
    # Array to hold the list of contents, sorted for clean display
    local contents=("$target"/*)
    
    # Loop variables
    local count=${#contents[@]}
    local i=0

    # Loop through all files and directories in the target path
    for entry in "${contents[@]}"; do
        i=$((i + 1))
        local name=$(basename "$entry")
        
        # Check if this is the last item in the list
        if [ "$i" -eq "$count" ]; then
            # If it's the last item, use the L-shaped corner symbol (└──)
            local line_symbol="└── "
            local new_prefix="${prefix}    " # No vertical line for the next level
        else
            # If it's not the last, use the T-shaped symbol (├──)
            local line_symbol="├── "
            local new_prefix="${prefix}│   " # Use a vertical line for the next level
        fi
        
        # Print the current entry
        echo -e "${prefix}${line_symbol}${name}"

        # If the entry is a directory (and not a symbolic link), recurse
        if [[ -d "$entry" && ! -L "$entry" ]]; then
            tree_recursive "$entry" "$new_prefix"
        fi
    done
}

# --- Main script execution ---

# Get the starting directory (default to the current directory '.')
START_DIR="${1:-.}"

echo "$START_DIR"

# Start the recursive function
tree_recursive "$START_DIR" ""
