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
    import time
    import socket
    import logging
    import threading

    from datetime import datetime
    from MessageHandler import MessageHandler
    from ResourceRequester import ResourceRequester

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

REQUEST = "REQUEST"
REPLY = "REPLY"

class RicartAgrawalaNode:
    """
    Represents a node in a distributed system implementing the Ricart-Agrawala
    algorithm for mutual exclusion. Each node communicates with others to request
    access to a shared resource, ensuring mutual exclusion.

    Attributes:
        node_id (int): Unique identifier for the node.
        ip (str): IP address of the node.
        port (int): Port on which the node listens for messages.
        nodes (list): List of dictionaries representing all nodes in the system.
        requesting_cs (bool): Indicates if the node is currently requesting the critical section.
        reply_count (int): Tracks the number of replies received from other nodes.
        timestamp (float): Timestamp of the current request for the critical section.
        deferred_requests (list): List of node IDs whose requests were deferred.
        lock (threading.Lock): Lock to ensure thread-safe access to node attributes.
        sock (socket.socket): UDP socket used for communication.
        message_handler (MessageHandler): Handles sending and receiving messages.
    """

    def __init__(self, node_id, ip, port, nodes):
        """
        Initializes a new node in the Ricart-Agrawala mutual exclusion algorithm.

        Args:
            node_id (int): Unique identifier for this node.
            ip (str): IP address on which this node will listen.
            port (int): Port on which this node will listen.
            nodes (list): Information about other nodes in the system.
        """
        self.node_id = node_id
        self.ip = ip
        self.port = port
        self.nodes = nodes
        self.requesting_cs = False
        self.reply_count = 0
        self.timestamp = None
        self.deferred_requests = []
        self.lock = threading.Lock()

        # Set up UDP socket for communication
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.message_handler = MessageHandler(self, self.sock)

        logging.info(f"Node {self.node_id} initialized on {self.ip}:{self.port} with nodes: {self.nodes}")

    def broadcast_request(self):
        """
        Broadcasts a request to enter the critical section to all other nodes,
        sending the current timestamp to determine access priority.
        """
        with self.lock:
            self.timestamp = datetime.now().timestamp()
            self.requesting_cs = True
            self.reply_count = 0

        message = f"{REQUEST}:{self.node_id}:{self.timestamp}"
        logging.info(f"Node {self.node_id} broadcasting request with timestamp {self.timestamp}")

        for node in self.nodes:
            if node["id"] != self.node_id:
                self.message_handler.send_message(message, node["ip"], node["port"])
                logging.info(f"Node {self.node_id} sent request to Node {node['id']}")

    def process_request(self, sender_id, sender_timestamp, address):
        """
        Handles an incoming request from another node. If this node has higher priority
        or is not requesting the critical section, it replies immediately. Otherwise,
        it defers the request.

        Args:
            sender_id (int): ID of the requesting node.
            sender_timestamp (float): Timestamp of the request.
            address (tuple): Address of the sending node.
        """
        with self.lock:

            if not self.requesting_cs or (self.timestamp, self.node_id) > (sender_timestamp, sender_id):
                reply_message = f"{REPLY}:{self.node_id}"
                self.message_handler.send_message(reply_message, address[0], address[1])
                logging.info(f"Node {self.node_id} sent reply to Node {sender_id} at {address}")

            else:
                self.deferred_requests.append(sender_id)
                logging.info(f"Node {self.node_id} deferred request from Node {sender_id} with timestamp {sender_timestamp}")

    def process_reply(self):
        """
        Processes an incoming reply from another node. Once replies from all nodes
        are received, this node enters the critical section, simulates resource use,
        and then exits, sending deferred replies if needed.
        """
        with self.lock:
            self.reply_count += 1
            logging.info(f"Node {self.node_id} received reply, count: {self.reply_count}")

            if self.reply_count == len(self.nodes) - 1:
                logging.info(f"Node {self.node_id} entering critical section")
                logging.info(f"PROCESS {self.node_id} entered the critical section.")

                # Simulate critical section execution
                time.sleep(2)

                logging.info(f"PROCESS {self.node_id} exiting the critical section.")
                logging.info(f"Node {self.node_id} exiting critical section")

                self.requesting_cs = False
                self.reply_count = 0

                for node_id in self.deferred_requests:
                    deferred_node = next(n for n in self.nodes if n["id"] == node_id)
                    reply_message = f"{REPLY}:{self.node_id}"
                    self.message_handler.send_message(reply_message, deferred_node["ip"], deferred_node["port"])
                    logging.info(f"Node {self.node_id} sent deferred reply to Node {node_id}")

                self.deferred_requests.clear()

    def listen(self):
        """
        Listens for incoming messages from other nodes. When a message is received,
        it is decoded and passed to the MessageHandler for processing.
        """
        logging.info(f"Node {self.node_id} started listening for incoming messages")
        while True:
            data, address = self.sock.recvfrom(1024)
            message = data.decode()
            logging.info(f"Node {self.node_id} received message: {message} from {address}")
            self.message_handler.handle_message(message, address)

    def start(self):
        """
        Starts the node's listener and requester threads. The listener thread
        continuously listens for incoming messages, and the requester thread
        periodically requests access to the critical section.
        """
        logging.info(f"Node {self.node_id} starting listener and requester threads")
        listener_thread = threading.Thread(target=self.listen, daemon=True)
        listener_thread.start()
        requester_thread = ResourceRequester(self)
        requester_thread.start()
        listener_thread.join()
        requester_thread.join()