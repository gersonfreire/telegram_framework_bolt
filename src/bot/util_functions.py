from importlib.metadata.diagnose import inspect
import logging
import os
import sys
import platform
import subprocess
import re
from typing import List, Union, Any, Callable
from inspect import signature
import importlib

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG to capture all messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Include date and time in the log messages
    handlers=[
        logging.StreamHandler(sys.stdout)  # Output log messages to the console
    ]
)

class CustomFormatter(logging.Formatter):
    """Custom logging formatter to add colors to log levels."""
    def format(self, record):
        log_colors = {
            logging.ERROR: "\033[91m",  # Red
            logging.WARNING: "\033[93m",  # Yellow
            logging.INFO: "\033[92m",  # Green
            logging.DEBUG: "\033[94m",  # Blue
        }
        reset_color = "\033[0m"
        log_color = log_colors.get(record.levelno, "")
        record.msg = f"{log_color}{record.msg}{reset_color}"
        return super().format(record)

# Update the handler to use the custom formatter
for handler in logging.getLogger().handlers:
    handler.setFormatter(CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)

def is_ipv6(address: str) -> bool:
    """Check if the given address is an IPv6 address."""
    return re.match(r'^[0-9a-fA-F:]+$', address) is not None

def get_and_convert_function(module_name: str, function_name: str) -> Callable:
    """
    Dynamically imports a function from a module and returns a wrapper that handles type conversion.
    
    Args:
        module_name (str): The name of the module containing the function
        function_name (str): The name of the function to import
    
    Returns:
        Callable: A wrapper function that handles type conversion for the target function
    
    Raises:
        ImportError: If the module or function cannot be imported
        AttributeError: If the function doesn't exist in the module
    """
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        # Get the function from the module
        func = getattr(module, function_name)
        # Get the function's signature
        sig = signature(func)

        def wrapper(*args, **kwargs):
            # Convert positional arguments
            converted_args = []
            for param_name, param in list(sig.parameters.items())[:len(args)]:
                annotation = param.annotation
                if annotation != param.empty:
                    try:
                        converted_args.append(annotation(args[len(converted_args)]))
                    except (ValueError, TypeError):
                        converted_args.append(args[len(converted_args)])
                else:
                    converted_args.append(args[len(converted_args)])

            # Convert keyword arguments
            converted_kwargs = {}
            for key, value in kwargs.items():
                if key in sig.parameters:
                    annotation = sig.parameters[key].annotation
                    if annotation != sig.parameters[key].empty:
                        try:
                            converted_kwargs[key] = annotation(value)
                        except (ValueError, TypeError):
                            converted_kwargs[key] = value
                    else:
                        converted_kwargs[key] = value

            # Call the function with converted arguments
            return func(*converted_args, **converted_kwargs)

        return wrapper

    except ImportError as e:
        logger.error(f"Failed to import module {module_name}: {e}")
        raise
    except AttributeError as e:
        logger.error(f"Function {function_name} not found in module {module_name}: {e}")
        raise
 
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
            
            # for each item on the parameter list, if it is non numerical, add quotes
            for i, param in enumerate(function_params):
                if not param.strip().isnumeric():
                    function_params[i] = f"'{param.strip()}'"
                    
            # join the list of parameters into a string
            function_params = f'({",".join(function_params)},)'
            
            # Convert the function parameters from string to a tuple
            params = eval(function_params)
        else:
            params = ()
        
        # Call the function with the parameters and return the result
        result = func(*params)
        return result
    except Exception as e:
        return f"Error: {e}"
 
# def convert_params(module_name: str, function_name: str, function_params: str) -> any:
def convert_params(function_params: str) -> any:
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
        # # Dynamically import the module
        # module = importlib.import_module(module_name)
        
        # # Get the function from the module
        # func = getattr(module, function_name)
        
        # strip the parameters string of any whitespace
        function_params = function_params.strip()
        
        if len(function_params) > 0:
            # create a list of each parameter
            function_params = function_params.split(",") 
            
            # for each item on the parameter list, if it is non numerical, add quotes
            for i, param in enumerate(function_params):
                if not param.strip().isnumeric():
                    function_params[i] = f"'{param.strip()}'"
                    
            # join the list of parameters into a string
            # function_params = f'({",".join(function_params)},)'
            function_params = f'[{",".join(function_params)},]'
            
            # Convert the function parameters from string to a tuple
            params = eval(function_params)
        else:
            params = ()
        
        # Call the function with the parameters and return the result
        # result = func(*params)
        # return result
        return params
    
    except Exception as e:
        return f"Error: {e}"

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

def call_and_convert_function(module_name: str, function_name: str, *args, **kwargs) -> Any:
    """
    Dynamically imports a function from a module, converts arguments to the correct types,
    and calls the function with the provided arguments.
    
    Args:
        module_name (str): The name of the module containing the function
        function_name (str): The name of the function to import
        *args: Variable positional arguments to pass to the function
        **kwargs: Variable keyword arguments to pass to the function
    
    Returns:
        Any: The result of the function call
    
    Raises:
        ImportError: If the module or function cannot be imported
        AttributeError: If the function doesn't exist in the module
    """
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        # Get the function from the module
        func = getattr(module, function_name)
        # Get the function's signature
        sig = signature(func)

        # Convert positional arguments
        converted_args = []
        for param_name, param in list(sig.parameters.items())[:len(args)]:
            annotation = param.annotation
            if annotation != param.empty:
                try:
                    converted_args.append(annotation(args[len(converted_args)]))
                except (ValueError, TypeError):
                    converted_args.append(args[len(converted_args)])
            else:
                converted_args.append(args[len(converted_args)])

        # Convert keyword arguments
        converted_kwargs = {}
        for key, value in kwargs.items():
            if key in sig.parameters:
                annotation = sig.parameters[key].annotation
                if annotation != sig.parameters[key].empty:
                    try:
                        converted_kwargs[key] = annotation(value)
                    except (ValueError, TypeError):
                        converted_kwargs[key] = value
                else:
                    converted_kwargs[key] = value

        # Call the function with converted arguments
        return func(*converted_args, **converted_kwargs)

    except ImportError as e:
        logger.error(f"Failed to import module {module_name}: {e}")
        raise
    except AttributeError as e:
        logger.error(f"Function {function_name} not found in module {module_name}: {e}")
        raise

def convert_parameters_to_correct_type(module_name: str, function_name: str, parameter_values: List[str]) -> List[Any]:
    """
    Given a function name and a list of parameter values, get the function signature
    and try to convert each item in the parameter list to the correct type.

    Args:
        module_name (str): The name of the module containing the function.
        function_name (str): The name of the function.
        parameter_values (List[str]): The list of parameter values as strings.

    Returns:
        List[Any]: The list of parameter values converted to the correct types.
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

if __name__ == "__main__":
        
    # from src.bot.util_functions import call_and_convert_function

    # Example string of arguments
    args_string = "2, 3"

    # Convert the string to a list of arguments
    args_list = [arg.strip() for arg in args_string.split(",")]

    # Convert the arguments to the appropriate types (e.g., int, float, etc.)
    # In this example, we assume the arguments are integers
    args_list = [int(arg) for arg in args_list]

    # Call the function with the unpacked arguments
    result = call_and_convert_function('math', 'pow', *args_list)

    print(result)  # Output: 8.0    

    # Example usage:
    result = call_and_convert_function('math', 'pow', 2, 3)  # Returns 8.0
    logger.info(f"Result: {result}")
    
    greeting = call_and_convert_function('util_functions', 'hello_world', name="World")  # Returns "Hello, World!"  
    logger.info(f"Greeting: {greeting}")  

    # Test the dynamic function import and conversion
    try:
        ping_function = get_and_convert_function('util_ping', 'ping_host')
        # Test with string timeout that should be converted to int
        success, message = ping_function(ip_address="192.168.1.1", timeout="200", return_message=True)
        logger.info(f"Dynamic function test result: {success}")
        logger.info(f"Dynamic function test message: {message}")
        
    except Exception as e:
        logger.error(f"Dynamic function test failed: {e}")

    ip_address = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    show_success = sys.argv[2].lower() == 'true' if len(sys.argv) > 2 else True
    user_id = sys.argv[3] if len(sys.argv) > 3 else None
    timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 500

    module_name = "math"
    function_name = "pow"
    function_params = "2, 3"  # Parameters as a string
    result = call_function(module_name, function_name, function_params)
    print(result)  # Output: 8.0

    # Example usage of hello_world function
    # module_name = "util_functions"
    # function_name = "hello_world"
    # function_params = "('World',)"  # Parameters as a string
    # result = call_function(module_name, function_name, function_params)
    # print(result)  # Output: Hello, World!

    # Example usage of hello_world_noparam function
    module_name = "util_functions"
    function_name = "hello_world_noparam"
    function_params = ""#"()"  # No parameters
    result = call_function(module_name, function_name, function_params)
    print(result)  # Output: Hello World!
    