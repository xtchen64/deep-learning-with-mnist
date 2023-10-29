"""
This file contains common utility functions.
"""

def auto_assign(func):
    """
    Automatically assigns the parameters.
    """
    def wrapper(self, *args, **kwargs):
        keys = func.__code__.co_varnames[1:func.__code__.co_argcount]
        for key, value in zip(keys, args):
            setattr(self, key, value)

        for key, value in kwargs.items():
            setattr(self, key, value)
        
        func(self, *args, **kwargs)
        
    return wrapper

def write_results_to_file(acc, f1, model_name, filename="result.csv"):
    """
    Writes the results to the given file.
    :param acc: accuracy
    :param f1: f1 score
    :param model_name: name of the model
    :param filename: name of the file to write to
    """
    # Initialize header and data lines
    header = "model,acc,f1\n"
    data_line = f"{model_name},{acc},{f1}\n"

    # Check if file exists
    try:
        with open(filename, 'r') as file:
            content = file.readlines()

            # Check if header exists
            if content:
                if header.strip() not in content[0]:
                    content.insert(0, header)
            else:
                content.append(header)

            # Check if model line exists
            model_exists = False
            for line in content:
                if line.startswith(model_name):
                    model_exists = True
                    break
            
            if not model_exists:
                content.append(data_line)

            new_content = ''.join(content)

    except FileNotFoundError:
        new_content = header + data_line

    # Write the updated content back to the file
    with open(filename, 'w') as file:
        file.write(new_content)