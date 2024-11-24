import importlib
import inspect

def call_function(module_name: str, function_name: str, function_params: str) -> any:
    """
    Dynamically call a function from a module with specified parameters.

    Args:
        module_name (str): The name of the module.
        function_name (str): The name of the function.
        function_params (str): The parameters to pass to the function, as a string.

    Returns:
        any: The result of the function call.
    """
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        
        # Get the function from the module
        func = getattr(module, function_name)
        
        # strip the parameters string of any whitespace
        function_params = function_params.strip()
        
        if len(function_params) > 0:
            # create a list of each parameter
            function_params = function_params.split(",") 
            
            # Convert the function parameters to the correct types
            # function_params = convert_parameters_to_correct_type(module_name, function_name, function_params)
            
            # Convert the function parameters from list to a tuple
            params = tuple(function_params)
        else:
            params = ()
        
        # Call the function with the parameters and return the result
        result = func(*params)
        return result
    except Exception as e:
        return f"Error: {e}"

def convert_parameters_to_correct_type(module_name: str, function_name: str, parameter_values: list) -> list:
    """
    Given a function name and a list of parameter values, get the function signature
    and try to convert each item in the parameter list to the correct type.

    Args:
        module_name (str): The name of the module containing the function.
        function_name (str): The name of the function.
        parameter_values (list): The list of parameter values as strings.

    Returns:
        list: The list of parameter values converted to the correct types.
    """
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        
        # Get the function from the module
        func = getattr(module, function_name)
        
        # Get the function signature
        sig = inspect.signature(func)
        
        # Convert the parameter values to the correct types
        converted_params = []
        for param, value in zip(sig.parameters.values(), parameter_values):
            param_type = param.annotation
            if param_type == inspect.Parameter.empty:
                # If no type annotation is provided, assume the parameter is a string
                param_type = str
            try:
                converted_value = param_type(value)
            except ValueError:
                raise ValueError(f"Cannot convert parameter '{param.name}' to {param_type}")
            converted_params.append(converted_value)
        
        return converted_params
    except Exception as e:
        raise RuntimeError(f"Error converting parameters for function '{function_name}': {e}")

def hello_world(name: str) -> str:
    """
    Return a greeting message.

    Args:
        name (str): The name to include in the greeting.

    Returns:
        str: The greeting message.
    """
    return f"Hello, {name}!"

def hello_world_noparam() -> str:
    """
    Return a greeting message.

    Returns:
        str: The greeting message.
    """
    return "Hello World!"

# Example usage
if __name__ == "__main__":
    module_name = "math"
    function_name = "pow"
    function_params = "(2, 3)"  # Parameters as a string
    result = call_function(module_name, function_name, function_params)
    print(result)  # Output: 8.0

    # Example usage of hello_world function
    module_name = "util_functions"
    function_name = "hello_world"
    function_params = "('World',)"  # Parameters as a string
    result = call_function(module_name, function_name, function_params)
    print(result)  # Output: Hello, World!

    # Example usage of hello_world_noparam function
    module_name = "util_functions"
    function_name = "hello_world_noparam"
    function_params = "()"  # No parameters
    result = call_function(module_name, function_name, function_params)
    print(result)  # Output: Hello World!

    # Example usage of convert_parameters_to_correct_type function
    module_name = "math"
    function_name = "pow"
    parameter_values = ["2", "3"]
    converted_params = convert_parameters_to_correct_type(module_name, function_name, parameter_values)
    print(converted_params)  # Output: [2.0, 3.0]