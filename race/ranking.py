"""Ordering and presentation helpers for active race cars."""


def _car_values(cars):
    """Accept either an iterable of cars or a name-to-car mapping."""
    return cars.values() if hasattr(cars, "values") else cars


def rank(cars):
    """Return active cars by distance, health, then English name."""
    active_cars = [car for car in _car_values(cars) if car.is_active]
    return sorted(active_cars, key=lambda car: (-car.distance, -car.health, car.name))


def best_active(cars):
    """Return the first ranked active car, or None if all cars are eliminated."""
    ranked = rank(cars)
    return ranked[0] if ranked else None


def format_rank(cars):
    """Format the ranking command's result without printing it."""
    ranked = rank(cars)
    return " ".join(car.name for car in ranked) if ranked else "NONE"
