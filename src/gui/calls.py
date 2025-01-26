import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from main import run_pipeline


def call_optimizer(country, budget, api_key):
    optimized_allocation_mk = run_pipeline(chosen_country=country, budget=budget, api_key=api_key)
    return optimized_allocation_mk

