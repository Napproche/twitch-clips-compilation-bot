import logging
import constants


class Logger:
    def __init__(self, parameters):
        logging.basicConfig(
            filename=constants.ERROR_LOGGING_FILE, level=logging.WARNING, format='%(asctime)s %(message)s')
        self.start_script(parameters)

    def log(self, message, exception):
        logging.warning(message)
        logging.exception(exception)

    def start_script(self, parameters):
        message = 'Starting script: {0} with parameters: {1}, {2}, {3}, {4}, {5}'.format(
            parameters.script_name, parameters.destination.name, parameters.video_type.name, parameters.count, parameters.game.name, parameters.custom_thumbnails)

        logging.warn(
            '--------------------------------------------------------------------------------------')
        print(message)
        logging.warn(message)
        logging.warn(
            '--------------------------------------------------------------------------------------')
