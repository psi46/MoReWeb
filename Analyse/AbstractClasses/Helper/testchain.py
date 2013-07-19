class test_chain:
    def __init__(self, test, parent):
        self.test_str = test
        self.parent = parent
        self.children = []
    def next(self):
        if len(self.children) > 0:
            return self.children[0]
        elif self.parent:
            return self.parent.up_next(self)
        return None
    def up_next(self, child):
        if not child in self.children:
            return None
        found = False
        for c in self.children:
            if found:
                return c
            if c is child:
                found = True

        if self.parent:
            return self.parent.up_next(self)
        return None
    def __repr__(self):
        str = self.test_str
        if len(self.children) > 1:
            str += ">{"
            for i in range(len(self.children)):
                if i > 0:
                    str += ','
                str += `self.children[i]`
            str += "}"
        elif len(self.children) == 1:
            str += ">"
            str += `self.children[0]`
        return str
    def clone(self, new_parent):
        c = test_chain(self.test_str, new_parent)
        c.children = []
        for d in self.children:
            c.children.append(d.clone(c))
        return c
    def multiply(self, test_str_list):
        if len(test_str_list) < 1:
            return
        self.parent.multiply_child(self, test_str_list)
    def multiply_child(self, child, test_str_list):
        if len(test_str_list) < 1:
            return
        if not child in self.children:
            return False

        index = 0
        for i in range(len(self.children)):
            if self.children[i] is child:
                index = i
                break

        self.children[index].test_str = test_str_list[0]
        if len(test_str_list) < 2:
            return
        for i in range(1, len(test_str_list)):
            c = self.children[index].clone(self)
            c.test_str = test_str_list[i]
            self.children.insert(index + i, c)

# Context-free grammar used for parsing
# -------------------------------------
# testlist  := tree,tree,tree,...,tree
# tree      := chain[>bracket]
# chain     := test>test>test>...>test
# bracket   := {testlist}

parent = None

debug = False

def parse_test_list(test_list):
    global parent
    parent = test_chain("ROOT", None)
    parent_save = parent

    if _parse_test_list_2(test_list, 0, len(test_list)) >= 0:
        return parent_save

def _parse_test_list_2(test_list, pos, length):
    global parent
    save_parent = parent
    if debug: print "Call parse list:", pos, length
    new_pos = _parse_test_tree(test_list, pos, length)
    if debug: print "Return parse tree a", new_pos
    if new_pos >= 0:
        pos = new_pos
    else:
        return -1

    while new_pos >= 0:
        pos = new_pos
        parent = save_parent
        if new_pos < length and test_list[pos] == ',':
            new_pos += 1
        new_pos = _parse_test_tree(test_list, new_pos, length)
        if debug: print "Return parse tree b", new_pos

    return pos

def _parse_test_tree(test_tree, pos, length):
    if debug: print "Call parse tree:", pos, length
    new_pos = _parse_test_chain(test_tree, pos, length)
    if new_pos >= 0:
        pos = new_pos
    else:
        return -1

    if pos < length and test_tree[pos] == '>':
        new_pos += 1

    new_pos = _parse_test_bracket(test_tree, new_pos, length)
    if new_pos >= 0:
        pos = new_pos
    return pos

def _parse_test_chain(test_list, pos, length):
    if debug: print "Call _parse chain:", pos, length
    new_pos = _parse_test(test_list, pos, length)
    if new_pos >= 0:
        pos = new_pos
    else:
        return -1

    while new_pos >= 0:
        if debug: print pos
        pos = new_pos
        if pos < length and test_list[pos] == '>':
            new_pos += 1
        new_pos = _parse_test(test_list, new_pos, length)

    return pos

def _parse_test(test_tree, pos, length):
    global parent
    if debug: print "Call parse test:", pos, length
    new_pos = pos
    while new_pos < length:
        if not test_tree[new_pos] in ">{},":
            new_pos += 1
        else:
            break
    if pos == new_pos:
        return -1

    new_parent = test_chain(test_tree[pos:new_pos], parent)
    parent.children.append(new_parent)
    parent = new_parent

    return new_pos

def _parse_test_bracket(test_tree, pos, length):
    if debug: print "Call parse bracket:", pos, length
    if pos < length and test_tree[pos] == '{':
        pos += 1
    else:
        return -1

    new_pos = _parse_test_list_2(test_tree, pos, length)

    if new_pos >= 0:
        pos = new_pos

    if pos < length and test_tree[pos] == '}':
        pos += 1
    else:
        return -1
    return pos
