import logging


FORMAT = logging.Formatter('%(asctime)-15s : %(levelname)s : %(message)s')


def get_logger(name, filename, level=logging.WARNING):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    stream = logging.StreamHandler()
    stream.setFormatter(FORMAT)
    logger.addHandler(stream)
    
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(FORMAT)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger