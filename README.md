![SysOP](Resources/ScreenSysOp.png)
# Ricart-Agrawala Algorithm
This code implements a simulated version of the Ricart-Agrawala mutual exclusion algorithm, which is a distributed method for ensuring exclusive access of processes to a critical section in distributed systems. The algorithm uses inter-process messages to coordinate access and avoid conflicts, relying on a request and defer policy. Through this mechanism, processes exchange access requests that are ordered to ensure that only one process enters the critical section at a time, promoting efficient synchronization and minimizing the number of required messages.
## 1. Steps to Install:



### 1. Upgrade and update
   ```bash   
   sudo apt-get update
   sudo apt-get upgrade 
   ```
### 2. Installation of application and internal dependencies

    git clone https://github.com/kayua/Ricart-Agrawala-Algorithm.git
    pip install -r requirements.txt

   
## 2. Run experiments:


### 1. Run (main.py) Server Mode
    
    python3 main.py (arguments)
    Example: python3 main.py --node_id (IP Address) --port (Port Number)
    

### Input parameters:

    Arguments:
        --node_id               ID of the current node.
        --ip                    IP of the current node.
        --port                  Port of the current node.
        --config_path           Path to the JSON configuration file for nodes.

    --------------------------------------------------------------


## 4. Requirements:

`pyfiglet 1.0.2`
`logging`