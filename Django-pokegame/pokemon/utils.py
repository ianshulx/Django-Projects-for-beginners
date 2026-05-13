"""
Battle and progression utilities.
Keep all game-logic here, out of views.
"""
import random

from .constants import (
    TYPE_EFFECTIVENESS,
    XP_REWARD_WIN, XP_REWARD_LOSE,
    LEVEL_UP_HP_GAIN, LEVEL_UP_SPEED_GAIN,
    xp_for_next_level,
)


# ── Damage calculation ────────────────────────────────────────────────────────

def get_effectiveness(attack_type: int, defender_type: int) -> float:
    return TYPE_EFFECTIVENESS.get((attack_type, defender_type), 1.0)


def effectiveness_label(multiplier: float) -> str:
    if multiplier == 0.0:
        return "It had no effect!"
    if multiplier >= 2.0:
        return "It's super effective!"
    if multiplier <= 0.5:
        return "It's not very effective..."
    return ""


def calculate_damage(attack, defender_poke) -> tuple[int, float, str]:
    """
    Returns (damage_dealt, effectiveness_multiplier, flavor_text).
    defender_poke is a MyPoke instance.
    """
    mult   = get_effectiveness(attack.attack_type, defender_poke.pokemon.pokemon_type)
    damage = max(1, int(attack.damage * mult))
    label  = effectiveness_label(mult)
    return damage, mult, label


# ── AI move selection ─────────────────────────────────────────────────────────

def ai_choose_attack(mypoke):
    """Return a random Attack from mypoke's species moveset, or None."""
    attacks = list(mypoke.pokemon.attacks.all())
    return random.choice(attacks) if attacks else None


# ── XP and leveling ───────────────────────────────────────────────────────────

def award_xp(mypoke, xp_amount: int) -> list[str]:
    """
    Award XP to a MyPoke, handling level-ups.
    Returns a list of event messages (level-up notices, etc.).
    Saves the mypoke instance.
    """
    events = []
    mypoke.current_xp += xp_amount
    events.append(f"{mypoke.name} gained {xp_amount} XP!")

    while mypoke.current_xp >= xp_for_next_level(mypoke.current_level):
        mypoke.current_xp -= xp_for_next_level(mypoke.current_level)
        mypoke.current_level += 1
        mypoke.hp_gain    += LEVEL_UP_HP_GAIN
        mypoke.speed_gain += LEVEL_UP_SPEED_GAIN
        events.append(
            f"{mypoke.name} grew to level {mypoke.current_level}! "
            f"(+{LEVEL_UP_HP_GAIN} HP, +{LEVEL_UP_SPEED_GAIN} Speed)"
        )

    mypoke.save()
    return events


# ── Evolution helpers ─────────────────────────────────────────────────────────

def check_and_apply_evolution(mypoke) -> str | None:
    """
    If mypoke is eligible to evolve, apply the evolution and return
    the new pokemon name.  Returns None if no evolution occurred.
    """
    chain = mypoke.pending_evolution()
    if chain is None:
        return None
    mypoke.pokemon = chain.to_pokemon
    mypoke.save()
    return chain.to_pokemon.name


# ── Battle-turn processor ─────────────────────────────────────────────────────

def process_challenger_turn(session, attack) -> dict:
    """
    Apply the challenger's chosen attack, then the AI opponent's turn.
    Mutates session (does NOT call session.save() — caller must save).
    Returns a dict: { 'events': [...], 'battle_over': bool }
    """
    events = []

    # ── Challenger attacks ────────────────────────────────────────────────────
    dmg, mult, label = calculate_damage(attack, session.opponent_poke)
    session.opponent_hp = max(0, session.opponent_hp - dmg)
    entry = {
        'actor':  session.challenger_poke.name,
        'attack': attack.name,
        'damage': dmg,
        'label':  label,
        'target': session.opponent_poke.name,
        'remaining_hp': session.opponent_hp,
        'side': 'challenger',
    }
    session.append_log(entry)
    events.append(
        f"{session.challenger_poke.name} used {attack.name}! "
        f"({dmg} damage{'. ' + label if label else ''})"
    )

    if session.opponent_hp <= 0:
        from .models import BattleSession
        session.status = BattleSession.CHALLENGER_WON
        return {'events': events, 'battle_over': True}

    # ── Opponent (AI) attacks ─────────────────────────────────────────────────
    ai_attack = ai_choose_attack(session.opponent_poke)
    if ai_attack:
        dmg2, mult2, label2 = calculate_damage(ai_attack, session.challenger_poke)
        session.challenger_hp = max(0, session.challenger_hp - dmg2)
        entry2 = {
            'actor':  session.opponent_poke.name,
            'attack': ai_attack.name,
            'damage': dmg2,
            'label':  label2,
            'target': session.challenger_poke.name,
            'remaining_hp': session.challenger_hp,
            'side': 'opponent',
        }
        session.append_log(entry2)
        events.append(
            f"{session.opponent_poke.name} used {ai_attack.name}! "
            f"({dmg2} damage{'. ' + label2 if label2 else ''})"
        )

    if session.challenger_hp <= 0:
        from .models import BattleSession
        session.status = BattleSession.OPPONENT_WON
        return {'events': events, 'battle_over': True}

    return {'events': events, 'battle_over': False}