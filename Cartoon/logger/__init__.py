import logging
import os
from datetime import datetime

# Get the root directory dynamically
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Moves up 3 levels
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Corrected log path
log_dir = os.path.join(ROOT_DIR, 'log')
os.makedirs(log_dir, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(filename)s - %(levelname)s - %(message)s",  # Changed %(name)s to %(filename)s
    level=logging.INFO
)

# Also print logs to the terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(filename)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)

print("Log file will be stored in:", LOG_FILE_PATH)


# import logging
# import os
# from datetime import datetime
# from from_root import from_root


# LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# log_path = os.path.join(from_root(), 'log', LOG_FILE)

# os.makedirs(log_path, exist_ok=True)

# lOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# logging.basicConfig(
#     filename=lOG_FILE_PATH,
#     format= "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
#     level= logging.INFO
# )
