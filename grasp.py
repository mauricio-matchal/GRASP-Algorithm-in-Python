import random
import math

def calculate_cost(route, distances):
    cost = 0
    for i in range(len(route) - 1):
        cost += distances[route[i]][route[i + 1]]
    cost += distances[route[-1]][route[0]]  
    return cost

def calculate_prize(route, prizes):
    return sum(prizes[city] for city in route)

def construct_solution(cities, distances, prizes, min_prize):
    solution = [0] 
    remaining_cities = set(cities)
    remaining_cities.remove(0)

    current_city = 0

    while calculate_prize(solution, prizes) < min_prize and remaining_cities:
        candidates = []
        for city in remaining_cities:
            cost = distances[current_city][city]
            benefit = prizes[city]
            ratio = benefit / cost if cost > 0 else float('inf')
            candidates.append((city, ratio))

        candidates.sort(key=lambda x: x[1], reverse=True)

        restricted_candidates = candidates[:max(1, len(candidates) // 3)]
        next_city = random.choice(restricted_candidates)[0]

        solution.append(next_city)
        remaining_cities.remove(next_city)
        current_city = next_city

    return solution

def local_search(solution, distances, prizes, min_prize):
    best_solution = solution
    best_cost = calculate_cost(solution, distances)

    improved = True
    while improved:
        improved = False
        for i in range(1, len(solution)):  # Mantém a cidade 0 fixa
            for j in range(i + 1, len(solution)):
                new_solution = solution[:]
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

                if calculate_prize(new_solution, prizes) >= min_prize:
                    new_cost = calculate_cost(new_solution, distances)
                    if new_cost < best_cost:
                        best_solution = new_solution
                        best_cost = new_cost
                        improved = True

        solution = best_solution

    return best_solution

def grasp(cities, distances, prizes, min_prize, max_iterations=50):
    best_solution = None
    best_cost = float('inf')

    for _ in range(max_iterations):
        solution = construct_solution(cities, distances, prizes, min_prize)

        solution = local_search(solution, distances, prizes, min_prize)

        cost = calculate_cost(solution, distances)
        if cost < best_cost:
            best_solution = solution
            best_cost = cost

    return best_solution, best_cost

if __name__ == "__main__":
    cities = [0, 1, 2, 3, 4]
    distances = [
        [0, 15, 50, 20, 25],
        [15, 0, 35, 25, 15],
        [50, 35, 0, 30, 20],
        [20, 25, 30, 0, 15],
        [25, 15, 20, 15, 0]
    ]
    prizes = [0, 20, 10, 20, 25]
    min_prize = 75

    best_solution, best_cost = grasp(cities, distances, prizes, min_prize)
    print("Melhor solução:", best_solution)
    print("Custo da melhor solução:", best_cost)
