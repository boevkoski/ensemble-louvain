# Ensemble Louvain

Ensemble Louvain is a parallelized Python implementation of the community detection algorithm suitable for community evolution, presented and applied in the following works:

* Evkoski, Bojan, et al. "Community evolution in retweet networks." Plos one 16.9 (2021): e0256175: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0256175
* Evkoski, Bojan, et al. "Retweet communities reveal the main sources of hate speech." PloS one 17.3 (2022): e0265602: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0265602
* Evkoski, Bojan, et al. "Evolution of topics and hate speech in retweet network communities." Applied Network Science 6.1 (2021): 1-20: https://appliednetsci.springeropen.com/articles/10.1007/s41109-021-00439-7

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
