#!/usr/bin/python3
# -*- coding: utf-8 -*-

__Author__ = 'Kayuã Oleques'
__GitPage__ = 'unknown@unknown.com.br'
__version__ = '{1}.{0}.{0}'
__initial_data__ = '2024/10/20'
__last_update__ = '2024/10/22'
__credits__ = ['INF-UFRGS']


try:
    import sys
    import logging

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

# Configure logging for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REQUEST = "REQUEST"
REPLY = "REPLY"


class MessageHandler:
    """
    Handles the sending and receiving of messages for a node participating
    in a distributed mutual exclusion algorithm.

    Attributes:
        node: The node instance that is using this MessageHandler.
        sock: The socket used to send and receive messages.
    """

    def __init__(self, node, sock):
        """
        Initializes the MessageHandler with a specific node and socket.

        Args:
            node: The node instance that this handler is associated with.
            sock: The socket through which messages are sent and received.
        """
        self.node = node
        self.sock = sock
        logging.info(f"MessageHandler initialized for Node {self.node.node_id}")

    def send_message(self, message, ip, port):
        """
        Sends a message to a specified IP and port.

        Args:
            message (str): The message content to send.
            ip (str): The destination IP address.
            port (int): The destination port.
        """
        self.sock.sendto(message.encode(), (ip, port))
        logging.info(f"Node {self.node.node_id} sent message: '{message}' to {ip}:{port}")

    def handle_message(self, message, address):
        """
        Processes incoming messages by identifying the type of message (REQUEST or REPLY)
        and delegating handling based on message content.

        Args:
            message (str): The received message content.
            address (tuple): The address (IP and port) of the sender.
        """
        logging.info(f"Node {self.node.node_id} received message: '{message}' from {address}")

        parts = message.split(":")
        if parts[0] == REQUEST:
            sender_id = int(parts[1])
            sender_timestamp = float(parts[2])
            logging.info(
                f"Node {self.node.node_id} handling REQUEST from Node {sender_id} with timestamp {sender_timestamp}")
            self.node.process_request(sender_id, sender_timestamp, address)

        elif parts[0] == REPLY:
            logging.info(f"Node {self.node.node_id} handling REPLY from {address}")
            self.node.process_reply()