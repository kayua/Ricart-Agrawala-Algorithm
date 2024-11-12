#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
__Author__ = 'Kayuã Oleques'
__GitPage__ = 'unknown@unknown.com.br'
__version__ = '{1}.{0}.{0}'
__initial_data__ = '2024/10/20'
__last_update__ = '2024/10/22'
__credits__ = ['INF-UFRGS']


try:
    import sys
    import time
    import random
    import logging
    import threading

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

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ResourceRequester(threading.Thread):
    """
    Manages the periodic requests for a shared resource by a node in a distributed
    mutual exclusion algorithm. Inherits from threading.Thread to allow each node
    to make requests independently in a separate thread.

    Attributes:
        node: The node instance requesting access to the shared resource.
    """

    def __init__(self, node):
        """
        Initializes the ResourceRequester for a given node and sets it as a daemon thread.

        Args:
            node: The node that will be requesting access to the shared resource.
        """
        super().__init__(daemon=True)
        self.node = node
        logging.info(f"ResourceRequester initialized for Node {self.node.node_id}")

    def run(self):
        """
        Main loop that periodically makes requests for the shared resource.
        Waits a random time interval between requests, simulating natural
        request behavior for the resource.
        """
        while True:
            # Generate a random wait time between 5 and 10 seconds
            wait_time = random.uniform(5, 10)
            logging.info(f"Node {self.node.node_id} will request the resource in {wait_time:.2f} seconds")
            time.sleep(wait_time)

            # Log and print the resource request
            logging.info(f"Node {self.node.node_id} is requesting the resource")
            print(f"Process {self.node.node_id} is requesting the resource.")

            # Broadcast the request to other nodes
            self.node.broadcast_request()