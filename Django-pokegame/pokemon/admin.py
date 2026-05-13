from django.contrib import admin

from .models import Attack, BattleSession, EvolutionChain, MyPoke, Player, Pokemon


@admin.register(Attack)
class AttackAdmin(admin.ModelAdmin):
    list_display = ('name', 'damage', 'attack_type')
    list_filter  = ('attack_type',)


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display  = ('name', 'pokemon_type', 'hp', 'speed', 'level')
    list_filter   = ('pokemon_type',)
    filter_horizontal = ('attacks',)


@admin.register(EvolutionChain)
class EvolutionChainAdmin(admin.ModelAdmin):
    list_display = ('from_pokemon', 'to_pokemon', 'level_required')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


@admin.register(MyPoke)
class MyPokeAdmin(admin.ModelAdmin):
    list_display  = ('name', 'pokemon', 'player', 'current_level', 'current_xp')
    list_filter   = ('player',)
    raw_id_fields = ('pokemon', 'player')


@admin.register(BattleSession)
class BattleSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'challenger_poke', 'opponent_poke',
        'challenger_hp', 'opponent_hp', 'status', 'created_at',
    )
    list_filter  = ('status',)
    readonly_fields = ('created_at', 'battle_log_json')