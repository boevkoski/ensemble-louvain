# Ensemble Louvain

Ensemble Louvain is a Python implementation of the Ensemble Louvain algorithm presented at the Networks 2021 Conference. Detailed experiment results and comparisons soon...

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install elouvain.

```bash
pip install elouvain
```

## Usage

```python
from elouvain import ensemble_louvain
import networkx as nx

if __name__ == '__main__':
    G = nx.karate_club_graph() # create the well-known karate club network
    partition = ensemble_louvain.detect(G) # apply Ensemble Louvain on the graph
    partition[1] # get community label for node 1
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
