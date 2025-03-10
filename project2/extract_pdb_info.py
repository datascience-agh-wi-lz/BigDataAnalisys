import numpy as np
import sys
import os
from datetime import datetime

# Function to parse PDB file and extract atomic coordinates
def extract_coordinates(pdb_file):
    coordinates = []
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM') or line.startswith('HETATM'):  # Extract atom lines
                # Extract x, y, z coordinates (columns 30-38, 38-46, 46-54)
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                coordinates.append([x, y, z])
    return np.array(coordinates)

# Function to calculate the distance matrix (contact map)
def calculate_contact_map(coordinates):
    n = len(coordinates)
    contact_map = np.zeros((n, n))  # Initialize a square matrix of size n x n

    for i in range(n):
        for j in range(i + 1, n):  # Only calculate upper triangle (symmetric matrix)
            # Calculate Euclidean distance between atoms i and j
            distance = np.linalg.norm(coordinates[i] - coordinates[j])
            contact_map[i, j] = distance
            contact_map[j, i] = distance  # Symmetric

    return contact_map

# Main function
def main(pdb_file, metadata):
    # Extract atomic coordinates from the PDB file
    coordinates = extract_coordinates(pdb_file)
    contact_map = calculate_contact_map(coordinates)
    
    print(f"Processing PDB file: {pdb_file}")
        
    # Determine file name without path and extension
    if '/' in pdb_file:
        name = pdb_file.split('/')[-1].split('.')[0]
    else:
        name = pdb_file.split('\\')[-1].split('.')[0]
        
    print(f"Extracted name: {name}")
    metadata_dict = {
        'Name': name,
        'Class': metadata[0],
        'Architecture': metadata[1],
        'Topology': metadata[2],
        'Homologous Superfamily': metadata[3],
        "Contact Map": contact_map.tolist()  # Convert numpy array to list for saving
    }
    
    # Construct file name and check if it already exists
    output_file = f'{name}_contact_map.npy'
    if os.path.exists(output_file):
        print(f"Warning: File {output_file} already exists. Adding timestamp to avoid overwriting.")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'{name}_contact_map_{timestamp}.npy'
    
    try:
        # Save dict to a file
        np.save(output_file, metadata_dict)
        print(f"File saved successfully: {output_file}")
    except Exception as e:
        print(f"Error while saving file {output_file}: {e}")

# Entry point
if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("Usage: python extract_pdb_info.py <input_pdb_file> <Class> <Architecture> <Topology> <Homologous Superfamily>")
        sys.exit(1)
    
    pdb_file = sys.argv[1]  # First argument is the PDB file
    metadata = sys.argv[2:]  # The rest of the arguments are metadata columns
    main(pdb_file, metadata)
