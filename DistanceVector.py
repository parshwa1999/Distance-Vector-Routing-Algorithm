#import copy
import sys


def min_column(table, column_no):
	value_list = []
	for i in range(0,len(table)):
		if table[i][column_no] != None:
			value_list.append(table[i][column_no])
	if(len(value_list) == 0):
		#print(table)
		#print("HHEELLLL")
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
#			print("j =" +j+"  i="+str(i))
			j = j.split()
#			print(j)
			if(i == nodes[j[0]]):
#				print("i="+str(i)+"nodes="+str(nodes[j[0]]))
				routing_table_node[i][i][nodes[j[1]]] = int(j[2])
				print("t="+str(count)+" distance from "+ nodes[i] +" to "+j[1]+" via "+j[1]+" is "+str(j[2]))
#				print(routing_table_node)
			if(i == nodes[j[1]]):
#				print("i="+str(i)+"nodes="+str(nodes[j[1]]))
				routing_table_node[i][i][nodes[j[0]]] = int(j[2])
				print("t="+str(count)+" distance from "+ nodes[i] +" to "+j[0]+" via "+j[0]+" is "+str(j[2]))
#				print(routing_table_node)
			nodes[str(j[0])+str(j[1])]= int(j[2])
			nodes[str(j[1])+str(j[0])]= int(j[2])
		routing_table_node[i][i][i] = 0
	count += 1
	return routing_table_node, count, nodes
"""	for i in links:
		i = i.split()
		routing_table[nodes[i[0]]][nodes[i[1]]] = int(i[2]), i[1]
		routing_table[nodes[i[1]]][nodes[i[0]]] = int(i[2]), i[0]"""

def update_table(nodes, routing_table_node, count):
	print(" ")
	change = 0
	old_table = routing_table_node[:]
	for i in range(0, len(routing_table_node)):
		for j in range(0, len(routing_table_node[i])):
			if(routing_table_node[i][i][j] != None): #check neighbour
				for k in range(0, len(routing_table_node[i][j])):
					if(min_column(routing_table_node[j],j) != None and min_column(old_table[j],k) != None):

						if(k != i and i!=j
							and routing_table_node[i][j][k] !=
							 min_column(old_table[j],k) + nodes[nodes[i]+nodes[j]]):

							routing_table_node[i][j][k] = min_column(old_table[j],k) + nodes[nodes[i]+nodes[j]]#min_column(old_table[i],j)
							print("t="+str(count)+" distance from "+ nodes[i] +" to "+nodes[k]+" via "+nodes[j]+" is "+str(routing_table_node[i][j][k]))
							change = 1

						"""
						else(k != i
							and routing_table_node[i][j][k] !=
							 min_column(old_table[j],k) + min_column(old_table[i],j)):

							routing_table_node[i][j][k] = min_column(old_table[j],k) + min_column(old_table[i],j)
							print("t="+str(count)+" distance from "+ nodes[i] +" to "+nodes[k]+" via "+nodes[j]+" is "+str(routing_table_node[i][j][k]))
							change = 1"""
						if(k == i):
							routing_table_node[i][j][k] = 0
	#print(change)
	#print(routing_table_node)
	return change, routing_table_node

def print_routing_routes(nodes, routing_table_node):
	for i in range(0, len(routing_table_node)):
		for j in range(0, len(routing_table_node[i])):
			if(i!=j):
				#print(str(i) + str(j) + str(routing_table_node))
				print("router "+nodes[i]+": "+nodes[j]+" is "+str(min_column(routing_table_node[i], j))+" routing through "+ nodes[route_through(min_column(routing_table_node[i],j), routing_table_node[i], j, i)])
		print(" ")

def reinitialize_tables(nodes, routing_table_node, links, count):
	for i in range(0,len(routing_table_node)):
		#print(i)
		for j in links:
#			print("j =" +j+"  i="+str(i))
			j = j.split()
			if(len(j) != 3):
				#print("leng"+str(len(j)))
				continue
			#print(j)
			if(i == nodes[j[0]]):
#				print("i="+str(i)+"nodes="+str(nodes[j[0]]))
				routing_table_node[i][i][nodes[j[1]]] = int(j[2])
				print("t="+str(count)+" distance from "+ nodes[i] +" to "+j[1]+" via "+j[1]+" is "+str(j[2]))
#				print(routing_table_node)
			if(i == nodes[j[1]]):
#				print("i="+str(i)+"nodes="+str(nodes[j[1]]))
				routing_table_node[i][i][nodes[j[0]]] = int(j[2])
				print("t="+str(count)+" distance from "+ nodes[i] +" to "+j[0]+" via "+j[0]+" is "+str(j[2]))
#				print(routing_table_node)
			nodes[str(j[0])+str(j[1])]= int(j[2])
			nodes[str(j[1])+str(j[0])]= int(j[2])
	count += 1
	return routing_table_node, count, nodes


def changed_configuration(nodes, routing_table_node, changed_config):
	count = 0
	reinitialize_tables(nodes, routing_table_node, changed_config, count)

	count += 1
	change = 1
	while(change == 1):
		#print(routing_table_node)
		change, routing_table_node = update_table(nodes, routing_table_node, count)
		count += 1
	return routing_table_node




configL = open(str(sys.argv[1]), "r")
configuration = configL.read().split('\n')
configL.close()

changeConfigL = open(str(sys.argv[2]), "r")
changed_config = changeConfigL.read().split('\n')
changeConfigL.close()
#print(changeConfigL.read())

next_line_no=0
no_of_nodes = int(configuration[next_line_no])
next_line_no += 1

#node_list = []
nodes = {}
for i in range(0, no_of_nodes):
	nodes[configuration[next_line_no+i]] = i
	nodes[i] = configuration[next_line_no+i]
#print(nodes)
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
		
#	routing_table_node.append(routing_table.copy())

links = []
for i in range(0, no_of_links):
	links.append(configuration[next_line_no+i])

count = 0
routing_table_node, count, nodes = initialize_tables(nodes, routing_table_node, links, count)
#print(routing_table_node)

change = 1
while(change == 1):
	#print(routing_table_node)
	change, routing_table_node = update_table(nodes, routing_table_node, count)
	count += 1

print("\n#Initial \n")
print_routing_routes(nodes, routing_table_node)
#print(routing_table_node)

print("\n#UPDATE\n")
routing_table_node = changed_configuration(nodes, routing_table_node, changed_config[1:len(changed_config)])

print("\n#FINAL\n")
print_routing_routes(nodes, routing_table_node)
#print(nodes)