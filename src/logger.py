import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,
)

print("The Error in the file is printed here ------------>", "%(message)s")

if __name__=="__main__":
    logging.info("Logging has started")         ## logging.info initiates the looging.basicConfig method and creates the file
                                                ## logging.basicConfig is global, no matter in which ever the file it is, when we initiate the logging.info, it initiates the method
                                                ## But, wither we have to import that file or import the logging package

