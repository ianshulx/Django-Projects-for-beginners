# services.py

from .models import MyPoke, Player


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

def get_available_attacks(my_poke: MyPoke) -> list:
    """
    Returns a list of Attack objects linked to this MyPoke's base Pokemon.
    These are shown to the player so they can choose one per turn.
    """
    return list(my_poke.pokemon.attacks.all())


def calculate_damage(attack_damage: int, defender_speed: int) -> int:
    """
    Simple damage formula.
    Defender's speed slightly reduces damage (acts as a soft defense).
    Minimum 1 damage always dealt.
    """
    damage = attack_damage - (defender_speed // 10)
    return max(1, damage)


# ─────────────────────────────────────────
# BATTLE
# ─────────────────────────────────────────

def get_initial_battle_state(player_poke: MyPoke, world_poke: MyPoke) -> dict:
    """
    Call this once when a battle starts.
    Returns a state dict that your view will keep passing back on every turn.

    Store this in Django session:
        request.session['battle_state'] = get_initial_battle_state(...)
    """
    return {
        "player_poke_id": player_poke.id,
        "world_poke_id": world_poke.id,
        "player_current_hp": player_poke.pokemon.hp + player_poke.hp_gain,
        "world_current_hp": world_poke.pokemon.hp + world_poke.hp_gain,
        "turn_log": [],       # list of strings describing what happened
        "status": "ongoing",  # "ongoing" | "player_won" | "world_won"
    }


def run_turn(state: dict, chosen_attack_id: int) -> dict:
    """
    Resolves one full turn (player attacks → world attacks back).
    
    Takes:
        state            — the battle state dict from session
        chosen_attack_id — the id of the Attack the player chose this turn

    Returns:
        updated state dict — save this back to session after calling
    """
    from .models import Attack  # local import to avoid circular imports

    log = []

    # ── Fetch what we need ──────────────────────────────────────────
    player_poke = MyPoke.objects.get(id=state["player_poke_id"])
    world_poke  = MyPoke.objects.get(id=state["world_poke_id"])
    chosen_attack = Attack.objects.get(id=chosen_attack_id)

    player_hp = state["player_current_hp"]
    world_hp  = state["world_current_hp"]

    # ── Player attacks ──────────────────────────────────────────────
    damage_to_world = calculate_damage(
        chosen_attack.damage,
        world_poke.pokemon.speed + world_poke.speed_gain
    )
    world_hp -= damage_to_world
    log.append(f"{player_poke.name} used {chosen_attack.name} → {damage_to_world} damage!")

    if world_hp <= 0:
        world_hp = 0
        log.append(f"{world_poke.name} fainted! You won!")
        state["world_current_hp"] = world_hp
        state["turn_log"].extend(log)
        state["status"] = "player_won"
        return state

    # ── World attacks back ──────────────────────────────────────────
    world_attacks = get_available_attacks(world_poke)

    if world_attacks:
        import random
        world_chosen_attack = random.choice(world_attacks)   # World picks randomly
        damage_to_player = calculate_damage(
            world_chosen_attack.damage,
            player_poke.pokemon.speed + player_poke.speed_gain
        )
        player_hp -= damage_to_player
        log.append(f"{world_poke.name} used {world_chosen_attack.name} → {damage_to_player} damage!")
    else:
        log.append(f"{world_poke.name} has no attacks and skipped its turn.")

    if player_hp <= 0:
        player_hp = 0
        log.append(f"{player_poke.name} fainted! You lost!")
        state["player_current_hp"] = player_hp
        state["world_current_hp"]  = world_hp
        state["turn_log"].extend(log)
        state["status"] = "world_won"
        return state

    # ── Still ongoing ───────────────────────────────────────────────
    state["player_current_hp"] = player_hp
    state["world_current_hp"]  = world_hp
    state["turn_log"].extend(log)
    state["status"] = "ongoing"
    return state


# ─────────────────────────────────────────
# CATCHING
# ─────────────────────────────────────────

def catch_pokemon(player: Player, world_poke: MyPoke) -> MyPoke:
    """
    Transfers ownership of a wild MyPoke from World to the player.
    Call this only after run_turn returns status = "player_won".
    """
    world_poke.player = player
    world_poke.save()
    return world_poke