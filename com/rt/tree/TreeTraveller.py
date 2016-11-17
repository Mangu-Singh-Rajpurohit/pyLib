import functools

class TreeNodeMixin(object):

    NODE_TYPE_LEAF  = 0
    NODE_TYPE_PARENT= 1
    ID_FIELD        = "id"
    VALUE_LABEL     = "value"
    NAME_LABEL      = "nodeName"
    PARENT_LABEL    = "parent"
    CHILDREN_LABEL  = "children"
    TYPE_LABEL      = "type"

    __slots__       = [NAME_LABEL, PARENT_LABEL, CHILDREN_LABEL, TYPE_LABEL, VALUE_LABEL]
    path_seperator  = "/"

    def __init__(self, **dictArgs):
        if self.VALUE_LABEL not in dictArgs:
            dictArgs[self.VALUE_LABEL]  = dictArgs[self.NAME_LABEL]

        lsMissingAttrs  = filter(lambda x: x not in dictArgs and x, self.__slots__)
        if len(lsMissingAttrs) > 0:
            raise Exception("one of required attribute present in __slots__ is missing %s" %lsMissingAttrs)

        selfSetter = functools.partial(setattr, self)
        map(selfSetter, dictArgs.keys(), dictArgs.values())

    def __unicode__(self):
        objParent = self.get_parent()
        return "{}{}{}".format((objParent and objParent.path) or "", self.path_seperator, self.nodeName)

    def __str__(self):
        return self.__unicode__().encode("UTF-8")

    def get_parent(self):
        return self.parent

    def get_path_seperator(self):
        return self.path_seperator

    def get_id_field(self):
        return self.ID_FIELD

    @property
    def path(self):
        return self.__unicode__()

    """______________________________________________________________________"""

class FlatTreeNodeMixin(object):

    def __add__(self, objOtherNode):
        strIdField  = self.get_id_field()
        self.children.push(getattr(objOtherNode, strIdField))
        return self

    """______________________________________________________________________"""

class HiearchicalTreeNodeMixin(object):
    LEAF_NODE_LABEL     = "parent"
    PARENT_NODE_LABEL   = "leaf"
    TYPE_LABEL          = "type"

    def __add__(self, objOtherNode):
        strIdField  = self.get_id_field()
        idFieldVal  = getattr(objOtherNode, strIdField)
        strKeyToUse = None
        eNodeType   = getattr(objOtherNode, self.TYPE_LABEL)

        if eNodeType == self.NODE_TYPE_PARENT:
            strKeyToUse = self.get_parentnode_label()
        elif eNodeType == self.NODE_TYPE_LEAF:
            strKeyToUse = self.get_leafnode_label()
        else:
            raise Exception("Invalid node type")

        self.children.setdefault(strKeyToUse, {})[idFieldVal] = objOtherNode
        return self

    def get_leafnode_label(self):
        return self.LEAF_NODE_LABEL

    def get_parentnode_label(self):
        return self.PARENT_NODE_LABEL

    """______________________________________________________________________"""

class LeafTreeNodeMixin(TreeNodeMixin):

    def __init__(self, **dictArgs):
        dictArgs["type"]        = TreeNodeMixin.NODE_TYPE_LEAF
        dictArgs["children"]    = []
        super(LeafTreeNodeMixin, self).__init__(**dictArgs)

    """______________________________________________________________________"""

class ParentTreeNodeMixin(TreeNodeMixin):
    def __init__(self, **dictArgs):
        dictArgs["type"]        = TreeNodeMixin.NODE_TYPE_LEAF
        dictArgs["children"]    = []
        super(LeafTreeNodeMixin, self).__init__(**dictArgs)

    """______________________________________________________________________"""

class TreeNode(TreeNodeMixin):
    pass

    """______________________________________________________________________"""

class LeafNode(LeafTreeNodeMixin):
    pass

    """______________________________________________________________________"""

class ParentNode(ParentTreeNodeMixin):
    pass

    """______________________________________________________________________"""

class HiearchicalLeafTreeNode(LeafNode, HiearchicalTreeNodeMixin):
    pass

    """______________________________________________________________________"""

class FlatLeafTreeNode(LeafNode, FlatTreeNodeMixin):
    pass

    """______________________________________________________________________"""

class HiearchicalParentTreeNode(LeafNode, HiearchicalTreeNodeMixin):
    pass

    """______________________________________________________________________"""

class FlatParentTreeNode(LeafNode, FlatTreeNodeMixin):
    pass

    """______________________________________________________________________"""

###############################################################################
##  Tree view starts
###############################################################################

class CurrentNodeWrapper(object):

    def __init__(self):
        self._currentNode = None

    def __get__(self, instance, ownerClass):
        return self._currentNode

    def __set__(self, instance, value):
        self._currentNode   = value

class Tree(dict):

    ROOT_LABEL      = "ROOT"
    CUR_NODE_LABEL  = "currentNode"

    @property
    def root(self):
        return self[self.ROOT_LABEL]

    @root.setter
    def root(self, objNode):
        self[self.get_root_label()] = objNode

    def __setitem__(self, key, val):
        if key == self.get_root_label():
            if type(val) != TreeNodeMixin:
                raise Exception("Invalid Root set")

        super(Tree, self).__setitem__(key, val)

    def get_root_label(self):
        return self.ROOT_LABEL

    def get_current_node_label(self):
        return self.CUR_NODE_LABEL

    """______________________________________________________________________"""

class FlatTree(Tree):
    pass

    """______________________________________________________________________"""

class HiearchicalTree(Tree):
    def __add__(self, objChildNode):
        pass

    """______________________________________________________________________"""

objNode = LeafNode(nodeName = "", parent = None, children = [1, 2, 3], value = "")
print objNode