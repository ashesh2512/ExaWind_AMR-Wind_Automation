import re

# Declare path of file you wish to check
file_path = "/Users/srichard/Downloads/AMR Base File.inp"

# Create function to check for different variable types

def is_real_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_boolean(value):
    if value.lower() in ['true', 'false']:
        return True
    try:
        # Also consider 0 as False and 1 as True
        num_value = int(value)
        return num_value in [0, 1]
    except ValueError:
        return False

def is_string(value):
    return isinstance(value, str)

def is_valid_file_name(value):
    # Regular expression to check if the value is a valid file name in the format "name.type"
    file_name_pattern = r'^[\w\-]+[.][\w]+$'
    return bool(re.match(file_name_pattern, value))

def is_list_of_3_real_numbers(value):
    try:
        numbers = value.split()
        if len(numbers) != 3:
            return False
        for num in numbers:
            if not is_real_number(num):
                return False
        return True
    except:
        return False

def is_list_of_3_integers(value):
    try:
        numbers = value.split()
        if len(numbers) != 3:
            return False
        for num in numbers:
            if not is_integer(num):
                return False
        return True
    except:
        return False

def is_list_of_4_real_numbers(value):
    try:
        numbers = value.split()
        if len(numbers) != 4:
            return False
        for num in numbers:
            if not is_real_number(num):
                return False
        return True
    except:
        return False
    
def is_list_of_2_integers(value):
    try:
        numbers = value.split()
        if len(numbers) != 2:
            return False
        for num in numbers:
            if not is_integer(num):
                return False
        return True
    except:
        return False
    
def is_list_of_2_real_numbers(value):
    try:
        numbers = value.split()
        if len(numbers) != 2:
            return False
        for num in numbers:
            if not is_real_number(num):
                return False
        return True
    except:
        return False
    
def is_list_of_3_booleans(value):
    try:
        booleans = value.split()
        if len(booleans) != 3:
            return False
        for boolean in booleans:
            if not is_boolean(boolean):
                return False
        return True
    except:
        return False
    
def is_list_of_strings(value):
    try:
        strings = value.split()
        return all(is_string(s) for s in strings)
    except:
        return False

def is_file_path(comment):
    return "file path" in comment.lower()

def extract_variable_declaration(line):
    # Use regular expression to extract the variable name and value
    match = re.match(r'^\s*([^#]+?)\s*=\s*(.*?)\s*(?:#.*)?$', line)
    if match:
        variable = match.group(1).strip()
        value = match.group(2).strip()
        return variable, value

    return None, None

def is_from_list(value, valid_list):
    return value.strip() in valid_list

def error_checker(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    errors = []

    for line in lines:
        variable, value = extract_variable_declaration(line)
        if variable is not None:
            # Check if there's a comment in brackets and extract the expected data type if available
            data_type_match = re.search(r'\[(.*?)\]', line)
            if data_type_match:
                data_type_comment = data_type_match.group(1).lower()
                if data_type_comment:
                    if 'file path' in data_type_comment:
                        # Ignore the variable with "file path" type
                        continue
                    elif 'list of 3 real numbers' in data_type_comment:
                        if not is_list_of_3_real_numbers(value):
                            errors.append(f"Error: '{variable}' should be a list of 3 real numbers (e.g., '1.0 2.0 3.0'), but found '{value}'")
                    elif 'list of 3 integers' in data_type_comment:
                        if not is_list_of_3_integers(value):
                            errors.append(f"Error: '{variable}' should be a list of 3 integers (e.g., '1 2 3'), but found '{value}'")
                    elif 'list of 4 real numbers' in data_type_comment:
                        if not is_list_of_4_real_numbers(value):
                            errors.append(f"Error: '{variable}' should be a list of 4 real numbers (e.g., '1.0 2.0 3.0 4.0'), but found '{value}'")
                    elif 'list of 2 integers' in data_type_comment:
                        if not is_list_of_2_integers(value):
                            errors.append(f"Error: '{variable}' should be a list of 2 integers (e.g., '1 2'), but found '{value}'")
                    elif 'list of 2 real numbers' in data_type_comment:
                        if not is_list_of_2_real_numbers(value):
                            errors.append(f"Error: '{variable}' should be a list of 2 real numbers (e.g., '1.0 2.0'), but found '{value}'")
                    elif 'list of 3 booleans' in data_type_comment:
                        if not is_list_of_3_booleans(value):
                            errors.append(f"Error: '{variable}' should be a list of 3 booleans (True or False), but found '{value}'")
                    elif 'list of strings' in data_type_comment:
                        if not is_list_of_strings(value):
                            errors.append(f"Error: '{variable}' should be a list of strings, but found '{value}'")
                    elif 'real number' in data_type_comment:
                        if not is_real_number(value):
                            errors.append(f"Error: '{variable}' should be a real number, but found '{value}'")
                    elif 'integer' in data_type_comment:
                        if not is_integer(value):
                            errors.append(f"Error: '{variable}' should be an integer, but found '{value}'")
                    elif 'boolean' in data_type_comment:
                        if not is_boolean(value):
                            errors.append(f"Error: '{variable}' should be a boolean (True or False), but found '{value}'")
                    elif 'list of strings' in data_type_comment:
                        # No further check for list of strings
                        pass
                    elif 'string' in data_type_comment:
                        if not is_string(value):
                            errors.append(f"Error: '{variable}' should be a string, but found '{value}'")
                    elif 'file name' in data_type_comment:
                        if not is_valid_file_name(value):
                            errors.append(f"Error: '{variable}' should be a valid file name (format: 'name.type'), but found '{value}'")
                    elif 'wall_model' in data_type_comment:
                        wall_model_types = ['periodic', 'pressure_inflow', 'pressure_outflow', 'mass_inflow', 'no_slip_wall', 'slip_wall', 'symmetric_wall', 'wall_model']
                        if not is_from_list(value, wall_model_types):
                            errors.append(f"Error: '{variable}' should be one of {wall_model_types}, but found '{value}'")
                    elif 'ActuatorForcing' in data_type_comment:
                        ActuatorForcing_types = ['BoussinesqBuoyancy', 'CoriolisForcing', 'ABLForcing', 'BodyForce', 'ABLMeanBoussinesq', 'ActuatorForcing']
                        if not is_from_list(value, ActuatorForcing_types):
                            errors.append(f"Error: '{variable}' should be one of {ActuatorForcing_types}, but found '{value}'")
                    elif 'PlaneSampler' in data_type_comment:
                        PlaneSampler_types = ['PlaneSampler', 'LineSampler', 'LidarSampler', 'ProbeSampler']
                        if not is_from_list(value, PlaneSampler_types):
                            errors.append(f"Error: '{variable}' should be one of {PlaneSampler_types}, but found '{value}'")

            # Check incflo.physics against the list of valid strings
            if 'incflo.physics' in variable:
                valid_physics = ['FreeStream', 'SyntheticTurbulence', 'ABL', 'Actuator', 'RayleighTaylor', 'BoussinesqBubble', 'TaylorGreenVortex']
                if value not in valid_physics:
                    errors.append(f"Error: 'incflo.physics' should be one of {valid_physics}, but found '{value}'")

            # Check incflo.godunov_type against the list of valid strings
            if 'incflo.godunov_types' in variable:
                valid_physics = ['plm', 'ppm', 'ppm_nolim', 'weno_js', 'weno_z']
                if value not in valid_physics:
                    errors.append(f"Error: 'incflo.godunov_type' should be one of {valid_physics}, but found '{value}'")

            # Check turbulence.model against the list of valid strings
            if 'turbulence.model' in variable:
                valid_physics = ['Laminar', 'Smagorinsky', 'KOmegaSST', 'OneEqKsgsM84']
                if value not in valid_physics:
                    errors.append(f"Error: 'turbulence.model' should be one of {valid_physics}, but found '{value}'")

            # Check incflo.post_processing against the list of valid strings
            if 'incflo.post_processing' in variable:
                valid_physics = ['Sampling', 'KineticEnergy', 'Enstrophy', 'Averaging']
                declared_values = value.split()
                for val in declared_values:
                    if val not in valid_physics:
                        errors.append(f"Error: 'incflo.post_processing' should be one or more of {valid_physics}, but found '{val}'")

            # Check ABL.bndry_planes against the list of valid strings
            if 'ABL.bndry_planes' in variable:
                valid_physics = ['xlo', 'xhi', 'ylo', 'yhi', 'zlo', 'zhi']
                declared_values = value.split()
                for val in declared_values:
                    if val not in valid_physics:
                        errors.append(f"Error: 'ABL.bndry_planes' should be one or more of {valid_physics}, but found '{val}'")

            # Check if gravity is not =~ -9.81
            if 'incflo.gravity' in variable:
                declared_value = value.split()
                z_value = float(declared_value[2])
                if z_value > -9.8 or z_value < -10:
                    errors.append(f"Error: 'Are you sure you don't want gravity to be [0 0 -9.81]? It is currently {z_value}'")

            # Check if denisty is not =~ 1.225
            if 'incflo.density' in variable:
                declared_value = value.split()
                d_value = float(declared_value[0])
                if d_value < 1.2 or d_value > 1.3:
                    errors.append(f"Error: 'Are you sure you don't want density to be 1.225? It is currently {declared_value}'")

            # Check if laminar prandtl is not =~ 0.7
            if 'transport.laminar_prandtl' in variable:
                declared_value = value.split()
                d_value = float(declared_value[0])
                if d_value < 0.65 or d_value > 0.75:
                    errors.append(f"Error: 'Are you sure you don't want laminar prandtl to be 0.7? It is currently {declared_value}'")

            # Check if amr.max_grid_size is divisible by amr.blecking_factor
            if 'amr.max_grid_size' in variable:
                max_grid_size = int(value)
                if max_grid_size % 8 != 0:
                    errors.append("Error: 'amr.max_grid_size' should be divisible by 8 unless 'amr.blocking_factor' has been declared")

    return errors

# Example usage:
errors = error_checker(file_path)

if errors:
    print("Errors found:")
    for error in errors:
        print(error)
else:
    print("No errors found.")
