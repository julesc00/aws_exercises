#!/bin/bash

# Set the output directory (optional, can be the same as input)
output_directory="./processed"
mkdir -p "$output_directory"

# Function to process a single MP3 file
process_mp3() {
    local input_file="$1"
    local output_file="$output_directory/528hz_$(basename "$input_file")"
    
    echo "Processing $input_file -> $output_file"

    # Use ffmpeg to re-encode from 440Hz to 528Hz
    ffmpeg -i "$input_file" -af "asetrate=44100*1.2,aresample=44100,atempo=0.8333" -y "$output_file"
    
    if [[ $? -eq 0 ]]; then
        echo "Successfully processed: $input_file"
    else
        echo "Error processing: $input_file"
    fi
}

# Loop through all MP3 files in the current directory
for file in *.mp3; do
    if [[ -f "$file" ]]; then
        process_mp3 "$file"
    fi
done

echo "Processing complete. Check the '$output_directory' directory for output files."
