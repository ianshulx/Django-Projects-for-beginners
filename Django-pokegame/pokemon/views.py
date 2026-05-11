from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .constants import TYPE_ICONS, TYPE_NAMES, WILD_PLAYER_NAME, XP_REWARD_LOSE, XP_REWARD_WIN
from .forms import LoginForm, RegisterForm
from .models import Attack, BattleSession, MyPoke, Player, Pokemon
from .utils import award_xp, check_and_apply_evolution, process_challenger_turn


# ── Auth ──────────────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, Trainer {user.username}! Your journey begins.")
        return redirect('home')
    return render(request, 'pokemon/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'pokemon/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ── Home ──────────────────────────────────────────────────────────────────────

@login_required
def home_view(request):
    player   = request.user.player
    my_pokes = player.pokemons.select_related('pokemon').all()

    # Recent battle sessions involving the player
    recent_battles = BattleSession.objects.filter(
        challenger_poke__player=player
    ).select_related(
        'challenger_poke__pokemon', 'opponent_poke__pokemon'
    ).order_by('-created_at')[:5]

    return render(request, 'pokemon/home.html', {
        'my_pokes':       my_pokes,
        'recent_battles': recent_battles,
        'type_icons':     TYPE_ICONS,
        'type_names':     TYPE_NAMES,
    })


# ── Pokédex (browse all) ──────────────────────────────────────────────────────

@login_required
def pokedex_view(request):
    player = request.user.player

    wild_player = Player.objects.filter(name=WILD_PLAYER_NAME).first()
    wild_pokes  = (
        wild_player.pokemons.select_related('pokemon').all()
        if wild_player else MyPoke.objects.none()
    )
    # print(wild_player)
    print(player)
    other_pokes = (
        MyPoke.objects
        .exclude(player=player)
        .exclude(player__name=WILD_PLAYER_NAME)
        .select_related('pokemon', 'player')
    )

    return render(request, 'pokemon/pokedex.html', {
        'wild_pokes':   wild_pokes,
        'other_pokes':  other_pokes,
        'type_icons':   TYPE_ICONS,
        'type_names':   TYPE_NAMES,
    })


# ── My Pokémon ────────────────────────────────────────────────────────────────

@login_required
def my_pokemon_view(request):
    player   = request.user.player
    my_pokes = player.pokemons.select_related('pokemon').all()
    return render(request, 'pokemon/my_pokemon.html', {
        'my_pokes':   my_pokes,
        'type_icons': TYPE_ICONS,
        'type_names': TYPE_NAMES,
    })


@login_required
def my_pokemon_detail_view(request, mypoke_id):
    player = request.user.player
    mypoke = get_object_or_404(MyPoke, id=mypoke_id, player=player)
    return render(request, 'pokemon/my_pokemon_detail.html', {
        'mypoke':       mypoke,
        'type_icons':   TYPE_ICONS,
        'type_names':   TYPE_NAMES,
        'evolution':    mypoke.pending_evolution(),
    })


# ── Battle — choose your fighter ──────────────────────────────────────────────

@login_required
def battle_select_view(request, opponent_id):
    """
    Step 1: Player picks which of their Pokémon will fight the opponent.
    opponent_id = MyPoke.id of the target.
    """
    player   = request.user.player
    opponent = get_object_or_404(MyPoke, id=opponent_id)

    # Can't battle your own pokemon
    if opponent.player == player:
        messages.error(request, "You can't battle your own Pokémon!")
        return redirect('pokedex')

    my_pokes = player.pokemons.select_related('pokemon').all()
    if not my_pokes.exists():
        messages.error(request, "You have no Pokémon! Capture one first.")
        return redirect('pokedex')

    if request.method == 'POST':
        challenger_id = request.POST.get('challenger_id')
        challenger    = get_object_or_404(MyPoke, id=challenger_id, player=player)

        # Check for an already-ongoing session between these two
        existing = BattleSession.objects.filter(
            challenger_poke=challenger,
            opponent_poke=opponent,
            status=BattleSession.ONGOING,
        ).first()
        if existing:
            return redirect('battle_session', session_id=existing.id)

        session = BattleSession.objects.create(
            challenger_poke = challenger,
            opponent_poke   = opponent,
            challenger_hp   = challenger.total_hp(),
            opponent_hp     = opponent.total_hp(),
        )
        session.append_log({
            'system': True,
            'message': (
                f"Battle started! {challenger.name} (lv {challenger.current_level}) "
                f"vs {opponent.name} (lv {opponent.current_level}). "
                f"{'Wild ' if opponent.player.name == WILD_PLAYER_NAME else ''}"
                f"{opponent.pokemon.name} appeared!"
            ),
        })
        session.save()
        return redirect('battle_session', session_id=session.id)

    return render(request, 'pokemon/battle_select.html', {
        'opponent':   opponent,
        'my_pokes':   my_pokes,
        'type_icons': TYPE_ICONS,
        'type_names': TYPE_NAMES,
    })


# ── Battle — turn-based session ───────────────────────────────────────────────

@login_required
def battle_session_view(request, session_id):
    session  = get_object_or_404(BattleSession, id=session_id)
    player   = request.user.player
    challenger = session.challenger_poke

    # Only the challenger's owner may interact
    if challenger.player != player:
        print("wow")
        messages.error(request, "This is not your battle!")
        return redirect('home')

    if not session.is_ongoing:
        print("ok"  )
        return redirect('battle_result', session_id=session.id)

    if request.method == 'POST':
        attack_id = request.POST.get('attack_id')
        attack    = get_object_or_404(Attack, id=attack_id)

        # Validate the attack belongs to the challenger's moveset
        if not challenger.pokemon.attacks.filter(id=attack.id).exists():
            messages.error(request, "That attack doesn't belong to your Pokémon!")
            return redirect('battle_session', session_id=session.id)

        result = process_challenger_turn(session, attack)
        session.save()

        if result['battle_over']:
            # Award XP
            if session.challenger_won:
                xp_events = award_xp(challenger, XP_REWARD_WIN)
            else:
                xp_events = award_xp(challenger, XP_REWARD_LOSE)

            # Store XP events in session message
            for msg in xp_events:
                messages.info(request, msg)

        return redirect('battle_session', session_id=session.id)

    attacks = challenger.pokemon.attacks.all()
    log     = session.log[-8:]  # show last 8 entries

    return render(request, 'pokemon/battle.html', {
        'session':    session,
        'attacks':    attacks,
        'log':        log,
        'type_icons': TYPE_ICONS,
        'type_names': TYPE_NAMES,
    })


# ── Battle result ─────────────────────────────────────────────────────────────

@login_required
def battle_result_view(request, session_id):
    session  = get_object_or_404(BattleSession, id=session_id)
    player   = request.user.player
    challenger = session.challenger_poke

    if challenger.player != player:
        messages.error(request, "This is not your battle!")
        return redirect('home')

    # Evolution check
    evolution_name = None
    if session.challenger_won:
        evolution_name = check_and_apply_evolution(challenger)
        if evolution_name:
            messages.success(
                request,
                f"✨ {challenger.name} evolved into {evolution_name}!"
            )

    can_capture = (
        session.challenger_won
        and session.opponent_is_wild
        and session.opponent_poke.player.name == WILD_PLAYER_NAME
    )

    return render(request, 'pokemon/battle_result.html', {
        'session':        session,
        'can_capture':    can_capture,
        'evolution_name': evolution_name,
        'type_icons':     TYPE_ICONS,
    })


# ── Capture ───────────────────────────────────────────────────────────────────

@login_required
def capture_view(request, session_id):
    session    = get_object_or_404(BattleSession, id=session_id)
    player     = request.user.player
    challenger = session.challenger_poke

    if challenger.player != player:
        messages.error(request, "Not your battle.")
        return redirect('home')

    if not session.challenger_won:
        messages.error(request, "You must win the battle to capture a Pokémon!")
        return redirect('battle_result', session_id=session.id)

    wild_poke = session.opponent_poke
    if wild_poke.player.name != WILD_PLAYER_NAME:
        messages.error(request, "You can only capture wild Pokémon.")
        return redirect('battle_result', session_id=session.id)

    # Transfer ownership
    wild_poke.player = player
    wild_poke.save()

    messages.success(
        request,
        f"Gotcha! {wild_poke.name} ({wild_poke.pokemon.name}) was added to your team!"
    )
    return redirect('my_pokemon')


# ── Evolution ─────────────────────────────────────────────────────────────────

@login_required
def evolve_view(request, mypoke_id):
    player = request.user.player
    mypoke = get_object_or_404(MyPoke, id=mypoke_id, player=player)
    chain  = mypoke.pending_evolution()

    if not chain:
        messages.info(request, f"{mypoke.name} cannot evolve yet.")
        return redirect('my_pokemon_detail', mypoke_id=mypoke.id)

    if request.method == 'POST':
        new_name = check_and_apply_evolution(mypoke)
        if new_name:
            messages.success(request, f"✨ {mypoke.name} evolved into {new_name}!")
        return redirect('my_pokemon_detail', mypoke_id=mypoke.id)

    return render(request, 'pokemon/evolution.html', {
        'mypoke':      mypoke,
        'evolved_to':  chain.to_pokemon,
        'type_icons':  TYPE_ICONS,
        'type_names':  TYPE_NAMES,
    })