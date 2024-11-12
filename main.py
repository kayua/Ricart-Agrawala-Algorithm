#!/usr/bin/python3
# -*- coding: utf-8 -*-

__Author__ = 'Kayuã Oleques'
__GitPage__ = 'unknown@unknown.com.br'
__version__ = '{1}.{0}.{0}'
__initial_data__ = '2024/10/20'
__last_update__ = '2024/10/22'
__credits__ = ['INF-UFRGS']


try:
    import os
    import sys
    import json
    import logging
    import argparse

    from Components.View import View

    from datetime import datetime
    from logging.handlers import RotatingFileHandler
    from Components.RicartAgrawalaNode import RicartAgrawalaNode

except ImportError as error:

    print(error)
    print()
    print("1. (optional) Setup a virtual environment: ")
    print("  python3 - m venv ~/Python3env/Ricart-Agrawala")
    print("  source ~/Python3env/Ricart-Agrawala/bin/activate ")
    print()
    print("2. Install requirements:")
    print("  pip3 install --upgrade pip")
    print("  pip3 install -r requirements.txt ")
    print()
    sys.exit(-1)


DEFAULT_IP_ADDRESS = "127.0.0.1"



def get_logs_path():
    """
    Returns the directory path for storing logs. Creates the directory if it doesn't exist.
    """
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def configure_logging(verbosity):
    """
    Configures the logging settings for the application, setting up both console
    and rotating file handlers based on the specified verbosity level.

    Args:
        verbosity (int): The logging level (e.g., logging.DEBUG, logging.INFO).
    """
    logger = logging.getLogger()
    logging_format = '%(asctime)s\t***\t%(message)s'

    if verbosity == logging.DEBUG:
        logging_format = '%(asctime)s\t***\t%(levelname)s {%(module)s} [%(funcName)s] %(message)s'

    LOGGING_FILE_NAME = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
    logging_filename = os.path.join(get_logs_path(), LOGGING_FILE_NAME)

    logger.setLevel(verbosity)

    # Set up rotating file handler with max file size and backup count
    rotating_file_handler = RotatingFileHandler(filename=logging_filename, maxBytes=1000000, backupCount=5)
    rotating_file_handler.setLevel(verbosity)
    rotating_file_handler.setFormatter(logging.Formatter(logging_format))

    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(verbosity)
    console_handler.setFormatter(logging.Formatter(logging_format))

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(rotating_file_handler)
    logger.addHandler(console_handler)

    logging.info("Logging configuration complete. Log file: %s", logging_filename)


def load_nodes(file_path):
    """
    Loads the node configurations from a JSON file.

    Args:
        file_path (str): The path to the JSON configuration file.

    Returns:
        list: A list of nodes loaded from the configuration file.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
        return data["nodes"]


def show_all_settings(arguments):
    """
    Logs all settings and command-line arguments after parsing.
    Displays the command used to run the script along with the
    corresponding values for each argument.

    Args:
        arguments (argparse.Namespace): The parsed command-line arguments.
    """
    # Log the command used to execute the script
    logging.info("Command:\n\t{0}\n".format(" ".join([x for x in sys.argv])))
    logging.info("Settings:")

    # Calculate the maximum length of argument names for formatting
    lengths = [len(x) for x in vars(arguments).keys()]
    max_length = max(lengths)

    # Log each argument and its value
    for keys, values in sorted(vars(arguments).items()):
        settings_parser = "\t" + keys.ljust(max_length, " ") + " : {}".format(values)
        logging.info(settings_parser)

    # Log a newline for spacing
    logging.info("")


def main():
    """
    Main function for initializing and starting the Ricart-Agrawala node application.
    Sets up logging, parses command-line arguments, loads node configurations,
    and starts a Ricart-Agrawala node instance.
    """
    # Set logging verbosity level
    configure_logging(logging.DEBUG)

    # Define command-line arguments for the script
    parser = argparse.ArgumentParser(description="Ricart-Agrawala Mutual Exclusion Algorithm")
    parser.add_argument("--node_id", type=int, help="ID of the current node.")
    parser.add_argument("--ip", type=str, help="IP of the current node.", default=DEFAULT_IP_ADDRESS)
    parser.add_argument("--port", type=int, help="Port of the current node.", default=5000)
    parser.add_argument("--config_path", type=str, default="nodes.json",
                        help="Path to the JSON configuration file for nodes.")

    args = parser.parse_args()

    # Initialize a View instance for displaying information
    view = View()
    view.print_view("Mutual Exclusion")

    # Log all settings for reference
    show_all_settings(args)

    logging.info("Loading nodes from configuration file: %s", args.config_path)
    nodes = load_nodes(args.config_path)

    # Initialize and start a Ricart-Agrawala node
    logging.info("Starting Ricart-Agrawala Node %d on %s:%d", args.node_id, args.ip, args.port)
    node = RicartAgrawalaNode(args.node_id, args.ip, args.port, nodes)
    node.start()


if __name__ == "__main__":
    main()