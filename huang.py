#!/usr/bin/env python3
import sys

def parse_after_keyword(file_path, keyword):
    parsed_data = []
    with open(file_path, 'r', errors='ignore') as f:
        # 1) skip until the keyword
        for line in f:
            if keyword in line:
                break

        # 2) now read every remaining line
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip blank lines

            # 3) split into fields and strip commas from each token
            tokens = [tok.strip(',') for tok in line.split()]

            # 4) convert numeric-looking tokens to floats
            row = []
            for tok in tokens:
                try:
                    row.append(float(tok))
                except ValueError:
                    row.append(tok)
            parsed_data.append(row)

    return parsed_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_output_file>")
        sys.exit(1)

    path = sys.argv[1]
    keyword = "Beginning the parallel mode approximation computations."
    data = parse_after_keyword(path, keyword)

    # report and preview
    print(f"Parsed {len(data)} rows after the keyword.\n")
    for row in data[7:55]:
        print(row)

    # example NumPy conversion:
    try:
        import numpy as np
        arr = np.array(data[7:55], dtype=float)
        print("\nNumPy array shape:", arr.shape)
    except Exception as e:
        print("\nNumPy conversion failed:", e)

    dq=arr[:,1]
    freq=arr[:,3]
    
    # constants
    hbar = 1.0545718e-34          # J·s
    c    = 2.99792458e10          # cm/s
    amu  = 1.660539e-27  
    amu_to_kg = 1.66053906660e-27       # kg per amu
    me_kg     = 9.1093837015e-31        # kg per electron mass
    angstrom_to_bohr = 1.0/0.529177210903e-10  # Å → a₀ (in m/m)

    # compute the conversion factor
    factor = np.sqrt(amu_to_kg/me_kg) * angstrom_to_bohr         # kg

    dq_SI   = dq * 1e-10* np.sqrt(amu)
    omega = 2*np.pi * c * freq

    dq_au=dq * (1.889716) * (np.sqrt(1822.89))
    omega_au=freq * (1/8065.579) * (1/27.211386245988)

    S = omega * dq_SI**2 / (2 * hbar) 
    S_au=0.5 * omega_au * dq_au**2

    print(S_au)




    



