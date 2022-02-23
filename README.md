# QView
Simple graphical viewer for remote SLURM queues (tested on Norwegian HPCs Fram, Saga, and Betzy). Tested with Python 3.8.6.

## Install requirements
Set up a virtual environment like this

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Running QView
Run the program with

```bash
$ cd QView
$ python main.py
```

### Logging in to a cluster
After starting `main.py`, you will see the log-in window. Log in with your
username and password, selecting the appropriate cluster from the list.
