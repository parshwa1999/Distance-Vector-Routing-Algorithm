import copy
import sys


def min_column(table, column_no):
	value_list = []
	for i in range(0,len(table)):
		if table[i][column_no] != None:
			value_list.append(table[i][column_no])
	if(len(value_list) == 0):
		return None
	else:
		return min(value_list)

def route_through(value, table, column_no, node_no):
	for i in range(0, len(table)):
		if(node_no != i):
			if table[i][column_no] == value:
				return i

def initialize_tables(nodes, routing_table_node, links, count):
	for i in range(0,len(routing_table_node)):
		for j in links:
			j = j.split()
			if(i == nodes[j[0]]):
				routing_table_node[i][i][nodes[j[1]]] = int(j[2])
				print("t="+str(count)+" distance from "+ nodes[i] +" to "+j[1]+" via "+j[1]+" is "+str(j[2]))
			if(i == nodes[j[1]]):
				routing_table_node[i][i][nodes[j[0]]] = int(j[2])
				print("t="+str(count)+" distance from "+ nodes[i] +" to "+j[0]+" via "+j[0]+" is "+str(j[2]))
			nodes[str(j[0])+str(j[1])]= int(j[2])
			nodes[str(j[1])+str(j[0])]= int(j[2])
		routing_table_node[i][i][i] = 0
	count += 1
	return routing_table_node, count, nodes

def update_table(nodes, routing_table_node, count):
	print(" ")
	change = 0
	old_table = copy.deepcopy(routing_table_node)
	for i in range(0, len(routing_table_node)):
		for j in range(0, len(routing_table_node[i])):
			if(routing_table_node[i][i][j] != None): #check neighbour
				for k in range(0, len(routing_table_node[i][j])):
					if(min_column(routing_table_node[j],j) != None and min_column(old_table[j],k) != None):

						if(k != i and i!=j
							and routing_table_node[i][j][k] !=
							 min_column(old_table[j],k) + nodes[nodes[i]+nodes[j]]):

							routing_table_node[i][j][k] = min_column(old_table[j],k) + nodes[nodes[i]+nodes[j]]#min_column(old_table[i],j)							
							if(min_column(old_table[i],j) != min_column(old_table[j],k) + nodes[nodes[i]+nodes[j]] and j != k):
								print("t="+str(count)+" distance from "+ nodes[i] +" to "+nodes[k]+" via "+nodes[j]+" is "+str(routing_table_node[i][j][k]))
							change = 1

						if(k == i):
							routing_table_node[i][j][k] = 0

	return change, routing_table_node

def print_routing_routes(nodes, routing_table_node):
	for i in range(0, len(routing_table_node)):
		for j in range(0, len(routing_table_node[i])):
			if(i!=j):
				print("router "+nodes[i]+": "+nodes[j]+" is "+str(min_column(routing_table_node[i], j))+" routing through "+ nodes[route_through(min_column(routing_table_node[i],j), routing_table_node[i], j, i)])
		print(" ")

def poison_reverse(nodes, routing_table_node):
	for i in range(0, len(routing_table_node)):
		for k in range(0, len(routing_table_node[i][i])):
			if(routing_table_node[i][i][k] != min_column(routing_table_node[i], k)):
				routing_table_node[i][i][k] = None
	return routing_table_node

def reinitialize_tables(nodes, routing_table_node, links, count):
	for i in range(0,len(routing_table_node)):
		for j in links:
			j = j.split()
			if(len(j) != 3):
				continue
			if(i == nodes[j[0]]):
				routing_table_node[i][i][nodes[j[1]]] = int(j[2])
				print("t="+str(count)+" distance from "+ nodes[i] +" to "+j[1]+" via "+j[1]+" is "+str(j[2]))
			if(i == nodes[j[1]]):
				routing_table_node[i][i][nodes[j[0]]] = int(j[2])
				print("t="+str(count)+" distance from "+ nodes[i] +" to "+j[0]+" via "+j[0]+" is "+str(j[2]))
			nodes[str(j[0])+str(j[1])]= int(j[2])
			nodes[str(j[1])+str(j[0])]= int(j[2])
	count += 1
	return routing_table_node, count, nodes


def changed_configuration(nodes, routing_table_node, changed_config):
	count = 0
	routing_table_node, count, nodes = reinitialize_tables(nodes, routing_table_node, changed_config, count)

	change = 1
	while(change == 1):
		change, routing_table_node = update_table(nodes, routing_table_node, count)
		count += 1
	return routing_table_node




configL = open(str(sys.argv[1]), "r")
configuration = configL.read().split('\n')
configL.close()

changeConfigL = open(str(sys.argv[2]), "r")
changed_config = changeConfigL.read().split('\n')
changeConfigL.close()

next_line_no=0
no_of_nodes = int(configuration[next_line_no])
next_line_no += 1

nodes = {}
for i in range(0, no_of_nodes):
	nodes[configuration[next_line_no+i]] = i
	nodes[i] = configuration[next_line_no+i]

print("\n#START\n")

next_line_no += no_of_nodes

no_of_links = int(configuration[next_line_no])
next_line_no += 1


routing_table_node = []
for i in range(0,no_of_nodes):
	routing_table_node.append([])
	for j in range(0,no_of_nodes):
		routing_table_node[i].append([])
		for k in range(0,no_of_nodes):
			routing_table_node[i][j].append(None)
		

links = []
for i in range(0, no_of_links):
	links.append(configuration[next_line_no+i])

count = 0
routing_table_node, count, nodes = initialize_tables(nodes, routing_table_node, links, count)

change = 1
while(change == 1):
	change, routing_table_node = update_table(nodes, routing_table_node, count)
	count += 1
print(routing_table_node)
routing_table_node = poison_reverse(nodes, routing_table_node)

print("\n#Initial \n")
print_routing_routes(nodes, routing_table_node)

print("\n#UPDATE\n")
routing_table_node = changed_configuration(nodes, routing_table_node, changed_config[1:len(changed_config)])
routing_table_node = poison_reverse(nodes, routing_table_node)

print("\n#FINAL\n")
print_routing_routes(nodes, routing_table_node)