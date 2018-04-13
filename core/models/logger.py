import logging

class Logger:
    def __init__(self, filename):
        logging.basicConfig(filename=filename, level=logging.WARNING, format='%(asctime)s %(message)s')

    def log(self, message, exception):
        logging.warning(message)
        logging.exception(exception)
    
    def broadcast(self, message):
        logging.info('--------------------------------------------------------------------------------------')
        logging.info(message)
        logging.info('--------------------------------------------------------------------------------------')
