import logging

def setup_logger(log_file="app.log"):
    logging.basicConfig(
        filename=log_file,    
        level=logging.INFO,     
        format='%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'   
    )

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)

def log_critical(message):
    logging.critical(message)