"""
Pipeline package for M3 Expressive presentation generation.
"""

from pipeline.schema import DeckConfig, SlidePlan, DeckPlan
from pipeline.planner import PlanMapper, auto_plan_from_outline
from pipeline.builder import M3DeckBuilder, build_deck_from_dict, build_deck_from_json

__all__ = [
    "DeckConfig",
    "SlidePlan",
    "DeckPlan",
    "PlanMapper",
    "auto_plan_from_outline",
    "M3DeckBuilder",
    "build_deck_from_dict",
    "build_deck_from_json",
]
