import logging
import os
import sys
import platform
import subprocess
import re
from typing import Union, Any, Callable
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

def ping_host(ip_address: str = 'localhost', show_success: bool = True, user_id: int = None, return_message: bool = False, timeout: int = 500, self=None ) -> Union[bool, tuple[bool, str]]:
    """
    Pings a given IP address and returns status and optionally a message.
    Args:
        ip_address (str): The IP address of the host to ping. Defaults to 'localhost'.
        show_success (bool, optional): If True, sends a message when the host is up. Defaults to True.
        user_id (str, optional): The user ID to send the message to. If None, no message is sent. Defaults to None.
        return_message (bool, optional): If True, returns (success, message) tuple. If False, returns just success. Defaults to False.
        timeout (int, optional): The timeout for the ping command in milliseconds. Defaults to 500 milliseconds.
    Returns:
        Union[bool, tuple[bool, str]]: Either just the success status (bool) or (success_status, message) tuple
    """
    try:
        logger.debug(f"Pinging {ip_address} with timeout {timeout}ms...")

        is_ipv6_address = is_ipv6(ip_address)
        param = "-n" if platform.system().lower() == "windows" else "-c"
        timeout_param = "-w" if platform.system().lower() == "windows" else "-W"
        parameters_list = ["ping", param, "1", timeout_param, str(timeout), ip_address]
        command_line = " ".join(parameters_list)
        
        try:
            result = subprocess.run(
                parameters_list,
                capture_output=True,
                text=True,
                check=True
            )
                
            logger.debug(f"Subprocess command: {command_line}")
            
            response = result.returncode
            logger.debug(f"Ping response for {ip_address}: {response}")
            logger.debug(f"Ping output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Ping command failed with error: {e}\n{command_line}\n{e.stdout}\n{e.stderr}")
            if return_message:
                return False, f"Ping command failed with error: \n{command_line}\n{e.stdout}\n{e.stderr}"
            return False
        except OSError as e:
            logger.error(f"OS error occurred while pinging {ip_address}: {e}\n{command_line}")
            if return_message:
                return False, f"OS error occurred while pinging {ip_address}: {e}\n{command_line}"
            return False

        # Send a Telegram message if an instance of bot was given
        if user_id and self:
            message = f"{ip_address} is up!\n{command_line}" if response == 0 else f"{ip_address} is down!\n{command_line}"
            logger.debug(message)
            self.send_message_by_api(user_id, message) if response != 0 or show_success else None
        
        if return_message:
            return response == 0, f"{ip_address} is up!\n{command_line}\n{result.stdout}" if response == 0 else f"{ip_address} is down!\n{e.stdout}\n{e.stderr}"
        
        return response == 0
            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(f"An error occurred while pinging {ip_address}: {e}, in {fname} at line {exc_tb.tb_lineno}")
        if return_message:
            return False, f"An error occurred while pinging {ip_address}: {e}, in {fname} at line {exc_tb.tb_lineno}"
        return False

if __name__ == "__main__":

    ip_address = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    show_success = sys.argv[2].lower() == 'true' if len(sys.argv) > 2 else True
    user_id = sys.argv[3] if len(sys.argv) > 3 else None
    timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 500

    result = ping_host(ip_address=ip_address, show_success=show_success, user_id=user_id, timeout=timeout)
    if result:
        logger.info(f"{ip_address} is up!")
    else:
        logger.error(f"{ip_address} is down!")

    # Just get the boolean status
    success = ping_host(ip_address="192.168.1.1")

    # Get both status and message
    success, message = ping_host(ip_address="192.168.1.1", return_message=True)
    logger.error(message)

    # Test with 192.168.1.1 and a timeout of 100 milliseconds
    success, message = ping_host(ip_address="192.168.1.1", return_message=True, timeout=100)
    logger.error(f"Test with 192.168.1.1 and 100ms timeout: {message}")