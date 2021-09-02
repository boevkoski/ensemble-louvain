import community as louvain
import networkx as nx
import itertools
import multiprocessing as mp

results = []
lock = mp.Lock()

def detect(network, weight='weight',
           partitions=100,
           matching_threshold=0.99,
           resolution=1,
           on_giant_component=False,
           cores=1):
    """Computes the partition of the graph nodes by the Ensemble Louvain
    Parameters
    ----------
    network : networkx.Graph
       the networkx graph which is decomposed
    weight : str, optional
        the key in graph to use as weight. Default to 'weight'
    partitions : int, optional
        number of runs of Louvain in the Ensemble
    matching_threshold : float, optional
        controls when do two nodes belong to the same community. E.g. matching_threshold of 0.9
        will place two nodes in the same community if in 90% of the partitions they appear together
    resolution :  double, optional
        Will change the size of the communities, default to 1.
        represents the time described in
        "Laplacian Dynamics and Multiscale Modular Structure in Networks",
        R. Lambiotte, J.-C. Delvenne, M. Barahona
    on_giant_component : bool, optional
        if True, Ensemble Louvain will be applied on the giant component instead of the whole network
    cores : int, optional
        number of cores on which Ensemble Louvain will execute
    Returns
    -------
    partition : list
       The partition, with communities sorted by community size
   """

    # transform to giant component if "on_giant_component" is True
    network = _giant_component(network) if on_giant_component else network

    # calculate the matching dictionary between each pair of nodes
    matching_dict = _calculate_matching_scores(network, weight, partitions, resolution, cores)

    # create the meta-network out of the node matchings
    meta_network = _create_metanetwork(network, matching_dict, partitions, matching_threshold)

    # identify the connected components in the meta-network
    partition = list(nx.connected_components(meta_network))

    partition = [list(community) for community in partition]

    i = 0
    predictions = {}
    for community in partition:
        for node in community:
            predictions[node] = i
        i += 1

    return predictions


def _create_metanetwork(network, matching_dict, partitions, matching_threshold):
    """Creates the Ensemble Louvain meta-network
    Parameters
    ----------
    network : networkx.Graph
       the networkx graph which which Ensemble Louvain is applied on
    matching_dict : dict
        the matching dictionary created in the previous step of the Ensemble Louvain
        where key is a frozenset of nodes and value is the comemberships/matches
    partitions : int, optional
        number of runs of Louvain in the Ensemble
    matching_threshold : float, optional
        controls when do two nodes belong to the same community. E.g. matching_threshold of 0.9
        will place two nodes in the same community if in 90% of the partitions they appear together
    Returns
    -------
    meta_network : networkx.Graph
       The metanetwork created by using the matching dictionary and the matching threshold
    """

    meta_network = nx.Graph()

    for node_pair, matching_score in matching_dict.items():
        if matching_score >= partitions * matching_threshold:
            tuple_node_pair = tuple(node_pair)
            node_1 = tuple_node_pair[0]
            node_2 = tuple_node_pair[1]
            meta_network.add_edge(node_1, node_2)

    for node in network.nodes():
        if not meta_network.has_node(node):
            meta_network.add_node(node)

    return meta_network

def _calculate_matching_scores(network, weight, partitions, resolution, cores=1):
    """Computes the matching scores required for the Ensemble Louvain
    Parameters
    ----------
    network : networkx.Graph
       the networkx graph which is decomposed
    weight : str, optional
        the key in graph to use as weight. Default to 'weight'
    partitions : int, optional
        number of runs of Louvain
    resolution :  double, optional
        Will change the size of the communities, default to 1.
        represents the time described in
        "Laplacian Dynamics and Multiscale Modular Structure in Networks",
        R. Lambiotte, J.-C. Delvenne, M. Barahona
    cores : int, optional
        number of cores on which Ensemble Louvain will execute
    Returns
    -------
    matching_dict : dictionary
       The matching dictionary, where key is a frozenset of nodes and
       value is the comemberships/matches
    """

    cpus = mp.cpu_count()
    if cpus < cores:
        cores = cpus
    elif cores < 1:
        cores = 1

    if cores == 1:
        matching_dict = _calculate(network, weight=weight, partitions=partitions, resolution=resolution)
        return matching_dict
    else:
        pool = mp.Pool(cores)
        partitions_per_cpu = partitions // (cores - 1)
        if partitions_per_cpu != 0:
            for run in range(cores - 1):
                pool.apply_async(_calculate, args=(network, weight, partitions_per_cpu, resolution),
                                 callback=_collect_result)
        partitions_left = partitions % (cores - 1)
        if partitions_left != 0:
            pool.apply_async(_calculate, args=(network, weight, partitions_left, resolution),
                             callback=_collect_result)

        pool.close()
        pool.join()

        global results

        matching_dict = {}
        for matching_dict_small in results:
            for key, matching_score in matching_dict_small.items():
                matching_dict[key] = matching_dict.get(key, 0) + matching_score

        results = []
        return matching_dict

def _calculate(network, weight, partitions, resolution):
    matching_dict = {}
    for run in range(partitions):
        partition = louvain.best_partition(network, weight=weight, resolution=resolution, randomize=True)

        nodes = list(network.nodes())
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                node_i = nodes[i]
                node_j = nodes[j]

                if partition[node_i] == partition[node_j]:
                    node_pair = (node_i, node_j)
                    matching_dict[node_pair] = matching_dict.get(node_pair, 0) + 1

    return matching_dict

def _giant_component(network):
    """Returns the giant component of a network
    Parameters
    ----------
    network : networkx.Graph
       the networkx graph on which giant component extraction is applied
    """
    network_components = sorted(nx.connected_components(network), key=len, reverse=True)
    return network.subgraph(network_components[0])

def _collect_result(result):
    # global lock
    # lock.acquire()
    # global results
    results.append(result)
    # lock.release()