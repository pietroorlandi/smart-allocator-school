class ResourceAllocator:
    def __init__(self, schools_data: list):
        self._school_data = schools_data

    def calculate_best_allocation(self, budget: float):
        technologies = ['Broadband', 'Cellular']

        # Greedy
        connected_schools = []
        remaining_budget = budget

        # Sort schools by population density, isolation, and cost to prioritize the best candidates
        sorted_schools = sorted(self._school_data, key=lambda x: (x['pop_density'], -x['isolation'], min(x['costs'])), reverse=True)

        for school in sorted_schools:
            best_cost_idx = min(range(len(school['costs'])), key=school['costs'].__getitem__)
            cost = school['costs'][best_cost_idx]
            if cost <= remaining_budget:
                connected_schools.append({'school_id': school['school_id'], 'school_name': school['school_name'], 'technology': technologies[best_cost_idx], 'reason': school['reason'][best_cost_idx], 'cost': cost, 'pop_density': school['pop_density'], 'isolation': school['isolation']})
                remaining_budget -= cost

        connected_schools.append({'remaining_budget': remaining_budget})

        return connected_schools


# if(__name__ == '__main__'):
#     schools_data = [
#         {'id': 0, 'pop_density': 100, 'isolation': 0.8, 'costs': [500, 600], 'reason': ["", ""]},
#         {'id': 1, 'pop_density': 200, 'isolation': 0.5, 'costs': [600, 1200], 'reason': ["", ""]},
#         {'id': 2, 'pop_density': 150, 'isolation': 0.3, 'costs': [700, 1100], 'reason': ["", ""]},
#         {'id': 3, 'pop_density': 120, 'isolation': 0.7, 'costs': [550, 1400], 'reason': ["", ""]},
#         {'id': 4, 'pop_density': 180, 'isolation': 0.4, 'costs': [650, 100], 'reason': ["", "because il cellular"]},
#     ]
#     res_all = ResourceAllocator(schools_data=schools_data)
#     df = res_all.calculate_best_allocation(2000)
#     print(df)