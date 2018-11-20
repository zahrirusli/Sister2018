# Zatt

Zatt is a **distributed storage system** built on the [Raft](https://raft.github.io) consensus algorithm.

![logo](logo.svg)

It allows clients to share a **key-value** data structure (a python `dict`), that is automatically replicated to a high availability cluster.

The project aims to fully implement the algorithm described in the [raft paper](http://ramcloud.stanford.edu/raft.pdf); the following features have been implemented so far:

* Leader election
* Log replication
* Log compaction
* Membership changes

## Table of Contents
* [Architecture](architecture.md)
* [Running a Server](server.md)
* [Embedding a Client](client.md)
* [Reference](reference.md)


## Quickstart Tutorial
### Installation
Both the server and the client are shipped in the same
[package](https://pypi.python.org/pypi/raft/), which can be installed by several means:

**PyPI**

`$ pip3 install zatt`

**Pip & Github**

`$ pip3 install git+ssh://github.com/simonacca/zatt.git`

**Cloning**

```
$ git clone git@github.com:simonacca/zatt.git
$ cd zatt
$ git checkout develop
$ python3 setup.py install
```

Regardless of the installation method, you can check that the software works properly issuing  `$ zattd --help`.


### Spinning up a cluster
We will now start a 3 server cluster on the local machine, listening on ports `9000`, `9001` and `9002` respectively.


Start the first server node:

`$ zattd --address 127.0.0.1 --port 9000 --storage 0.persist --remote-address 127.0.0.1 --remote-port 9001 --remote-address 127.0.0.1 --remote-port 9002`

And the remaining ones in separate terminals:
```
$ zattd --address 127.0.0.1 --port 9001 --storage 0.persist --remote-address 127.0.0.1 --remote-port 9000 --remote-address 127.0.0.1 --remote-port 9002
$ zattd --address 127.0.0.1 --port 9002 --storage 0.persist --remote-address 127.0.0.1 --remote-port 9000 --remote-address 127.0.0.1 --remote-port 9001
```

A server can be configured with command-line options or with a config file,
in this example, we are going to use both.

First, create an empty folder and enter it:
`$ mkdir zatt_cluster && cd zatt_cluster`.

Now create a config file `zatt.conf` with the following content:
```
{"cluster": {
    "0": ["127.0.0.1", 5254],
    "1": ["127.0.0.1", 5255],
    "2": ["127.0.0.1", 5256]
 }
}
```

You can now run the first node:

`$ zattd -c zatt.conf --id 0 -s zatt.0.persist --debug`

This tells zattd to run the node with `id:0`, taking the info about address and port from the config file.

Now you can spin up a second node: open another terminal, navigate to `zatt_cluster` and issue:

`$ zattd -c zatt.conf --id 2 -s zatt.2.persist --debug`

Repeat for a third node, this time with `id:2`

### Interacting with the cluster

To interact with the cluster, we need a client. Open a python interpreter (`$ python`) and run the following commands:

```
In [1]: from zatt.client import DistributedDict
In [2]: d = DistributedDict('127.0.0.1', 5254)
In [3]: d['key1'] = 0
```

Let's retrieve `key1` from a second client:

Open the python interpreter on another terminal and run:

```
In [1]: from zatt.client import DistributedDict
In [2]: d = DistributedDict('127.0.0.1', 5254)
In [3]: d['key1']
Out[3]: 0
In [4]: d
Out[4]: {'key1': 0}
```

### Notes

Please note that in order to erase the log of a node, the corresponding `zatt.{id}.persist` folder has to be removed.

Also note that JSON, currently used for serialization, only supports keys of type `str` and values of type `int, float, str, bool, list, dict `.
