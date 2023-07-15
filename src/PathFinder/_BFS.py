class BFS:
    def __init__(self, choose_house):
        graph = {
            0: [1],
            1: [0, 2, 3, 4],
            2: [1],
            3: [1],
            4: [1, 5],
            5: [4, 6],
            6: [5, 7, 15],
            7: [6, 8],
            8: [7, 9],
            9: [8, 10],
            10: [9, 11],
            11: [10, 12, 13, 14],
            12: [11],
            13: [11],
            14: [11],
            15: [6, 16, 17],
            16: [15, 21],
            17: [15, 18, 19],
            18: [17],
            19: [17, 20],
            20: [19],
            21: [16]
        }
        self._coords_by_node = {
            0: (217, 162), # bed1
            1: (245, 162),
            2: (259, 132), # bathtub
            3: (292, 131), # toilet
            4: (251, 217), # door house1
            5: (251, 256),
            6: (184, 256),
            7: (184, 285),
            8: (144, 285),
            9: (144, 332),
            10: (82, 332), # house2
            11: (84, 262),
            12: (48, 263), # bed2
            13: (91, 232), # bathub2
            14: (122, 237), # toilet2
            15: (188, 216),
            16: (54, 216),
            17: (190, 112),
            18: (189, 75), # hospital
            19: (121, 111),
            20: (121, 75), # restaurant
            21: (56, 190), # work
        }
        self._survivor_house = choose_house
        self.graph = graph

    def get_node_by_necessity(self, node_name: str) -> int:
        if node_name == 'hunger':
            return 20
        if node_name == 'health':
            return 18
        if node_name == 'energy':
            return 0 if self._survivor_house == 4 else 12
        if node_name == 'hygiene':
            return 2 if self._survivor_house == 4 else 13
        if node_name == 'bladder':
            return 3 if self._survivor_house == 4 else 14
        if node_name == 'nothing':
            return 21

    def get_coord_node(self, node: int) -> tuple:
        return self._coords_by_node.get(node)

    def shortest_path(self, node1: int, node2: int) -> list:
        path_list = [[node1]]
        path_index = 0
        # To keep track of previously visited nodes
        previous_nodes = {node1}
        if node1 == node2:
            return path_list[0]

        while path_index < len(path_list):
            current_path = path_list[path_index]
            last_node = current_path[-1]
            next_nodes = self.graph[last_node]
            # Search goal node
            if node2 in next_nodes:
                current_path.append(node2)
                return current_path
            # Add new paths
            for next_node in next_nodes:
                if not next_node in previous_nodes:
                    new_path = current_path[:]
                    new_path.append(next_node)
                    path_list.append(new_path)
                    # To avoid backtracking
                    previous_nodes.add(next_node)
            # Continue to next path in list
            path_index += 1
        # No path is found
        return []