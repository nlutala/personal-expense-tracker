"""
Helper functions to be used to help derive constants
"""
import os


def get_root_path():
    """
    Get the root path of the project.
        :return: Root path (string)
    """
    current_path = os.path.dirname(__file__)
    return os.path.split(current_path)[0]
