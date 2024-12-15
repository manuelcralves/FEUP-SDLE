# Shopping Lists on the Cloud 

SDLE Second Assignment of group T04G12

**Group members**

- Diogo Alves (up202410346@up.pt)
- Inês Almeida (up202004513@up.pt)
- Manuel Alves (up201906910@up.pt)

## Project Objective 

Development of a local-first shopping list application with data persistence on devices and in the cloud, using ZeroMQ for efficient communication, enabling collaboration and reliable backup.

## Requirements and Installation

Ensure you have Python installed on your system. The project depends on the following Python packages:

- `jsonlib-python3`

- `prettytable`

- `pyzmq`

If these packages are not already installed, you can install them using the following commands:

```
pip install jsonlib-python3
pip install prettytable
pip install pyzmq
```

## Usage

**Running the Broker**

Start the broker by running the `broker.py` script in a terminal:

```
python broker.py
```

**Running the Client**

You can run multiple clients by executing the `client.py` script in separate terminal windows. Pass the client name as an argument when starting the client:

```
python client.py client1
```

For additional clients, replace `client1` with a unique name:

```
python client.py client2
```

### Notes

- Ensure the broker is running before starting any clients.

- Clients must use unique names to avoid conflicts.