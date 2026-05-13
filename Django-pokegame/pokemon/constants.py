"""
Game constants: type definitions, type effectiveness chart, XP/leveling formulas.
"""

# ── Type definitions ──────────────────────────────────────────────────────────
POKEMON_TYPES = [
    (0, 'Normal'),
    (1, 'Fire'),
    (2, 'Water'),
    (3, 'Grass'),
    (4, 'Electric'),
    (5, 'Psychic'),
    (6, 'Rock'),
    (7, 'Ghost'),
]

TYPE_NAMES = dict(POKEMON_TYPES)

TYPE_ICONS = {
    0: '⚪', 1: '🔥', 2: '💧', 3: '🌿',
    4: '⚡', 5: '🔮', 6: '🪨', 7: '👻',
}

TYPE_COLORS = {
    0: '#A8A878', 1: '#F08030', 2: '#6890F0', 3: '#78C850',
    4: '#F8D030', 5: '#F85888', 6: '#B8A038', 7: '#705898',
}

# ── Type effectiveness ─────────────────────────────────────────────────────────
# (attacker_type_id, defender_type_id): damage_multiplier
TYPE_EFFECTIVENESS = {
    # Fire (1)
    (1, 3): 2.0,   # Fire → Grass  : super effective
    (1, 6): 2.0,   # Fire → Rock   : super effective
    (1, 2): 0.5,   # Fire → Water  : not very effective
    (1, 1): 0.5,   # Fire → Fire   : not very effective
    # Water (2)
    (2, 1): 2.0,   # Water → Fire
    (2, 6): 2.0,   # Water → Rock
    (2, 3): 0.5,   # Water → Grass
    (2, 2): 0.5,   # Water → Water
    # Grass (3)
    (3, 2): 2.0,   # Grass → Water
    (3, 6): 2.0,   # Grass → Rock
    (3, 1): 0.5,   # Grass → Fire
    (3, 3): 0.5,   # Grass → Grass
    # Electric (4)
    (4, 2): 2.0,   # Electric → Water
    (4, 3): 0.5,   # Electric → Grass
    (4, 4): 0.5,   # Electric → Electric
    # Psychic (5)
    (5, 7): 2.0,   # Psychic → Ghost (doubled for fun)
    (5, 5): 0.5,   # Psychic → Psychic
    # Rock (6)
    (6, 1): 2.0,   # Rock → Fire
    (6, 0): 2.0,   # Rock → Normal
    (6, 2): 0.5,   # Rock → Water
    (6, 3): 0.5,   # Rock → Grass
    # Ghost (7)
    (7, 5): 2.0,   # Ghost → Psychic
    (7, 7): 2.0,   # Ghost → Ghost
    (7, 0): 0.0,   # Ghost → Normal : no effect
    (7, 6): 0.5,   # Ghost → Rock
}

# ── XP / Leveling ─────────────────────────────────────────────────────────────
XP_PER_LEVEL_MULTIPLIER = 100   # XP to level N+1 = N * multiplier

def xp_for_next_level(current_level: int) -> int:
    """XP needed from current_level to current_level + 1."""
    return current_level * XP_PER_LEVEL_MULTIPLIER

# XP rewards
XP_REWARD_WIN  = 60
XP_REWARD_LOSE = 15

# Stat bonuses per level-up
LEVEL_UP_HP_GAIN    = 5
LEVEL_UP_SPEED_GAIN = 2

# ── Wild player sentinel ───────────────────────────────────────────────────────
WILD_PLAYER_NAME = 'Wild'