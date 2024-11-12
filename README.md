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
    Example: python3 main.py --process_id (ID Process) --listen_port 5050 --send_port 5050 --flask_port 5000 --address (IP Address)
    

### Input parameters:

    Arguments:

        --process_id            Process ID ()
        --number_processes      Number of processes
        --listen_port           Listening message port
        --send_port             Sending message port 
        --max_delay             Maximum delay communication
        --max_retries           Maximum retries message send
        --address               Local IP Address
        --flask_port            Flask port for frontend/backend communication
    --------------------------------------------------------------


## 3. Implemented semantics

![Execution](Resources/execution.png)

## 4. Requirements:

`pyfiglet 1.0.2`
`logging`