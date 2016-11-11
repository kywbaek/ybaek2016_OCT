#!/usr/bin/env python

import sys, copy

# function for creating graph with "1st degree network"
def get_first_degree_graph(batch_data):
    graph1 = {}
    
    # assign variables for each line
    for line in batch_data[1:]:
        
        time, id1, id2, amount, message = line.split(',',4) # some messages contain commas
            
        # update graph for each cases
        if id1 not in graph1:
            graph1[id1] = [id2]
            if id2 not in graph1:         # (both id1 and id2 not in graph)
                graph1[id2] = [id1]
            else:                         # (id2 in graph but not id1)
                graph1[id2].append(id1) 
        elif id2 not in graph1:           # (id1 in graph but not id2)
            graph1[id1].append(id2)
            graph1[id2] = [id1]
    
    return graph1


# function for creating a graph with "2nd degree network"
def get_second_degree_graph(graph1):
    graph2 = copy.deepcopy(graph1)       # using deepcopy instead of shallow copy
    for id1 in graph1:                   # iterate each user for additional degree network
        for id2 in graph1[id1]:
            for id2A in graph1[id2]:
                if (id2A not in graph1[id1]) and (id2A != id1):
                    graph2[id1].append(id2A)
    return graph2


# function for creating a graph with one level higher "degree network"
# compare current graph with the previous graph( with one degree lower ) to get lately added users
# for those users, look for additional degree network on the graph with "1st degree network"
def add_degree_to_graph(graph1,pre_graph,cur_graph):
    new_graph = copy.deepcopy(cur_graph)
    for id1 in cur_graph:
        if len(pre_graph[id1]) < len(cur_graph[id1]):
            for id2 in [id for id in cur_graph[id1] if id not in pre_graph[id1]]:
                for id2A in graph1[id2]:
                    if (id2A not in cur_graph[id1]) and (id2A != id1):
                        new_graph[id1].append(id2A)
    return new_graph


# function for getting all necessary graphs 
def get_graphs_for_all_features(batch_data):
    graph1 = get_first_degree_graph(batch_data)
    graph2 = get_second_degree_graph(graph1)
    graph3 = add_degree_to_graph(graph1,graph1,graph2)
    graph4 = add_degree_to_graph(graph1,graph2,graph3)
    return [graph1, graph2, graph4]


# function for creating "check list" for input data with graph
def get_check_list(stream_data,graph):
    check_list = []
    
    for line in stream_data[1:]:
        
        time, id1, id2, amount, message = line.split(',',4)
        if (id1 in graph) and (id2 in graph[id1]):
            check_list.append('trusted')
        else: check_list.append('unverified')

    return check_list

# use sys.argv to get the input/output paths
# get check lists and outputs them into text files.
def main():

    batch_file, stream_file = sys.argv[1:3]

    with open(batch_file, 'r') as b_f:
        batch_data  = b_f.read().split('\n')
        del batch_data[-1]
    with open(stream_file, 'r') as s_f:
        stream_data = s_f.read().split('\n')
        del stream_data[-1]

    graphs = get_graphs_for_all_features(batch_data)    

    for i in range(3):
        out_text_list = get_check_list(stream_data,graphs[i])
        out_text = '\n'.join(out_text_list) + '\n'
        with open(sys.argv[i+3], 'w+') as out_f:
            out_f.write(out_text)
        
if __name__ == "__main__":

    main()
