from xml.etree import ElementTree as ET
import decision_tree as dt

class Parser_DecisionTree:
    def __init__(self, file_name):
        self.root = ET.parse(file_name).getroot()

    def create_tree(self):
        node = self.root[0]
        return self.create_node(node)

    def create_node(self, node):
        t = node.find('type')
        if (t == None):
            return None

        type = t.text
        if (type == "categorical"):
            return self.create_categorical(node)
        if (type == "interactive_range"):
            return self.create_range(node)
        if (type == "decision"):
            return self.create_decision(node)

        return None

    def create_categorical(self, node):
        cat_node = dt.CategoricalNode()
        query = node.find('query')
        for line in query:
            cat_node.addQueryLine(line.text)

        categories = node.find("categories")
        node_children = node.find("node_children")
        for cat, child in zip(categories, node_children):
            category = self.create_category(cat)
            node_child = self.create_node(child)
            cat_node.addChild(category, node_child)

        return cat_node

    def create_category(self, cat):
        desc = cat.find('description').text
        category = dt.Category(desc)
        return category

    def create_range(self, node):
        u = node.find('unit')
        if (u == None):
            unit = 'und.'
        else:
            unit = u.text
        rang_node = dt.RangeNode(unit)

        if node.find('query'):
            query = node.find('query')
            for line in query:
                rang_node.addQueryLine(line.text)

        thresholds = node.find("thresholds")
        node_children = node.find("node_children")
        for th, child in zip(thresholds, node_children):
            threshold = self.create_threshold(th)
            node_child = self.create_node(child)
            rang_node.addChild(node_child, threshold)

        return rang_node

    def create_threshold(self, th):
        threshold = dt.Threshold()
        interval = th.find('interval').text
        if (interval == 'unbounded'):
            threshold.interval = dt.UNBOUNDED_INTERVAL
            threshold.value = float("inf")
        else:
            if (interval == 'open'):
                threshold.interval = dt.OPEN_INTERVAL
            else:
                threshold.interval = dt.CLOSED_INTERVAL
            threshold.value = float(th.find('upper_bound').text)
        return threshold

    def create_decision(self, node):
        desc = node.find('description')
        return dt.DecisionNode(desc)