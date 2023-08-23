import os

# these need to be updated to your preferences
output_folder = '/Users/srichard/Downloads/'
precursor_file_name = 'precursor_data.inp'

def extract_section_data(base_file, section_name):
    section_data = {}
    in_section = False
    section_header = f"{section_name}\n"

    with open(base_file, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip() == section_header.strip():
            in_section = True
            section_data[section_name] = []
        elif line.startswith(';') and in_section:
            break
        elif in_section:
            section_data[section_name].append(line.strip())

    return section_data



def output_spinup_data(base_file):
    return extract_section_data(base_file, '; Spinup')


def output_precursor_data(base_file):
    return extract_section_data(base_file, '; Precursor')


def output_turbines_data(base_file):
    return extract_section_data(base_file, '; Turbines')

output_file_spinup = os.path.join(output_folder, 'spinup_data.inp')

base_file_name = 'AMR Base File'
base_file = output_folder + base_file_name

spinup_data = output_spinup_data(base_file)
precursor_data = output_precursor_data(base_file)
turbines_data = [extract_section_data(base_file, '; Turbines')]


# Generate spinup file
def write_spinup_data_to_inp(spinup_data, output_file_spinup):
    with open(output_file_spinup, 'w') as file:
        file.write('; Spinup\n')
        for line in spinup_data.get('; Spinup', []):
            file.write(f"{line}\n")

        # Print extracted data for verification
        print("Extracted Spinup Data:")
        for line in spinup_data.get('; Spinup', []):
            print(line)

write_spinup_data_to_inp(spinup_data, output_file_spinup)


# Generate precursor file
def combine_spinup_and_precursor(spinup_data, precursor_data, output_file_precursor):
    combined_data = spinup_data.copy()

    # Update spinup variables with new values from precursor data
    precursor_section = precursor_data.get('; Precursor')
    if precursor_section:
        for i, line in enumerate(combined_data['; Spinup']):
            if "=" in line:
                key, value = line.split("=", 1)
                spinup_key = key.strip()
                for precursor_line in precursor_section:
                    if "=" in precursor_line:
                        precursor_key, precursor_value = precursor_line.split("=", 1)
                        if precursor_key.strip() == spinup_key:
                            combined_data['; Spinup'][i] = f"{spinup_key} = {precursor_value.strip()}"
                            precursor_section.remove(precursor_line)  # Remove the processed line
                            break

    # Add new variables from precursor section
    if precursor_section:
        if '; Precursor' not in combined_data:
            combined_data['; Precursor'] = []
        for line in precursor_section:
            combined_data['; Precursor'].append(line)

    with open(output_file_precursor, 'w') as file:
        for section, lines in combined_data.items():
            file.write(f"{section}\n")
            for line in lines:
                file.write(f"{line}\n")

output_file_precursor = os.path.join(output_folder, precursor_file_name)
combine_spinup_and_precursor(spinup_data, precursor_data, output_file_precursor)

def inp_file_to_dict(filename):
    result_dict = {}
    current_key = None
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespaces and newlines
            if line.startswith(";"):
                current_key = line
                result_dict[current_key] = []
            elif current_key is not None:
                result_dict[current_key].append(line)
    return result_dict

file_path = output_folder + precursor_file_name
precursor_data_use = inp_file_to_dict(file_path)

# Generate turbines file
def combine_precursor_and_turbine(precursor_data_use, turbines_data, output_file_turbines):
    combined_data = precursor_data_use.copy()

    # Update precursor variables with new values from turbines data
    turbines_section = turbines_data[0].get('; Turbines')
    if turbines_section:
        for i, line in enumerate(combined_data['; Precursor']):
            if "=" in line:
                key, value = line.split("=", 1)
                precursor_key = key.strip()
                for turbine_line in turbines_section:
                    if "=" in turbine_line:
                        turbine_key, turbine_value = turbine_line.split("=", 1)
                        if turbine_key.strip() == precursor_key:
                            combined_data['; Precursor'][i] = f"{precursor_key} = {turbine_value.strip()}"
                            turbines_section.remove(turbine_line)  # Remove the processed line
                            break

    # Add new variables from turbines section
    if turbines_section:
        if '; Turbines' not in combined_data:
            combined_data['; Turbines'] = []
        for line in turbines_section:
            combined_data['; Turbines'].append(line)

    with open(output_file_turbines, 'w') as file:
        for section, lines in combined_data.items():
            file.write(f"{section}\n")
            for line in lines:
                file.write(f"{line}\n")

output_file_turbines = os.path.join(output_folder, 'turbines_data.inp')
combine_precursor_and_turbine(precursor_data_use, turbines_data, output_file_turbines)

