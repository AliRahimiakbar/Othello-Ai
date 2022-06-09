import random
import copy
import sys

from player import Player


class AlphaBetaPlayer(Player):

    def get_next_move(self):
        res_coordinates = []
        res_count = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for i in range(self.board.get_n()):
            for j in range(self.board.get_n()):
                self.board.start_imagination()
                if self.board.is_imaginary_move_valid(self.player_number, i, j):
                    self.board.imagine_placing_piece(self.player_number, i, j)
                    count = self.get_next_move_min(alpha, beta, 2)
                    if count == res_count:
                        res_coordinates.append((i, j))
                    if count > res_count:
                        res_coordinates = [(i, j)]
                        res_count = count
        if len(res_coordinates) == 0:
            return None
        return random.choice(res_coordinates)

    def get_next_move_max(self, alpha, beta, max_size):
        res_count = float('-inf')
        x = copy.deepcopy(self.board.imaginary_board_grid)
        if max_size:
            for i in range(self.board.get_n()):
                for j in range(self.board.get_n()):
                    self.board.imaginary_board_grid = copy.deepcopy(x)
                    if self.board.is_imaginary_move_valid(self.player_number, i, j):
                        self.board.imagine_placing_piece(self.player_number, i, j)
                        res_count = max(res_count, self.get_next_move_min(alpha, beta, max_size - 1))
                        if res_count >= beta:
                            return res_count
                        alpha = max(res_count, alpha)
        self.board.imaginary_board_grid = copy.deepcopy(x)
        if res_count < -10000:
            return self.get_score()
        return res_count

    def get_next_move_min(self, alpha, beta, max_size):
        res_count = float('inf')
        x = copy.deepcopy(self.board.imaginary_board_grid)
        if max_size:
            for i in range(self.board.get_n()):
                for j in range(self.board.get_n()):
                    self.board.imaginary_board_grid = copy.deepcopy(x)
                    if self.board.is_imaginary_move_valid(self.opponent_number, i, j):
                        self.board.imagine_placing_piece(self.opponent_number, i, j)
                        res_count = min(res_count, self.get_next_move_max(alpha, beta, max_size - 1))
                        if res_count <= alpha:
                            return res_count
                        beta = max(res_count, alpha)
        self.board.imaginary_board_grid = copy.deepcopy(x)
        if res_count > 10000:
            return self.get_score()
        return res_count


    def get_score(self):
        scores = [0, 0]
        for row in self.board.imaginary_board_grid:
            for cell in row:
                if cell >= 0:
                    scores[cell] += 1
        return scores[self.player_number] - scores[self.opponent_number]
