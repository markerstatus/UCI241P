from collections import deque


class City:
    """One city and the highways that leave it."""

    def __init__(self, name, population):
        self.name = name
        self.population = population
        self.connected = []


def build_graph(population_path, road_path):
    """Read the population and highway files into an undirected city graph.

    params:
        population_path: path to lines of "<city name> : <population>"
        road_path: path to lines of "<city name 1> : <city name 2>"
    return:
        list of City: every city, with connected holding neighboring City objects
    """
    cities = {}
    with open(population_path, encoding="utf-8") as population_fs:
        for line in population_fs:
            line = line.strip()
            if not line:
                continue
            name, population = line.split(" : ", 1)
            cities[name] = City(name, int(population))

    with open(road_path, encoding="utf-8") as road_fs:
        for line in road_fs:
            line = line.strip()
            if not line:
                continue
            left_name, right_name = line.split(" : ", 1)
            left_city = cities[left_name]
            right_city = cities[right_name]
            if left_city is right_city:
                continue
            if right_city not in left_city.connected:
                left_city.connected.append(right_city)
            if left_city not in right_city.connected:
                right_city.connected.append(left_city)

    return list(cities.values())


def connected_city_group(cities):
    visited = set()
    components = []
    for city in cities:
        if city in visited:
            continue
        stack = [city]
        visited.add(city)
        component = []
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in current.connected:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        components.append(component)
    return components


def count_connected_city_group(cities):
    return len(connected_city_group(cities))


def count_each_connected_city_group_populations(cities):
    populations = [
        sum(city.population for city in component)
        for component in connected_city_group(cities)
    ]
    return sorted(populations)


def highway_distance(start, end):
    """Return the fewest highways between two cities, or -1 if unreachable.
    BFS algorithm.

    params:
        start: City
        end: City
    return:
        int: shortest path length; 0 when start is end
    """
    if start is end:  # edge case
        return 0

    visited = {start}
    # use deque for efficient popping from the left
    queue = deque([(start, 0)])
    while queue:
        current, distance = queue.popleft()
        for neighbor in current.connected:
            if neighbor is end:
                return distance + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    return -1


def test_files():
    cities = build_graph("city_population.txt", "road_network.txt")
    by_name = {city.name: city for city in cities}
    populations = count_each_connected_city_group_populations(cities)
    groups = connected_city_group(cities)

    assert len(cities) == 925
    assert len(by_name) == 925
    assert count_connected_city_group(cities) == 1
    assert populations == [119854062]
    assert sum(populations) == sum(city.population for city in cities)
    assert sum(len(group) for group in groups) == len(cities)

    for city in cities:
        neighbor_names = [neighbor.name for neighbor in city.connected]
        assert city not in city.connected
        assert len(neighbor_names) == len(set(neighbor_names))
        for neighbor in city.connected:
            assert city in neighbor.connected
            assert highway_distance(city, neighbor) == 1
            assert highway_distance(neighbor, city) == 1

    expected_populations = {
        "New York": 8405837,
        "Los Angeles": 3884307,
        "Nashville-Davidson": 634464,
        "Louisville/Jefferson County": 609893,
        "Lee's Summit": 93184,
        "O'Fallon": 82809,
    }
    for name, population in expected_populations.items():
        assert by_name[name].population == population
        assert by_name[name].connected

    new_york = by_name["New York"]
    assert by_name["Warwick"] in new_york.connected
    assert by_name["Oxnard"] not in new_york.connected

    distance_cases = [
        ("New York", "New York", 0),
        ("New York", "Warwick", 1),
        ("Phoenix", "San Jose", 1),
        ("New York", "Oxnard", 2),
        ("Atlanta", "Detroit", 2),
        ("New York", "Los Angeles", 3),
        ("Boston", "San Antonio", 3),
        ("New York", "San Antonio", 4),
        ("Boston", "Seattle", 4),
        ("Atlanta", "Denver", 5),
        ("New York", "Hoover", 6),
    ]
    for start_name, end_name, expected in distance_cases:
        start = by_name[start_name]
        end = by_name[end_name]
        assert highway_distance(start, end) == expected
        assert highway_distance(end, start) == expected

    print(f"Cities: {len(cities)}")
    print(f"Islands: {count_connected_city_group(cities)}")
    print(f"Island populations: {populations}")
    for start_name, end_name, expected in distance_cases:
        print(f"Distance {start_name} -> {end_name}: {expected}")


def main():
    test_files()
    print("All tests passed.")


if __name__ == "__main__":
    main()
