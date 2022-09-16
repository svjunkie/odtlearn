from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from gurobipy import Model


class ProblemFormulation(ABC):
    def __init__(
        self, X, y, tree, X_col_labels, model_name, time_limit, num_threads, verbose
    ) -> None:
        """
        :param X: numpy matrix of covariates
        :param y: numpy array of class labels
        :param tree: Tree object
        :param _lambda: The regularization parameter in the objective
        :param model_name: str name of Gurobi model
        :param time_limit: The given time limit for solving the MIP
        :param verbose: Display Gurobi model output
        """
        self.X = pd.DataFrame(X, columns=X_col_labels)
        self.y = y
        self.X_col_labels = X_col_labels

        # datapoints contains the indicies of our training data
        self.datapoints = np.arange(0, self.X.shape[0])

        self.tree = tree
        self.time_limit = time_limit
        self.model_name = model_name
        # Gurobi model
        self.model = Model(self.model_name)
        if not verbose:
            # supress all logging
            self.model.params.OutputFlag = 0
        if num_threads is not None:
            self.model.params.Threads = num_threads
        self.model.params.TimeLimit = time_limit

    @abstractmethod
    def define_variables(self):
        pass

    @abstractmethod
    def define_constraints(self):
        pass

    @abstractmethod
    def define_objective(self):
        pass

    def create_main_problem(self):
        """
        This function creates and return a gurobi model based on the
        variables, constraints, and objective defined within a subclass
        """
        self.define_variables()
        self.define_constraints()
        self.define_objective()
        self.define_params()
