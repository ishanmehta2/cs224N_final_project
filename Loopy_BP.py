import numpy as np
import string
from scipy.special import logsumexp
import random

class VariableNode:
    def __init__(self, position):
        self.position = position
        self.letters = list(string.ascii_uppercase)
        self.log_probs = np.log(np.full(len(self.letters), 1.0 / len(self.letters)))
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def receive_message(self, factor_node, message):
        self.log_probs += message

    def normalize(self):
        self.log_probs -= logsumexp(self.log_probs)

class FactorNode:
    def __init__(self, clue, length, candidates, confidence_ratings, bigram_probs):
        self.clue = clue
        self.length = length
        self.candidates = candidates
        self.confidence_ratings = confidence_ratings
        self.bigram_probs = bigram_probs
        self.neighbors = []
        self.messages = {}

    def add_neighbor(self, variable_node):
        self.neighbors.append(variable_node)
        self.messages[variable_node.position] = np.zeros(len(variable_node.letters))

    def send_message(self, variable_node, min_log_prob=-100):
        idx = self.neighbors.index(variable_node)
        other_vars = self.neighbors[:idx] + self.neighbors[idx + 1:]
        message = np.full(len(variable_node.letters), min_log_prob)  # Initialize with minimum log probability
        
        for candidate in self.candidates:
            candidate_indices = [string.ascii_uppercase.index(char) for char in candidate]
            candidate_log_prob = np.log(self.confidence_ratings[candidate])

            for other_var in other_vars:
                other_idx = self.neighbors.index(other_var)
                candidate_log_prob += other_var.log_probs[candidate_indices[other_idx]]

            # Incorporate bigram probabilities
            if idx > 0:  # Previous letter bigram
                prev_var = self.neighbors[idx - 1]
                prev_letter_idx = candidate_indices[idx - 1]
                prev_letter = prev_var.letters[prev_letter_idx].lower()
                curr_letter = candidate[idx].lower()
                if prev_letter in self.bigram_probs and curr_letter in self.bigram_probs[prev_letter]:
                    candidate_log_prob += np.log(max(self.bigram_probs[prev_letter][curr_letter], np.exp(min_log_prob)))

            if idx < self.length - 1:  # Next letter bigram
                next_var = self.neighbors[idx + 1]
                next_letter_idx = candidate_indices[idx + 1]
                next_letter = next_var.letters[next_letter_idx].lower()
                curr_letter = candidate[idx].lower()
                if curr_letter in self.bigram_probs and next_letter in self.bigram_probs[curr_letter]:
                    candidate_log_prob += np.log(max(self.bigram_probs[curr_letter][next_letter], np.exp(min_log_prob)))

            message[candidate_indices[idx]] = logsumexp([message[candidate_indices[idx]], candidate_log_prob])

        self.messages[variable_node.position] = message - logsumexp(message)
        variable_node.receive_message(self, self.messages[variable_node.position])


class CrosswordSolvingGrid:
    def __init__(self, variables, factors):
        self.variables = variables
        self.factors = factors

    def run_belief_propagation(self, num_iterations=10):
        for _ in range(num_iterations):
            factor_list = list(self.factors.values())
            random.shuffle(factor_list)
            for factor in factor_list:
                for neighbor in factor.neighbors:
                    factor.send_message(neighbor)

            variable_list = list(self.variables.values())
            random.shuffle(variable_list)
            for variable in variable_list:
                variable.normalize()

    def get_solution(self):
        solution = {}
        for position, variable in self.variables.items():
            best_letter = variable.letters[np.argmax(variable.log_probs)]
            solution[position] = best_letter
        return solution
