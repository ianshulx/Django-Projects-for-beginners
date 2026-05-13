# PokéDjango

A turn-based Pokémon game built with Django. Battle wild Pokémon, capture them, train your team, and challenge other trainers.

---

## Features

- **Auth** — register/login via Django's built-in auth, auto-creates a linked `Player`
- **Pokédex** — browse wild Pokémon and other trainers' Pokémon
- **Turn-based battles** — pick your fighter, choose attacks each turn, AI opponent responds
- **Type effectiveness** — 8 types with a full super-effective/not-very-effective chart
- **Capture** — win against a wild Pokémon to add it to your team
- **XP & leveling** — earn XP from battles, level up with stat gains
- **Evolution** — Pokémon evolve automatically when level thresholds are met
- **Battle log** — full turn-by-turn history stored per session

---

## Project Structure

```
pokemon/
├── models.py        # Attack, Pokemon, EvolutionChain, Player, MyPoke, BattleSession
├── constants.py     # Type chart, XP formulas, type icons/colors
├── utils.py         # Damage calc, AI move selection, XP award, evolution check
├── views.py         # All views: auth, home, pokédex, battle, capture, evolution
├── urls.py          # App-level URL routing
├── forms.py         # RegisterForm, LoginForm
├── signals.py       # Auto-creates Player on User registration
├── apps.py          # Wires up signals
├── admin.py         # Admin registration for all models
└── templates/pokemon/
    ├── base.html
    ├── home.html
    ├── register.html
    ├── login.html
    ├── pokedex.html
    ├── my_pokemon.html
    ├── my_pokemon_detail.html
    ├── battle_select.html
    ├── battle.html
    ├── battle_result.html
    └── evolution.html
```

---

## Setup

**1. Install Django**
```bash
pip install django
```

**2. Add to `INSTALLED_APPS` in `settings.py`**
```python
INSTALLED_APPS = [
    ...
    'pokemon.apps.PokemonConfig',
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
```

**3. Wire up URLs in your project's `urls.py`**
```python
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       include('pokemon.urls')),
]
```

**4. Run migrations**
```bash
python manage.py makemigrations pokemon
python manage.py migrate
```

**5. Create a superuser**
```bash
python manage.py createsuperuser
```

**6. Seed data via `/admin/`**

| What | Details |
|---|---|
| `Attack` | Name, damage, type (e.g. Thunderbolt, 55, Electric) |
| `Pokemon` | Name, HP, speed, type, assign attacks |
| `Player` | Name = `wild`, leave User blank |
| `MyPoke` | Assign species + wild player — these appear in the Pokédex |
| `EvolutionChain` | e.g. Bulbasaur → Ivysaur at level 16 |

---

## Game Flow

```
Register / Login
      │
      ▼
   Home ──── My Team ──── Pokémon Detail ──── Evolve
      │
      ▼
   Pokédex (wild + other trainers)
      │
      ▼
   Pick opponent ──► Pick your fighter
                           │
                           ▼
                      Battle (turn-based)
                           │
                     ┌─────┴─────┐
                   Win           Lose
                    │              │
              Result screen    Result screen
                    │              │
               (if wild)      XP awarded (+15)
            Capture option
                    │
               XP awarded (+60)
                    │
            Evolution check
```

---

## Models

### `Attack`
| Field | Type |
|---|---|
| `name` | CharField |
| `damage` | IntegerField |
| `attack_type` | IntegerField (choice) |

### `Pokemon` (species template)
| Field | Type |
|---|---|
| `name` | CharField |
| `hp` | IntegerField |
| `speed` | IntegerField |
| `level` | IntegerField |
| `pokemon_type` | IntegerField (choice) |
| `attacks` | ManyToManyField → Attack |

### `MyPoke` (individual owned Pokémon)
| Field | Type |
|---|---|
| `name` | CharField |
| `pokemon` | ForeignKey → Pokemon |
| `player` | ForeignKey → Player |
| `hp_gain` | IntegerField |
| `speed_gain` | IntegerField |
| `current_level` | IntegerField |
| `current_xp` | IntegerField |

### `BattleSession`
Stores live HP, turn log (JSON), and status (`ongoing` / `challenger_won` / `opponent_won`).

---

## Type Chart

| Type | Super effective against |
|---|---|
| Fire | Grass, Rock |
| Water | Fire, Rock |
| Grass | Water, Rock |
| Electric | Water |
| Psychic | Ghost |
| Rock | Fire, Normal |
| Ghost | Psychic, Ghost |

Multipliers: `2.0` (super effective), `0.5` (not very effective), `0.0` (no effect).

---

## XP & Leveling

| Event | XP gained |
|---|---|
| Win a battle | +60 |
| Lose a battle | +15 |

XP to next level = `current_level × 100`

Each level-up grants: **+5 HP**, **+2 Speed**