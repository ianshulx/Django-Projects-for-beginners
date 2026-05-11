from django.urls import path

from . import views

urlpatterns = [
    # ── Auth ─────────────────────────────────────────────────────────────────
    path('register/', views.register_view,  name='register'),
    path('login/',    views.login_view,     name='login'),
    path('logout/',   views.logout_view,    name='logout'),

    # ── Main ──────────────────────────────────────────────────────────────────
    path('',          views.home_view,      name='home'),
    path('pokedex/',  views.pokedex_view,   name='pokedex'),

    # ── My Pokémon ────────────────────────────────────────────────────────────
    path('my-pokemon/',                     views.my_pokemon_view,        name='my_pokemon'),
    path('my-pokemon/<int:mypoke_id>/',     views.my_pokemon_detail_view, name='my_pokemon_detail'),

    # ── Battle ────────────────────────────────────────────────────────────────
    path('battle/select/<int:opponent_id>/', views.battle_select_view,  name='battle_select'),
    path('battle/session/<int:session_id>/', views.battle_session_view, name='battle_session'),
    path('battle/result/<int:session_id>/',  views.battle_result_view,  name='battle_result'),
    path('battle/capture/<int:session_id>/', views.capture_view,        name='capture'),

    # ── Evolution ─────────────────────────────────────────────────────────────
    path('evolve/<int:mypoke_id>/', views.evolve_view, name='evolve'),
]