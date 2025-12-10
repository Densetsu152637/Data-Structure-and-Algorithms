"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from sorting import radix_sort_items

class IntHolder:
    def __init__(self, end = 0):
        self.__value = end
        
    def __eq__(self, other):
        return id(self) == id(other)
    
    def __str__(self) -> str:
        return str(self.value())
    
    def __repr__(self) -> str:
        return self
    
    def increment(self):
        self.__value += 1
        
    def value(self) -> int:
        return int(self.__value)
    
class Leaf:
    
    def __init__(self, index: int, node_id: IntHolder, start: int, end: IntHolder):
        self.node_id = node_id.value()
        node_id.increment()
        self.index = index
        self.__start = start
        self.__end = end
        self.parent: Node | None = None
        
    def __str__(self) -> str:
        return f"Node {self.node_id + 1}"
    
    def __repr__(self) -> str:
        return self
    
    def start(self):
        return self.__start
    
    def end(self) -> int:
        return self.__end.value()
    
    def range(self) -> int:
        return self.end() - self.start() 
    
    def clamp_start(self, new: int):
        self.__start = new
        
    def contains_child(self, char: str) -> bool:
        return False

class Node:
    """
    Represents node in a Suffix Tree
    """
    
    def __init__(self, node_id: IntHolder, start: int, end: int):
        self.node_id = node_id.value()
        node_id.increment()
        self.children: dict[str, NodeLeaf] = dict()
        self.suffix_link: Node | None = None
        self.parent: Node | None = None
        
        self.__start   = start
        self.__end     = end
        
    def __eq__(self, other):
        return id(self) == id(other)
    
    def __str__(self) -> str:
        return f"Node {self.node_id + 1}"
    
    def __repr__(self) -> str:
        return self
    
    def str_complex(self) -> str:
        link = f" (suffix link to {self.suffix_link})" if self.suffix_link != None else ""
        return f"Node {self.node_id + 1}{link}"
        
    def start(self) -> int:
        return self.__start
    
    def end(self) -> int:
        return self.__end
    
    def range(self) -> int:
        return self.end() - self.start() 
    
    def clamp_start(self, new: int):
        self.__start = new
    
     # child functions
    
    def set_child(self, other, char: str):
        self.children[char] = other
        other.parent = self
        
    def get_child(self, char: str):
        try:
            return self.children[char]
        except KeyError:
            return None
        
    def remove_child(self, char: str):
        if self.contains_child(char):
            old_node = self.children.pop(char)
            old_node.parent = None
        
    def contains_child(self, char: str) -> bool:
        return self.get_child(char) != None
    
    def get_ordered_children(self) -> list[tuple[str]]:
        # CONSTANT TIME
        # because we are soring a list of strings
        # with a guaranteed length of 1
        # and we have a constant bucket size due to 
        # string limitations :D
        items: list[list[str, NodeLeaf]] = []
        for char, node in self.children.items():
            items.append([char, node])
        return radix_sort_items(items)
        
        
class Root (Node):
    
    def __init__(self, node_id: IntHolder, start: int, end: int):
        Node.__init__(self, node_id, start, end)
        
NodeLeaf = Node | Leaf      
NodeLike = NodeLeaf | None
            
TAB = '\t'

class SuffixTree:
    """
    Suffix Tree class, which contains
    """
    
    def __init__(self, text: str = "", verbose = False, debug = False, method = print, debug_from: int = 0):
        # reset all variables if they have been initialised before
        self.text  = []
        
        # for logging
        self.verbose      = verbose
        self.debug        = debug
        self.debug_from   = debug_from
        self.print_method = method       
        
        # start phase 0 (initialisation of all variables)
        self.phase      = 0
        self.extension  = 1
        
        self.leaf_end   = IntHolder(0)
        self.id_manager = IntHolder(0)
        
        self.root = Root(
            self.id_manager, 
            0, 
            0
        )
        
        self._print_node_created(self.root, height = 0)
        self._log_end_phase()
        
        self.root.parent        = self.root
        self.root.suffix_link   = self.root
        
        self.active_node:  Node = self.root
        self.active_length: int = 0
        self.active_char:   int = 0
        self.remainder:     int = 0
        
        self.s: Node | None = None
        
        self._build(text)
        
    def __str__(self):
        newline = "\n"
        text_arr = self._print_node("Root", self.root, height = 0)
        text = newline.join(text_arr)
        return f"Suffix Tree of {self.word()}:{newline}{text}{newline}" 
        
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.text)

    # Private helper methods
    
    def should_debug(self):
        in_range = self.phase >= self.debug_from if self.debug_from >= 0 else self.phase <= abs(self.debug_from) 
        return self.debug and in_range
    
    def _debug(self, msg):
        return self._print_to_console(self.should_debug(), msg)
    
    def _log(self, msg):
        return self._print_to_console(self.verbose, msg)
        
    def _print_to_console(self, cond: bool, msg):
        if cond: self.print_method(msg)
        
    def _log_end_phase(self):
        self._log("") # just creates a new line
        
    def _print_node_created(self, node: NodeLeaf, height: int):
        # A helper method to visualse the suffix tree
        node_type = "Leaf" if isinstance(node, Leaf) else "Internal"
        self._log(f"{TAB * height}{node} created: {node_type} node!")
        
    def _print_linking(self, n1: Node, n2: Node, height):
        self._log(f"{TAB * height}Linking {n1} to {n2}")
        
    def _print_node(self, char: str, node: Node, height: int) -> list[str]:
        """Debug helper: print the edges."""
        node_text = self.word()[node.start() : node.end()]
        text = []
        text.append(
            f"{TAB * height}{char}: {node} ({node.__class__.__name__}) \"{node_text}\" [{node.start()}-{node.end()}] (sfx link to {node.suffix_link})"
        )
        # print children
        for k, v in node.children.items():
            if isinstance(v, Node):
                text.extend(self._print_node(k, v, height + 1))
            elif isinstance(v, Leaf):
                text.append(self._print_leaf(k, node, v, height + 1))
                
        return text
            
    def _print_leaf(self, char: str, node: Node, leaf: Leaf, height: int) -> str:
        leaf_text = self.word()[leaf.start() : leaf.end()]
        return f"{TAB * height}{char}: {leaf} (Leaf) \"{leaf_text}\" [{leaf.start()}-{leaf.end()}] ({leaf.index})"
        
    def _build(self, text: str):
        """
        Build suffix tree for full string using Ukkonens online algorithm
        Runs in O(N) time where N = len(text)
        """
        for char in text:
            self.add_char(char)
            # if self.should_debug(): self.pretty_print()
            
    # Methods able to be called
    def pretty_print(self) -> str:
        value = self.__str__()
        print(value)
        return value
            
    def recreate(self, text: str):
        self.__init__(
            text, 
            self.verbose, 
            self.debug,
            self.print_method
        )
    
    def word(self) -> str:
        return "".join(self.text)
    
    def _rule_2_alt(self, char, created: list) -> Node:
        self._log(f"\tExtn {self.extension} applies Rule 2 (alternative)")
        # Rule 2 alternative
        # create branching leaf node
        j, i = self.extension - 1, self.phase - 1
        new_leaf = Leaf(
            j,                
            self.id_manager,
            i,
            self.leaf_end
        )
        
        # add leaf to found node to append to
        self.active_node.set_child(new_leaf, char)
        
        created.append(new_leaf)    
        
        # t by definition is our found branch node with the new leaf
        # dangling from it for rule 2 alt
        t = self.active_node
        return t
    
    def _rule_2_reg(self, char, created: list, existing_index: int) -> Node:
        self._log(f"\tExtn {self.extension} applies Rule 2 (regular)")
        # Rule 2 regular
        # create one new internal node between the active node and the old node
        # create one new leaf to extend from the new intgernal node
        # the first node should have the original character and be internal
        j, i = self.extension - 1, self.phase - 1
        branch_char = self.text[self.active_char]
        branch_node = self.active_node.get_child(branch_char)
        
        existing_char = self.text[existing_index]
        
        new_internal = Node(
            self.id_manager, 
            branch_node.start(),
            existing_index     
        )
        
        # increase the branch node starting position to exclude
        # the jump between self.active -> new internal
        branch_node.clamp_start(existing_index)
        
        # the second node should start from the new character
        new_leaf = Leaf(
            j, 
            self.id_manager,  
            i,  
            self.leaf_end       
        )
        
        # integrate the two objects into the tree by adding them as children to the active node
        # set the new internal node as the proper child of the active node
        # should override the old entry for self.active_char
        self.active_node.remove_child(branch_char)
        self.active_node.set_child(new_internal, branch_char)
        
        # set the original branch_node as the child of the new internal node 
        # for the character originally found in that position within the substring
        new_internal.set_child(branch_node, existing_char)
        
        # set the new_leaf as another child of the new internal node
        new_internal.set_child(new_leaf, char)
        
        # for printing
        created.append(new_internal)   
        created.append(new_leaf)
        
        # t by definition is our new internal node
        t = new_internal
        return t

    # Ukkonnens algorithm (implemented online)
    def add_char(self, char: str):
        """
        Add character — one phase.
        """
        # is a string, we want to make this function online only
        if len(char) > 1:
            return self._build(char)
        
        # start by incrementing end (rapid leaf extension trick)
        # this actually completes Rule 1 section of the entire phase
        # incrementing phase as well
        # we know we have one more suffix to cover
        # we want to reset the active node to the node connected to the most recently created leaf node
        self.text.append(char)
        self.leaf_end.increment()
        self.phase     += 1
        self.remainder += 1

        self._log(f"Phase {self.phase} starts from Extn {self.extension}")
        
        # rule 2s
        # we want to repeat rule 2 until we exhaust all our suffix links
        # rule 2 reg -> reg | alt 
        # rule 2 alt -> reg | alt
        # we do not need to check whether self.active_node.suffix_link == self.active_node
        # as the algorithm correctness guarantees that self.extension > self.phase if we 
        # move from root -> root via a suffix link jump
        
        # we already start from root at the start of the phase
        # so we want to start looking at the characters from 
        # str[j...i]
        i = self.phase - 1
        
        while self.remainder > 0: 
            created = [] # for logging
            
            # initialise j and t
            j = self.extension - 1
            t: Node | None = None
            
            if self.active_length == 0: self.active_char = i 
                
            # check to see if we need to rule 2 alt
            branch_char = self.text[self.active_char]
            branch_node = self.active_node.get_child(branch_char)
            
            # these are variables which need to be correct for later in the extension
            rule_2_alt = branch_node == None
            rule_2_reg = False
            rule_3     = False
            
            # we know that our branch node cannot be none
            # if rule_2_alt is false
            # so this is just for variable keeping really
            existing_index = branch_node.start() + self.active_length if branch_node != None else -1
            existing_char  = self.text[existing_index] if existing_index != -1 else None
            
            if rule_2_alt:
                # perform a rule 2 alt  
                t = self._rule_2_alt(char, created)  
                
            else:
                # we know that branch_node != None here, so we can do a skip count
                # only unless we can progress further in the loop
                if (
                    isinstance(branch_node, Node)
                    and self.active_length >= branch_node.range()
                ):
                    # calculate skipped to increment pointer
                    skipped = branch_node.range()   
                    self.active_length -= skipped
                    
                    # self._debug(f"skipped {skipped} ({branch_node.start()}->{branch_node.end()}) from {self.active_node} to {branch_node}")
                    # self._debug(f"was able to find {branch_node} from searching \"{self.active_char}\" on {self.active_node}")
                    
                    # start looking for the next iteration 
                    self.active_node = branch_node
                    self.active_char = self.active_char + branch_node.range()
                    
                    continue # go back to the start of the loop and see if you should do a rule 2 alt 
                
                # we need to see if we need to perform a rule 2 reg or rule 3 now
                rule_2_reg = existing_char != char
                rule_3 = not rule_2_reg
                
                if rule_2_reg:
                    # we can do a rule 2 regular if the characters are conflicting
                    t = self._rule_2_reg(char, created, existing_index)
                    
                else:
                    # we can do a rule 3 here (which is doing nothing :D)
                    self._log(f"\tExtn {self.extension} applies Rule 3")
                    t = self.active_node
            
            p = self.active_char + 1
            # one of these should be true always
            # operation = "Rule 2 regular" if rule_2_reg else (
                        # "Rule 2 alt"     if rule_2_alt else 
                        # "Rule 3"         if rule_3 else "Undefined :/"
            # )
            # self._debug(f"self.text:        \"{self.word()}\"")
            # self._debug(f"inserting:        \"{self.word()[j : i + 1]}\" (str[{j}..{i + 1}])")
            # self._debug(f"found:            \"{self.word()[branch_node.start() : branch_node.end()]}\" (str[{branch_node.start()}..{branch_node.end()}])" if branch_node != None else "found:            None") 
            # self._debug(f"remainder:        \"{self.word()[p : i + 1]}\" (str[{p}..{i + 1}])")
            # self._debug(f"expended:         \"{self.word()[j : p]}\" (str[{j}..{p}])")
            # self._debug(f"j, i, p:          {j}, {i}, {p}")
            # self._debug(f"active_length:    {self.active_length}")
            # self._debug(f"e_x, str[e_x]:    {existing_index}, {existing_char} vs {char}")
            # self._debug(f"br_char, br_node: {branch_char}, {branch_node}")
            # self._debug(f"active_node:      {self.active_node}")
            # self._debug(f"operation:        {operation}")
            
            if not (rule_2_reg or rule_2_alt or rule_3):
                # this is mainly for debugging but we get to this point panik
                self._log(f"\tExtn {self.extension} failed to apply a rule...")
            
            # print our active node and remainder
            rem_str = f"S[{p}...{i}]" if p <= i  else "EMPTY"
            self._log(f"\tActive Node = {self.active_node}; Remainder = {rem_str}")
            
            # print newly created nodes
            for new_node in created:
                self._print_node_created(new_node, 2)
                
            # IMPORTANT create suffix link between s -> t 
            # if s != None, then we can link s -> t
            # we can then set t as s for the next iteration
            # we need to do this before our showstopper otherwise we void algorithmic correctness
            if self.s != None and t != None and self.s != t:
                should_print = self.s.suffix_link != t
                self.s.suffix_link = t
                # only print if this is a new suffix link
                if should_print: self._print_linking(self.s, t, 2)
                
            # we can always make s = t as we go for the next iteration
            # s will get automatically cleaned up if no next iteration happens
            # t will automatically be reassigned over the next iteration
            if t != None: self.s = t
            
            # show-stopper trick 
            if (rule_3): 
                self.active_length += 1
                self.s = None
                break            
            
            # we can increment the extension because we have to do the next suffix link extension
            # dont forget to increment p as well otherwise it will be out of date
            # this code will not run if the operation was a Rule 3
            # self._debug(f"skip decrementing from {skip} to {skip - print_node.range()}")
            self.extension += 1
            self.remainder -= 1
            
            # this branching logic must be done in order to preserve correctness
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_char = self.phase - self.remainder
                
            elif self.active_node.suffix_link:
                self.active_node = self.active_node.suffix_link
                
            else:
                self.active_node = self.root
            
            # if self.should_debug(): self.pretty_print()
        
        self._log_end_phase()
        
    
    # Search the suffix array in O(n) time
    def search(self, txt: str) -> tuple[Node, int]:
        # returns (node found, progress on search)
        if len(txt) == 0:
            return (self.root, 0)
        
        p = 0
        active = self.root
        
        while active != None and p < len(txt):
            p_start = p
            for i in range(active.start(), active.end()):
                if p > len(txt) or self.text[i] != txt[p]:
                    return (active, p)
                p += 1
            # we finished the search over this one
            # next node
            next_char = txt[p_start]
            active = active.get_child(next_char)
            
        return (active, p)
    
    def contains(self, txt: str) -> int:
        # Search the suffix array in O(n) time
        found_leaf, p = self.search(txt)
        if p != len(txt) or not isinstance(found_leaf, Leaf):
            return -1
        
        # we know here that node must 
        return found_leaf.index
            
    # Suffix Array in O(n) time 
    def suffix_array(self) -> list[int]:
        arr = []
        self._suffix_array_rec(self.root, arr)
        return arr
    
    def _suffix_array_rec(self, node: Node, arr: list[int]):
        # does a DFS on the children of the nodes
        # to append to the array in order
        for char, child in node.get_ordered_children():          
            child : NodeLeaf  
            if isinstance(child, Leaf):
                arr.append(child.index)
            elif isinstance(child, Node):
                self._suffix_array_rec(child, arr)
                
    def bwt_sa(self) -> tuple[str, list[int]]:
        # returns the (bwt, SA) in a tuple
        SA = self.suffix_array()
        get_index = lambda i: (i - 1 % len(self.text))
        return ("".join(map(lambda i: self.text[get_index(i)], SA)), SA)
    
    def bwt(self) -> str:
        return self.bwt_sa()[0]
    
