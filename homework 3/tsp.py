import random
import operator
import pandas as pd
import numpy as np
from city import City
from fitness import Fitness


def create_route(cities):
    route = random.sample(cities, len(cities))
    return route


def initial_population(pop_size, city_list):
    pop = []

    for i in range(0, pop_size):
        pop.append(create_route(city_list))

    return pop


def rank_routes(pop):
    fitness_results = {}

    for i in range(0, len(pop)):
        fitness_results[i] = Fitness(pop[i]).route_fitness()

    return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)


def selection(pop_ranked, elite_size):
    selection_results = []
    df = pd.DataFrame(np.array(pop_ranked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, elite_size):
        selection_results.append(pop_ranked[i][0])

    for i in range(0, len(pop_ranked) - elite_size):
        pick = 100 * random.random()

        for i in range(0, len(pop_ranked)):
            if pick <= df.iat[i, 3]:
                selection_results.append(pop_ranked[i][0])
                break

    return selection_results


def create_mating_pool(pop, selection_results):
    mating_pool = []

    for i in range(0, len(selection_results)):
        index = selection_results[i]
        mating_pool.append(pop[index])

    return mating_pool


def breed(parent_1, parent_2):
    child = []
    parent_1_chromo = []
    parent_2_chromo = []

    gene_a = int(random.random() * len(parent_1))
    gene_b = int(random.random() * len(parent_1))

    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    for i in range(start_gene, end_gene):
        parent_1_chromo.append(parent_1[i])

    parent_2_chromo = [
        item for item in parent_2 if item not in parent_1_chromo]

    child = parent_1_chromo + parent_2_chromo
    return child


def breed_pop(mating_pool, elite_size):
    children = []
    length = len(mating_pool) - elite_size
    pool = random.sample(mating_pool, len(mating_pool))

    for i in range(0, elite_size):
        children.append(mating_pool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(mating_pool) - i - 1])
        children.append(child)

    return children


def mutate(individual, mutation_rate):
    for swapped in range(len(individual)):
        if(random.random() < mutation_rate):
            swap_with = int(random.random() * len(individual))

            city_1 = individual[swapped]
            city_2 = individual[swap_with]

            individual[swapped] = city_2
            individual[swap_with] = city_1

    return individual


def mutate_pop(pop, mutation_rate):
    mutated_pop = []

    for i in range(0, len(pop)):
        mutated_index = mutate(pop[i], mutation_rate)
        mutated_pop.append(mutated_index)

    return mutated_pop


def create_next_generation(current_gen, elite_size, mutation_rate):
    pop_ranked = rank_routes(current_gen)
    selection_results = selection(pop_ranked, elite_size)
    mating_pool = create_mating_pool(current_gen, selection_results)
    children = breed_pop(mating_pool, elite_size)
    next_generation = mutate_pop(children, mutation_rate)
    return next_generation


def genetic_algorithm(pop, pop_size, elite_size, mutation_rate, generations):
    pop = initial_population(pop_size, pop)
    print(f"Initial distance: {str(1 / rank_routes(pop)[0][1])}")

    for i in range(0, generations):
        pop = create_next_generation(pop, elite_size, mutation_rate)

    print(f"Final distance: {str(1 / rank_routes(pop)[0][1])}")
    best_route_index = rank_routes(pop)[0][0]
    best_route = pop[best_route_index]
    return best_route


def genetic_algorithm_track(pop, pop_size, elite_size, mutation_rate, generations):
    pop = initial_population(pop_size, pop)
    progress = []
    progress.append(1 / rank_routes(pop)[0][1])

    for i in range(0, generations):
        pop = create_next_generation(pop, elite_size, mutation_rate)
        progress.append(1 / rank_routes(pop)[0][1])

    print(f"1: {progress[0]}")
    print(f"{len(progress) // 4}: {progress[len(progress) // 4]}")
    print(f"{len(progress) // 2}: {progress[len(progress) // 2]}")
    print(f"{3 * len(progress) // 4}: {progress[3 * len(progress) // 4]}")
    print(f"{len(progress) - 1}: {progress[len(progress) - 1]}")


if __name__ == "__main__":
    city_list = []

    for i in range(0, 25):
        city_list.append(City(x=int(random.random() * 200),
                         y=int(random.random() * 200)))

    genetic_algorithm_track(pop=city_list, pop_size=100,
                            elite_size=20, mutation_rate=0.01, generations=500)
