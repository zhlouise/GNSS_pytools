import pandas as pd
import glob

def convert_txt_to_csv(txt_files, output_csv):
    # Initialize an empty DataFrame to hold all data
    combined_data = pd.DataFrame()

    for file in txt_files:
        # Read the space-delimited file, using regex to handle multiple spaces as delimiters
        data = pd.read_csv(file, delim_whitespace=True)
        
        # Append the data to the combined DataFrame
        combined_data = pd.concat([combined_data, data], ignore_index=True)

    # Write the combined DataFrame to a CSV file
    combined_data.to_csv(output_csv, index=False)

# List of your TXT files
txt_files = ['C:/Users/louis/OneDrive/Desktop/1.txt','C:/Users/louis/OneDrive/Desktop/2.txt']  # Replace with your actual file names

# Output CSV file name
output_csv = 'C:/Users/louis/OneDrive/Desktop/combined_output.csv'

# Convert the TXT files to CSV
convert_txt_to_csv(txt_files, output_csv)

print(f"Successfully converted {len(txt_files)} TXT files to {output_csv}.")
