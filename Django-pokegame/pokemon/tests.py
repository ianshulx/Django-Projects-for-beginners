from django.test import TestCase
from django.contrib.auth.models import User
from .models import Pokemon, Attack, MyPoke, Player, EvolutionChain, BattleSession
from .services import calculate_damage, get_initial_battle_state, run_turn, catch_pokemon
from .constants import XP_REWARD_WIN, WILD_PLAYER_NAME

class PokemonBattleSystemTests(TestCase):

    def setUp(self):
        # 1. Create a User and Players
        self.user = User.objects.create_user(username="ash", password="password123")
        self.player = Player.objects.create(user=self.user, name="Ash")
        self.wild_player = Player.objects.create(user=None, name=WILD_PLAYER_NAME)

        # 2. Create Attacks
        self.tackle = Attack.objects.create(name="Tackle", damage=20, attack_type=0)
        self.ember = Attack.objects.create(name="Ember", damage=25, attack_type=1)

        # 3. Create Base Pokemon
        self.charmander_base = Pokemon.objects.create(
            name="Charmander", hp=50, level=5, speed=40, pokemon_type=1
        )
        self.charmander_base.attacks.add(self.ember, self.tackle)
        
        self.charmeleon_base = Pokemon.objects.create(
            name="Charmeleon", hp=80, level=16, speed=60, pokemon_type=1
        )

        # 4. Create Evolution Chain
        EvolutionChain.objects.create(
            from_pokemon=self.charmander_base,
            to_pokemon=self.charmeleon_base,
            level_required=16
        )

        # 5. Create specific MyPoke instances
        self.player_poke = MyPoke.objects.create(
            name="My Charmander",
            pokemon=self.charmander_base,
            player=self.player,
            current_level=5
        )
        
        self.wild_poke = MyPoke.objects.create(
            name="Wild Charmander",
            pokemon=self.charmander_base,
            player=self.wild_player,
            current_level=5
        )

    # ── Model Property Tests ──────────────────────────────────────────

    def test_total_stats_calculation(self):
        """Check that base stats + gains sum up correctly."""
        self.player_poke.hp_gain = 10
        self.player_poke.speed_gain = 5
        self.player_poke.save()
        
        expected_hp = self.charmander_base.hp + 10
        expected_speed = self.charmander_base.speed + 5
        
        self.assertEqual(self.player_poke.total_hp(), expected_hp)
        self.assertEqual(self.player_poke.total_speed(), expected_speed)

    def test_evolution_logic(self):
        """Check if pending_evolution correctly detects level requirements."""
        # Level 5: No evolution yet
        self.assertIsNone(self.player_poke.pending_evolution())
        
        # Level 16: Evolution should be available
        self.player_poke.current_level = 16
        self.player_poke.save()
        
        evolution = self.player_poke.pending_evolution()
        self.assertIsNotNone(evolution)
        self.assertEqual(evolution.to_pokemon.name, "Charmeleon")

    # ── Service Logic Tests ───────────────────────────────────────────

    def test_calculate_damage_reduction(self):
        """Ensure defender speed reduces damage, but never below 1."""
        # attacker_dmg 20 - (speed 40 // 10) = 16
        damage = calculate_damage(20, 40)
        self.assertEqual(damage, 16)
        
        # Test minimum damage floor
        low_damage = calculate_damage(2, 50)
        self.assertEqual(low_damage, 1)

    def test_battle_flow_initialization(self):
        """Verify the initial state dictionary structure."""
        state = get_initial_battle_state(self.player_poke, self.wild_poke)
        
        self.assertEqual(state['player_poke_id'], self.player_poke.id)
        self.assertEqual(state['status'], 'ongoing')
        self.assertEqual(state['player_current_hp'], self.player_poke.total_hp())

    def test_run_turn_victory(self):
        """Test a turn where the player wins."""
        # Set wild poke to 1 HP
        state = get_initial_battle_state(self.player_poke, self.wild_poke)
        state['world_current_hp'] = 1
        
        # Player uses Tackle (20 dmg)
        updated_state = run_turn(state, self.tackle.id)
        
        self.assertEqual(updated_state['world_current_hp'], 0)
        self.assertEqual(updated_state['status'], 'player_won')
        self.assertIn("fainted! You won!", updated_state['turn_log'][-1])

    def test_catch_pokemon_service(self):
        """Verify ownership transfer works."""
        self.assertTrue(self.wild_poke.player.is_wild)
        
        catch_pokemon(self.player, self.wild_poke)
        
        # Refresh from DB
        self.wild_poke.refresh_from_db()
        self.assertEqual(self.wild_poke.player, self.player)
        self.assertFalse(self.wild_poke.player.is_wild)

    # ── Edge Cases ───────────────────────────────────────────────────

    def test_no_attacks_logic(self):
        """Ensure game doesn't crash if a wild pokemon has no attacks."""
        self.wild_poke.pokemon.attacks.clear()
        state = get_initial_battle_state(self.player_poke, self.wild_poke)
        
        # Run a turn. If no crash and log contains "skipped", it's a success.
        updated_state = run_turn(state, self.tackle.id)
        self.assertTrue(any("skipped its turn" in entry for entry in updated_state['turn_log']))