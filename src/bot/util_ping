import logging
import os
import sys
import platform
import subprocess

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

def ping_host(self=None, ip_address: str = 'localhost', show_success: bool = True, user_id: int = None) -> bool:
    """
    Pings a given IP address and sends a message indicating whether the host is up or down.
    Args:
        ip_address (str): The IP address of the host to ping. Defaults to 'localhost'.
        show_success (bool, optional): If True, sends a message when the host is up. Defaults to True.
        user_id (str, optional): The user ID to send the message to. If None, no message is sent. Defaults to None.        
    Returns:
        Bool: True if the host is up, False if the host is down.
    Raises:
        Exception: If an error occurs during the ping process, an error message is sent to the bot owner.    
    """
    
    try:
        logger.debug(f"Pinging {ip_address}...")

        param = "-n" if platform.system().lower() == "windows" else "-c"
        
        try:
            result = subprocess.run(
                ["ping", param, "1", ip_address],
                capture_output=True,
                text=True,
                check=True
            )
            response = result.returncode
            logger.debug(f"Ping response for {ip_address}: {response}")
            logger.debug(f"Ping output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Ping command failed with error: {e.stderr}")
            return False
        except OSError as e:
            logger.error(f"OS error occurred while pinging {ip_address}: {e}")
            return False

        # Send a Telegram message if an instance of bot was given
        if user_id and self:
            message = f"{ip_address} is up!" if response == 0 else f"{ip_address} is down!"
            logger.debug(message)
            self.send_message_by_api(user_id, message) if response != 0 or show_success else None
        
        return response == 0
            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(f"An error occurred while pinging {ip_address}: {e}, in {fname} at line {exc_tb.tb_lineno}")
        return False

if __name__ == "__main__":

    ip_address = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    show_success = sys.argv[2].lower() == 'true' if len(sys.argv) > 2 else True
    user_id = sys.argv[3] if len(sys.argv) > 3 else None

    result = ping_host(ip_address=ip_address, show_success=show_success, user_id=user_id)
    if result:
        logger.info(f"{ip_address} is up!")
    else:
        logger.error(f"{ip_address} is down!")