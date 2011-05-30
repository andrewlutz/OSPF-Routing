#! /usr/bin/env python

####################################################################################################
#			The report for this assignment is in 'SFWR 4C03 - Assignment 2 Report.pdf', in my SVN
#
#	Andrew Lutz
#	0664122
#	SFWR ENG 4C03 - Assignment 2
#	The following code is an implementation of the OSPF routing policy
#	routed.py
#	March 7, 2011
#
####################################################################################################


class daemon(object):

	KILL = False
	commands = ['add rt', 'add nt', 'del rt', 'del nt', 'con', 'tree', 'display']
	nodes = {}
	
	#********* The sets below were networks used in the testing phase. *********#
	
	nodes = {'rt1':{'rt6':5}, 'rt2':{'rt1':3, 'rt3':1, 'rt4':3}, 'rt3':{'rt1':3, 'rt8':2, 'rt4':2, 'rt5':3}, 'rt4':{'rt1':4, 'rt2':4},
	#		'rt5':{'rt9':4, 'rt2':2, 'rt6':2, 'rt4':3}, 'rt6':{'rt2':1, 'rt4':2}, 'rt7':{'rt2':1, 'rt3':3}, 'rt8':{'rt7':3, 'rt4':2},
	#		'rt9':{'rt1':7}}
	#nodes = {'rt1':{'rt2':10, 'rt4':5}, 'rt2':{'rt3':1, 'rt4':2}, 'rt3':{'rt5':4}, 'rt4':{'rt2':3, 'rt3':9, 'rt5':2}, 'rt5':{'rt1':7, 'rt3':6}}
	#nodes = {'rt1':{'rt2':10, 'rt3':5}, 'rt2':{'rt1':1, 'rt3':2}, 'rt3':{'rt1':4}}
	#nodes = {'rt3':{'nt8':6}, 'rt5':{'rt3':1}, 'nt8':{}, 'nt9':{}}
	
	def add_router(self,rt):
		node = 'rt' + str(rt)
		if node in self.nodes.keys(): #if the node exists as a main key in the dictionary
			print "ERROR: Router, ",node," already exists."	#error msg, cant add duplicate
			return
		print "Router,",node,"successfully added."			
		self.nodes[node] = {}	#adds router to nodes, no connections
	
	def add_network(self, nt):
		node = 'nt' + str(nt)
		if node in self.nodes.keys():
			print "ERROR: Network, ",node," already exists."
			return
		print "Network,",node,"successfully added."			
		self.nodes[node] = {}	#adds network to nodes, no connections
			
	def del_router(self, rt):
		node = 'rt' + str(rt)
		if node in self.nodes: #if the node exists as a main key in the dictionary
			del self.nodes[node]	#delete the main key
			for x in self.nodes:	#loop through remaining main keys in dict
				if node in self.nodes[x]:	#true if node exists as sub-node in main key 'x'
					del self.nodes[x][node]		#delete the sub key in 'x'
			print "Router, ",node,"successfully removed."
			return
		print "ERROR: Router, ",node," does not exist."

	
	def del_network(self, nt):
		node = 'nt' + str(nt)
		if node in self.nodes:
			del self.nodes[node]
			for x in self.nodes:
				if node in self.nodes[x]:
					del self.nodes[x][node]
			print "Network, ",node,"successfully removed."
			return
		print "ERROR: Network, ",node," does not exist."
				
	def con(self, cnx):
		
		#check that cnx[3], aka, connection cost is integer
		try:
			abs_val = (float(cnx[2]) - int(cnx[2]))
		except ValueError:
			print "ERROR: Edge cost must be an integer"
			return
		
		#check that argument list is length 3	
		if len(cnx) != 3:
			print "ERROR: Must enter 3 arguments"
			return
		#check that user is not connecting node to itself	
		elif cnx[0] == cnx[1]:
			print "ERROR: Cannot connect a node to itself"
			return
		#check that user is not connecting two networks
		elif cnx[0][:2] == "nt" and cnx[1][:2] == "nt":
			print "ERROR: Cannot connect two networks"
			return
		#check that both nodes exist in the network
		elif cnx[0] not in self.nodes:
			print "ERROR: " + cnx[0] + " does not exist in network"
			return	
		elif cnx[1] not in self.nodes:
			print "ERROR: " + cnx[1] + " does not exist in network"
			return
		#check that connection is integer type
		elif abs_val != 0:
			print "ERROR: Edge cost must be an integer"
			return
		#check that connection cost is >= 1
		elif int(cnx[2]) < 1:
			print "ERROR: Edge cost must be greater than or equal to 1"
			return

		self.nodes[cnx[0]][cnx[1]] = int(cnx[2])
		print "Connection from " + cnx[0] + " to " + cnx[1] + " made successfully"		
		return	
	

	def modified_Dijkstra(self, G, start):

		G = self.nodes	#holds the link-list table
		final_dist = self.nodes.fromkeys(self.nodes)	#dict of final distances
		final_rout = [0]*len(G.keys())	#array of final routes
		keys = G.keys()	#list holding keys from node dictionary
		uS = {}	#dict of unvisited nodes
		
		#This method sets all final distances to -1, in real life they are set to infinity, but we cant do that in python
		for x in final_dist:
			final_dist[x] = -1	#using -1 to represent infinity
		uS = self.nodes.fromkeys(self.nodes)
				
		final_dist[start] = 0 #set distance of source node to zero
		current = start #start at current node
		
		#this makes the final_rout array a 2d array, each node has its own array to store the shortest path
		i = 0
		while i < len(keys):
			final_rout[i] = []
			i += 1

		while uS != {}:		#while there are still unvisited nodes
			if final_dist[current] != -1:	#if node has not been relaxed
				indexC = keys.index(current)	#get index of current node
				for y in G[current]:	#for each node attached to the node currently being relaxed
					index = keys.index(y)	#get index of adjacent node to current node currently being checked
					if final_dist[y] == -1: #if node has not been visited
						final_dist[y] = (final_dist[current] + G[current][y]) #update distance
						final_rout[index] = final_rout[indexC] + [current] #update route
 					elif (final_dist[current] + G[current][y]) < final_dist[y] and current != start:
						final_dist[y] = (final_dist[current] + G[current][y]) #update distance
						final_rout[index] = final_rout[indexC] + [current] #update route
			del uS[current] #delete current node from unvisited set once it has been relaxed
			
			#this method chooses the closest node to the current node, the closest
			#node will be relaxed next in accordance with Dijkstra Algorithm
			e_vert = [] #list will hold adjacent vertices
			for x in G:
				if x in uS and final_dist[x] > 0: #all unrelaxed nodes adjecent to current node
					e_vert.append(x)
			try:
				close_tuple = min([(final_dist[x],x) for x in e_vert])
			except ValueError:
				break
			current = close_tuple[1] #set new current node
		
		return (final_dist, final_rout, keys)
				
		
	def tree(self, node):
		if node[:2] == 'nt':
			print "ERROR: Cannot compute tree function for a network."
			return
		elif node == "":
			print "ERROR: Enter source node."
			return
		elif node not in self.nodes:
			print "ERROR: Router " + node + " does not exist in network"
			return
		
		D,R,keys = self.modified_Dijkstra(self.nodes, node)
		print
		
		i = 0
		while i < (len(R)):
			j = 0
			if D[keys[i]] == 0:
				pass	#if node is source node,do not print
			elif D[keys[i]] == -1:
				route = "  : no path to " + keys[i]
				print "\t", route
			else:	
				route = str(D[keys[i]]) + " : "
				while j < len(R[i]):
						route += (R[i][j]) + ", "
						j += 1
				route += keys[i]
				print "\t", route		
			
			i += 1	
		return

		
	def display(self):
		print
		keys = self.nodes.keys()	#store the keys from dictionary in a list for easier display
		top_row = "  "				
		row = [""] * len(keys)		#create array of rows for link-state database
		keys.sort()					#sorts the key list for easier reading
		i = 0
		while i < len(keys):
			top_row += "  " + keys[i]	#create string of all keys
			i += 1
		print top_row
		i = 0
		#The following loop creates the rows of the LSDB, and inserts the edge costs in the table
		while i < len(keys):	
			row[i] = keys[i]
			j = 0
			while j < len(keys):
				row[i] += "  "
				if keys[i] in self.nodes[keys[j]]:	#The following 4 lines provide padding depending on
													#the length of the connection(1 or 2 digits), this
													#helps keep the display table formatted and legible
					if len(str(self.nodes[keys[j]][keys[i]])) == 1:	
						row[i] += str(self.nodes[keys[j]][keys[i]]) + " "
					elif len(str(self.nodes[keys[j]][keys[i]])) == 2:
						row[i] += str(self.nodes[keys[j]][keys[i]]) + ""
				else:
					row[i] += "  "	
				row[i] += " "
				j += 1
			print row[i]
			i += 1	
		return
		
	#This method processes input when user wishes to input a range of nodes	
	def multNodes(self,nodes):
		index = nodes.find('-')
		i = 0
		num1 = ''
		num2 = ''
		while i < index:
			num1 += nodes[i]
			i += 1
		i = index + 1	
		while i < len(nodes):
			num2 += nodes[i]
			i += 1
			
		num1 = int(num1)
		num2 = int(num2)
		return range(num1,num2+1)
		
		
	#checks if command is acceptable, if so it returns a list of arguements
	def check_cmd(self, cmd):
		if cmd == "":
			return False
			
		elif cmd[0] == 'a':
			if cmd[:7] == 'add rt ':
				params = cmd[7:].split(',')
				return 'add rt', params
			
			elif cmd[:7] == 'add nt ':
				params = cmd[7:].split(',')
				return 'add nt', params
				
		elif cmd[0] == 'd':
			if cmd[:7] == 'del rt ':
				params = cmd[7:].split(',')
				return 'del rt', params
			
			elif cmd[:7] == 'del nt ':
				params = cmd[7:].split(',')
				return 'del nt', params
			
			elif cmd[:7] == 'display' and cmd[7:] == "":
				return 'display', []
			
		elif cmd[:4] == 'con ':
			params = cmd[4:].split(' ')
			return 'con', params
		
		elif cmd[:5] == 'tree ':
			params = cmd[5:]
			return 'tree', params
		
		elif cmd[:4] == 'quit' and cmd[4:] == "":
			return 'quit'

		return False		
			
			
	#This method 	
	def run(self):

		while self.KILL == False:
			u_input = raw_input("\nEnter a command...\n")
			c_in = self.check_cmd(u_input)	#this calls to check if input is valid, was cmd(cmd)
			if c_in == False:
				print "Command not recognized"
				continue
			elif c_in == 'quit':
				self.KILL = True	#stops the while loop(and the program)
			else:
				index = self.commands.index(str(c_in[0])) #takes index number of the command
				nodes = c_in[1]	#nodes are the second input parameter
				if nodes == ['']:
					print "No nodes entered"
					continue
			
				#parse the router list
				if index == 0:
					for x in nodes:
						if '-' in x:
							m_nodes = self.multNodes(x) #add a range of nodes
							for y in m_nodes: #m_nodes holds the returnes list of nodes from multNode, adds each node in list
								self.add_router(y)
						else:	
							self.add_router(x) #if no '-', add single node
				
				elif index == 1:
					for x in nodes:
						if '-' in x:
							m_nodes = self.multNodes(x)
							for y in m_nodes:
								self.add_network(y)
						else:	
							self.add_network(x)
				
				elif index == 2:
					for x in nodes:
						if '-' in x:
							m_nodes = self.multNodes(x)
							for y in m_nodes:
								self.del_router(y)
						else:	
							self.del_router(x)
				
				elif index == 3:
					for x in nodes:
						if '-' in x:
							m_nodes = self.multNodes(x)
							for y in m_nodes:
								self.del_network(y)
						else:	
							self.del_network(x)
						
				elif index == 4:			
					self.con(nodes)  # in con method makes sure the list of of length 3
					
				elif index == 5:
					self.tree(nodes)
				
				elif index == 6:
					self.display()
					
				else:
					print "Method index error!"
					
									
now = daemon()
now.run()