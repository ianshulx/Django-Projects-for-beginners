import json

from django.contrib.auth.models import User
from django.db import models

from .constants import POKEMON_TYPES


# ── Core species models ───────────────────────────────────────────────────────

class Attack(models.Model):
    name        = models.CharField(max_length=100)
    damage      = models.IntegerField()
    attack_type = models.IntegerField(choices=POKEMON_TYPES, default=0)

    def __str__(self):
        return f"{self.name} ({self.get_attack_type_display()}, {self.damage} dmg)"


class Pokemon(models.Model):
    name         = models.CharField(max_length=100)
    hp           = models.IntegerField(help_text="Base HP for this species")
    level        = models.IntegerField(help_text="Base level of species (used as reference)")
    xp           = models.IntegerField(default=0, help_text="Base XP (reference only)")
    pokemon_type = models.IntegerField(choices=POKEMON_TYPES, default=0)
    attacks      = models.ManyToManyField(Attack, blank=True)
    speed        = models.IntegerField(help_text="Base speed for this species")
    is_starter   = models.BooleanField(default=False, help_text="Appears in starter selection")

    def __str__(self):
        return self.name


# ── Evolution chain ────────────────────────────────────────────────────────────

class EvolutionChain(models.Model):
    """Defines that from_pokemon evolves into to_pokemon at level_required."""
    from_pokemon     = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name='evolves_into'
    )
    to_pokemon       = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name='evolved_from'
    )
    level_required   = models.IntegerField()

    class Meta:
        unique_together = ('from_pokemon', 'to_pokemon')

    def __str__(self):
        return f"{self.from_pokemon} → {self.to_pokemon} (lv {self.level_required})"


# ── Player ────────────────────────────────────────────────────────────────────

class Player(models.Model):
    """
    Wraps Django's auth User.
    A special Player with name='wild' (no linked User) owns uncaptured Pokémon.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='player'
    )
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    @property
    def is_wild(self):
        return self.user is None


# ── MyPoke (individual owned Pokémon) ─────────────────────────────────────────

class MyPoke(models.Model):
    """
    An individual Pokémon owned by a Player.
    Tracks individual level/XP/stat-gains on top of the base species (Pokemon).
    """
    name    = models.CharField(max_length=100)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    player  = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='pokemons'
    )

    # Individual stat gains from leveling
    hp_gain    = models.IntegerField(default=0)
    speed_gain = models.IntegerField(default=0)

    # Individual progression
    current_level = models.IntegerField(default=1)
    current_xp    = models.IntegerField(default=0)

    def total_hp(self):
        return self.pokemon.hp + self.hp_gain

    def total_speed(self):
        return self.pokemon.speed + self.speed_gain

    def xp_to_next_level(self):
        from .constants import xp_for_next_level
        return xp_for_next_level(self.current_level)

    def xp_progress_percent(self):
        needed = self.xp_to_next_level()
        return int((self.current_xp / needed) * 100) if needed else 100

    def pending_evolution(self):
        """Return the Pokemon this MyPoke can evolve into, or None."""
        return (
            EvolutionChain.objects
            .filter(from_pokemon=self.pokemon, level_required__lte=self.current_level)
            .select_related('to_pokemon')
            .first()
        )

    def __str__(self):
        return f"{self.name} ({self.pokemon.name}, lv {self.current_level})"


# ── Battle Session ─────────────────────────────────────────────────────────────

class BattleSession(models.Model):
    ONGOING          = 'ongoing'
    CHALLENGER_WON   = 'challenger_won'
    OPPONENT_WON     = 'opponent_won'
    STATUS_CHOICES   = [
        (ONGOING,        'Ongoing'),
        (CHALLENGER_WON, 'Challenger Won'),
        (OPPONENT_WON,   'Opponent Won'),
    ]

    TURN_CHALLENGER = 'challenger'

    challenger_poke = models.ForeignKey(
        MyPoke, on_delete=models.CASCADE, related_name='battles_as_challenger'
    )
    opponent_poke   = models.ForeignKey(
        MyPoke, on_delete=models.CASCADE, related_name='battles_as_opponent'
    )

    challenger_hp   = models.IntegerField()
    opponent_hp     = models.IntegerField()

    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ONGOING)
    battle_log_json = models.TextField(default='[]')

    created_at      = models.DateTimeField(auto_now_add=True)

    # ── Log helpers ───────────────────────────────────────────────────────────

    @property
    def log(self):
        return json.loads(self.battle_log_json)

    def append_log(self, entry: dict):
        log = self.log
        log.append(entry)
        self.battle_log_json = json.dumps(log)

    # ── Convenience ───────────────────────────────────────────────────────────

    @property
    def is_ongoing(self):
        return self.status == self.ONGOING

    @property
    def challenger_won(self):
        return self.status == self.CHALLENGER_WON

    @property
    def opponent_is_wild(self):
        from .constants import WILD_PLAYER_NAME
        return self.opponent_poke.player.name == WILD_PLAYER_NAME

    def challenger_hp_percent(self):
        return max(0, int((self.challenger_hp / self.challenger_poke.total_hp()) * 100))

    def opponent_hp_percent(self):
        return max(0, int((self.opponent_hp / self.opponent_poke.total_hp()) * 100))

    def __str__(self):
        return (
            f"{self.challenger_poke} vs {self.opponent_poke} "
            f"[{self.get_status_display()}]"
        )