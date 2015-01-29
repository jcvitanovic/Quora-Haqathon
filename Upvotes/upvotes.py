def get2pot(n):
	""" ... """
	p = 1
	while (p < n):
		p *= 2
	return p
def sum_of_n(n):
	return (n * (n+1) / 2)

def check_combine(type, left, right):
	if type:
		#non decreasing
		return left <= right
	else:
		#non increasing
		return left >= right

class Node:
	"""..."""
	def __init__(self, value = None, index = None):
		self.sum = 0 #the thing we will query
		self.hi = index #index interval start
		self.lo = index #index interval end
		self.first = value  #maybe redundant, because I already have indicies?
		self.last = value # same as up?
		self.firstLen = 1 
		self.lastLen = 1

	def __repr__(self):
		return "sum: %s | lo: %s, hi: %s, first: %s, last: %s, firstLen: %s, lastLen: %s" % (self.sum,
																							 self.lo,
																							 self.hi,
																							 self.first,
																							 self.last,
																							 self.firstLen,
																							 self.lastLen)

def combine_nodes(leftChild, rightChild, type):
	parent = Node()
	if leftChild is None:
		return rightChild
	if rightChild is None:
		return leftChild

	parent.lo = leftChild.lo
	parent.hi = rightChild.hi
	parent.first = leftChild.first
	parent.last = rightChild.last

	if check_combine(type, leftChild.last, rightChild.first):
		#combine
		len_combined = leftChild.lastLen + rightChild.firstLen
		parent.sum = sum_of_n (len_combined - 1) - sum_of_n(leftChild.lastLen - 1) - sum_of_n(rightChild.firstLen - 1)
		parent.sum += leftChild.sum + rightChild.sum
		if(leftChild.firstLen == leftChild.hi - leftChild.lo + 1):
			parent.firstLen = len_combined
		else:
			parent.firstLen = leftChild.firstLen

		if(rightChild.lastLen == rightChild.hi - rightChild.lo + 1):
			parent.lastLen = len_combined
		else:
			parent.lastLen = rightChild.lastLen
	else:
		parent.sum = leftChild.sum + rightChild.sum
		parent.firstLen = leftChild.firstLen
		parent.lastLen = rightChild.lastLen
	return parent


class TournamentTree:
	""" ... """	

	def __initParents(self, left, right):
		if left == 1:
			return #its a root, already set
		#to do: handle null children (padd)
		for i in range(left, right, 2):
			#set parents
			leftChild = self.array[i]
			rightChild = self.array[i+1]
			
			self.array[i // 2] = combine_nodes(leftChild, rightChild, self.type)

		self.__initParents(left - (right-left) / 2, left)
	

	def __init__(self, input, t):
		self.offset = get2pot(len(input))
		self.array = []
		self.dataLen = len(input)
		for i in range(len(input)):
			self.array.append(Node(input[i], i))
		arr_tmp = []
		for i in range(0, self.offset):
			arr_tmp.append(Node())
		self.array = arr_tmp + self.array
		self.array = self.array + [None] * (self.offset - len(input))
		self.type = t #true if non decreasing type, false if non increasing type
		self.__initParents(len(self.array) - self.offset, len(self.array))
	
	def query(self,i,lo, hi):
		node = self.array[i]
		print "checking interval: %s %s with node interval %s %s" % (lo, hi, node.lo, node.hi)		
		if(lo <= node.lo and hi >= node.hi):
			return node
		elif(node.hi < lo or node.lo > hi):
			return None
		else:
			return combine_nodes(self.query(2*i, lo, hi), self.query(2*i+1, lo, hi), self.type)

	def query_tree(self,lo, hi):
		result_node = self.query(1,lo, hi)
		return result_node.sum

def compute(tree1, tree2, n, k, input):
	iterations = n - k + 1
	for i in range(iterations):
		print input[i:i+k]
		q1 = tree1.query_tree(i,i+k-1)
		print ("*****************************")
		q2 = tree2.query_tree(i,i+k-1)
		print "non decreasing: %s, non increasing: %s" % (q1, q2)

if __name__== "__main__":
	input = [1, 2, 3, 1, 1]
	tree1 = TournamentTree(input, True)
	tree2 = TournamentTree(input, False)
	print "after init:"
	for node in tree1.array:
		print node
	print "---------------"
	for node in tree2.array:
		print node
	print "-----------------------------------------------"
	compute(tree1, tree2, len(input), 3, input)

