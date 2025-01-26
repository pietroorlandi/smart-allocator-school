from unconnected_schools_extractor.unconnected_schools_extractor import UnconnectedSchoolsExtractor
from main import run_pipeline

def call_optimizer(country, budget, api_key):
    optimized_allocation_mk = run_pipeline(chosen_country=country, budget=budget, api_key=api_key)
    return optimized_allocation_mk

