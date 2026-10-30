def _car_values(cars):
    return cars.values() if hasattr(cars, "values") else cars


def rank(cars):
    active_cars = [car for car in _car_values(cars) if car.is_active]
    return sorted(active_cars, key=lambda car: (-car.distance, -car.health, car.name))


def best_active(cars):
    ranked = rank(cars)
    return ranked[0] if ranked else None


def format_rank(cars):
    ranked = rank(cars)
    return " ".join(car.name for car in ranked) if ranked else "NONE"
