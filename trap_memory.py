trap_zones = []

def remember_trap_zone(price_level):
    if price_level not in trap_zones:
        trap_zones.append(price_level)

def check_reentry(price, tolerance=5):
    return any(abs(price - z) < tolerance for z in trap_zones)

def get_trap_memory():
    return trap_zones
