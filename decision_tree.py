TREE_NODE = 0

DECISION_NODE = 1
CATEGORICAL_NODE = 2
RANGE_NODE = 3


class TreeNode:
    def __init__(self):
        self.query = []
        self.children = []
        self.is_leaf = False
        self.type = TREE_NODE
        
    def addQueryLine(self, line):
        self.query.append(line)
         
    def addChild(self, node_child):
        self.children.append(node_child)
        node_child.father = self
        
    def getChild(self, pos):
        if pos >= len(self.children):
            return None
        else:
            return self.children[pos]
    
    def print(self):
        for l in self.query:
            print(l)
        print("É folha: " + str(self.is_leaf))
        print("")
        for child in self.children:
            if child != None:
                child.print()

class DecisionNode(TreeNode):
    def __init__(self, des):
        super().__init__()
        self.is_leaf = True
        self.description = des
        self.type = DECISION_NODE
    
    def print(self):
        print(self.description)
        print("")
        #super.print()

OPEN_INTERVAL = 0
CLOSED_INTERVAL = 1
UNBOUNDED_INTERVAL = 2

class Threshold:
    def __init__(self):
        self.interval = UNBOUNDED_INTERVAL
        self.value = 0

class RangeNode(TreeNode):
    def __init__(self, unit):
        super().__init__()
        self.thresholds = []
        self.intervals = []
        self.unit = unit
        self.type = RANGE_NODE
        
    def addChild(self, node, threshold):
        self.thresholds.append(threshold)
        self.children.append(node)
        
    def getChild(self, value):
        for th, i in zip(self.thresholds, range(len(self.children))):
            
            if th.interval == CLOSED_INTERVAL:
                if value <= th.value:
                    return self.children[i]
            elif th.interval == OPEN_INTERVAL:
                if value < th.value:
                    return self.children[i]
            
        return self.children[-1]

class Category:
    def __init__(self, description):
        self.description = description
        self.id_node = -1

class CategoricalNode(TreeNode):
    def __init__(self):
        super().__init__()
        self.categories = []
        self.type = CATEGORICAL_NODE
    
    def addChild(self, category, node):
        self.categories.append(category)
        self.children.append(node)
        category.id_node = len(self.children) - 1
        
    def getChild(self, category):
        return self.children[category.id_node]