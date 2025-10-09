def binary_to_hex(file_path, output_file=None):
    """
    Convert a binary file to hexadecimal representation.
    
    Args:
        file_path (str): Path to the binary file
        output_file (str, optional): Path to save hex output. If None, prints to console.
    """
    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()
            hex_data = binary_data.hex()
            
            # Format hex data with spaces for readability (optional)
            formatted_hex = ' '.join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))
            
            if output_file:
                with open(output_file, 'w') as out_file:
                    out_file.write(formatted_hex)
                print(f"Hex data saved to {output_file}")
            else:
                print(formatted_hex)
                
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # Replace 'input.bin' with your binary file path
    binary_to_hex("C:/Users/louis/Dropbox/FYP/Data/hmt_flight_test2_20251007/down_antenna_all.ubx",
                   "C:/Users/louis/Dropbox/FYP/Data/hmt_flight_test2_20251007/down_antenna_all_hex.ubx")
    
    # Or save to a file
    # binary_to_hex('input.bin', 'output.hex')