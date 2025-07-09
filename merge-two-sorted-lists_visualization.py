from manim import *

class MergeLinkedLists(Scene):
    def construct(self):
        list1_nodes = ["1", "2", "4"]
        list2_nodes = ["1", "3", "4"]
        
        list1_objs = self.create_linked_list(list1_nodes, BLUE, 3*LEFT + UP)
        list2_objs = self.create_linked_list(list2_nodes, GREEN, 3*RIGHT + UP)
        
        self.play(Create(list1_objs), Create(list2_objs))
        self.wait(1)
        
        dummy = self.create_node("", YELLOW).shift(UP*2 + 4*LEFT)
        dummy_label = Text("Dummy").scale(0.5).next_to(dummy, DOWN)
        self.play(Create(dummy), Write(dummy_label))
        
        tail_arrow = Arrow(dummy.get_right(), dummy.get_right() + RIGHT, color=RED)
        tail_text = Text("Tail").scale(0.5).next_to(tail_arrow, UP)
        self.play(Create(tail_arrow), Write(tail_text))
        
        merged_group = VGroup(dummy)
        current = dummy
        
        ptr1 = list1_objs[0]
        ptr2 = list2_objs[0]
        i, j = 0, 0
        
        while i < len(list1_nodes) and j < len(list2_nodes):
            node1 = list1_objs[i*2]
            node2 = list2_objs[j*2]
            self.play(Indicate(node1), Indicate(node2))
            
            if list1_nodes[i] <= list2_nodes[j]:
                selected = node1
                i += 1
            else:
                selected = node2
                j += 1
                
            selected_copy = selected.copy().set_color(WHITE)
            new_pos = current.get_center() + RIGHT*2
            selected_copy.move_to(new_pos)
            
            arrow = Arrow(current.get_right(), selected_copy.get_left(), buff=0.1)
            self.play(selected.animate.set_color(RED), run_time=0.5)
            self.play(
                Transform(selected.copy(), selected_copy),
                Create(arrow),
                run_time=1
            )
            self.play(selected.animate.set_color(BLUE if selected in list1_objs else GREEN), run_time=0.5)
            
            merged_group.add(arrow, selected_copy)
            current = selected_copy
            
            new_tail_arrow = Arrow(selected_copy.get_right(), selected_copy.get_right() + RIGHT, color=RED)
            self.play(
                Transform(tail_arrow, new_tail_arrow),
                tail_text.animate.next_to(new_tail_arrow, UP)
            )
            self.wait(0.5)
        
        remaining = list1_nodes[i:] if i < len(list1_nodes) else list2_nodes[j:]
        remaining_objs = list1_objs[i*2:] if i < len(list1_nodes) else list2_objs[j*2:]
        color = BLUE if i < len(list1_nodes) else GREEN
        
        for node in remaining_objs[::2]:
            node_copy = node.copy().set_color(WHITE)
            new_pos = current.get_center() + RIGHT*2
            node_copy.move_to(new_pos)
            
            arrow = Arrow(current.get_right(), node_copy.get_left(), buff=0.1)
            self.play(Indicate(node))
            self.play(node.animate.set_color(RED), run_time=0.5)
            self.play(
                Transform(node.copy(), node_copy),
                Create(arrow),
                run_time=1
            )
            self.play(node.animate.set_color(color), run_time=0.5)
            
            merged_group.add(arrow, node_copy)
            current = node_copy
            
            new_tail_arrow = Arrow(node_copy.get_right(), node_copy.get_right() + RIGHT, color=RED)
            self.play(
                Transform(tail_arrow, new_tail_arrow),
                tail_text.animate.next_to(new_tail_arrow, UP)
            )
            self.wait(0.5)
        
        merged_label = Text("Merged List", color=YELLOW).next_to(merged_group, UP, buff=1)
        self.play(Write(merged_label))
        self.wait(2)
    
    def create_node(self, text, color):
        node = Text(text).scale(0.8)
        circle = Circle(radius=0.5, color=color).surround(node)
        return VGroup(circle, node)
    
    def create_linked_list(self, values, color, start_pos):
        group = VGroup()
        prev = None
        for val in values:
            node = self.create_node(val, color)
            if prev:
                node.next_to(prev, RIGHT, buff=1.5)
            else:
                node.move_to(start_pos)
            group.add(node)
            if prev:
                arrow = Arrow(prev.get_right(), node.get_left(), buff=0.1)
                group.add(arrow)
            prev = node
        label = Text("List" if color == BLUE else "List 2", color=color).scale(0.6).next_to(node, DOWN)
        group.add(label)
        return group