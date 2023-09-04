import random

# Knapsack problem parameters
knapsack_capacity = 100
num_items = 30


def is_pareto_optimal(solution):
    for tabu_solution in tabu_list:
        if all(
            solution[i] <= tabu_solution[i] for i in range(num_items)
        ) and any(
            solution[i] < tabu_solution[i] for i in range(num_items)
        ):
            return False
    return True

# TABU search parameters
num_iterations = 100
tabu_list_size = 3

# Initial solution (all items excluded)
current_solution = [0] * num_items

# Initialize TABU list
tabu_list = []

# Define weight factors for the scalarized objective function
w_value = 0.5 # Weight factor for maximizing total value
w_weight = 0.5

#Utopian Values
target_max_value = 30
target_max_weight = 0


def weighted_metric_objective(solution):
    total_value = sum(item['value'] * solution[i] for i, item in enumerate(items))
    total_weight = sum(item['weight'] * solution[i] for i, item in enumerate(items))
    
    max_value_deviation = abs(total_value - target_max_value) * w_value 
    max_weight_deviation = abs(total_weight - target_max_weight) * w_weight 
    
    
    if total_weight > knapsack_capacity:  # Penalize solutions that exceed capacity
        penalty = w_weight * (total_weight - knapsack_capacity)
    else:
        penalty = 0
        
    return max_value_deviation + max_weight_deviation
    
# Run the code 100 times and calculate the percentage of Pareto optimal solutions
num_runs = 100
pareto_optimal_count = 0


for run in range(num_runs):
    # Generate random items with values and weights
    items = [
        {
            'label': f'item{i+1}',
            'value': random.randint(1, 30),
            'weight': random.randint(1, 10)
        }
        for i in range(num_items)
    ]

    
    current_solution = [0] * num_items
    tabu_list = []
    
    


    # Main TABU search loop
    for _ in range(num_iterations):
        best_candidate = None
        best_candidate_value = -1
        
        # Generate neighbors of the current solution
        for i in range(num_items):
            neighbor = list(current_solution)
            neighbor[i] = 1 - neighbor[i]  # Toggle inclusion/exclusion of item
            neighbor_value = weighted_metric_objective(neighbor)
        
            # Calculate the total weight of the neighbor
            neighbor_weight = sum(item['weight'] * neighbor[i] for i, item in enumerate(items))
        
            # Check if the neighbor is feasible and has better value
            if neighbor_weight <= knapsack_capacity and neighbor_value > best_candidate_value and neighbor not in tabu_list:
                best_candidate = neighbor  # Assign the best candidate
                best_candidate_value = neighbor_value
        
        if best_candidate is not None:
            # Update current solution only if a valid best_candidate is found
            current_solution = best_candidate
        
            # Add the current solution to the TABU list
            tabu_list.append(current_solution)
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)
            #print(tabu_list)

    # Check if the current solution is Pareto optimal and increment the count
    if is_pareto_optimal(current_solution):
        pareto_optimal_count += 1

    # Print the status for each run
    print(f"Run {run + 1}: Pareto Optimal? {is_pareto_optimal(current_solution)}")

# Calculate and print the percentage of Pareto optimal solutions
percentage_pareto_optimal = (pareto_optimal_count / num_runs) * 100
print(f"\nPercentage of Pareto Optimal Solutions WSM: {percentage_pareto_optimal:.2f}%")


# Extract the selected items and their details
selected_items = [item for i, item in enumerate(items) if current_solution[i] == 1]
total_value = sum(item['value'] for item in selected_items)  
total_weight = sum(item['weight'] for item in selected_items)


'''
# Print the results
print("Selected Items:")
for i, item in enumerate(selected_items):
    print(f"{item['label']}, Value: {item['value']}, Weight: {item['weight']}")
print(f"Number of items selected: {len(selected_items)}")   
print(f"Total Value: {total_value}") 
print(f"Total Weight: {total_weight}")
print(f"Scalarized Objective Value: {scalarized_objective(current_solution)}")


# Check if the current solution is Pareto optimal
if is_pareto_optimal(current_solution):
    print("The current solution is Pareto optimal.")
else:
    print("The current solution is not Pareto optimal.")
    
'''


