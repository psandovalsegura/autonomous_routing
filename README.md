# autonomous_routing
This repo contains the domain of agent-based autonomous vehicle routing simulator.

## Requirements
1. Python 3.7.4
2. A copy of [NetLogo-5.3](https://ccl.northwestern.edu/netlogo/5.3.0/)

It is recommended that you use a Python [virtual environment](https://docs.python.org/3/library/venv.html) to manage the package installs that will be required. Ours is called "autorouting", so we initiate it with `source autorouting/bin/activate` and leave it with `deactivate`.


## How to use
1. From within netlogo.py, point `autonomous_routing =` to the path of your mars.nlogo file. This is the path to the model.
2. From within netlogo.py, point `netlogo_location =` to the path of your NetLogo 5.3 directory that you downloaded.
3. Run `pip3 install -r requirements.txt`

Now, to run Dijkstra's Algorithm on the simulator, type
```
python3 controller.py "dijkstra"
```

**Note**: According to [pyNetLogo docs](https://pynetlogo.readthedocs.io/en/latest/install.html) only headless mode (without GUI) is supported on Mac.
