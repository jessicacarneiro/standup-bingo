"""
Bingo card module for generating and managing bingo cards.

This module handles the core bingo card logic including generating
random cards from a list of entries.
"""

import random


def generate_bingo_card(entries, num_entries):
    """
    Generate a random bingo card from available entries.
    
    Args:
        entries (list): List of available entries
        num_entries (int): Number of entries to include on the card
        
    Returns:
        list: Randomly selected entries for the bingo card
        
    Raises:
        ValueError: If num_entries is greater than the number of available entries
    """
    return random.sample(entries, num_entries)
