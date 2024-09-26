import time

class MinimaxWithAlphaBeta:
    def __init__(self):
        self.nodes_visited = 0

    def minimax(self, depth, node_index, maximizing_player, values, alpha, beta):
        self.nodes_visited += 1

        if depth == 3:
            return values[node_index]

        if maximizing_player:
            max_eval = float('-inf')
            for i in range(2):
                eval = self.minimax(depth + 1, node_index * 2 + i, False, values, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(2):
                eval = self.minimax(depth + 1, node_index * 2 + i, True, values, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

values = [7, 5, 6, 9, 2, 4, 3, 1]

minimax_ab = MinimaxWithAlphaBeta()

start_time = time.perf_counter()

optimal_value = minimax_ab.minimax(0, 0, True, values, float('-inf'), float('inf'))

end_time = time.perf_counter()

print(f"Optimal Value: {optimal_value}")
print(f"Time taken: {end_time - start_time:.10f} seconds")
print(f"Number of nodes visited: {minimax_ab.nodes_visited}")
