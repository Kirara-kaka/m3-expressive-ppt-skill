"""
Data Schema and Models for M3 Expressive presentation generation.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json

VALID_ARCHETYPES = [
    "cover_hero",
    "bento_grid",
    "process_roadmap",
    "dual_contrast",
    "kpi_metrics",
    "feature_list",
    "quote_takeaway",
    "team_showcase",
]

VALID_THEME_PRESETS = [
    "indigo_coral",
    "electric_mint",
    "digital_lavender",
    "warm_amber",
    "electric_violet",
]

@dataclass
class DeckConfig:
    title: str = "Presentation Deck"
    preset_theme: str = "indigo_coral"
    seed_color: Optional[str] = None
    is_dark: bool = False
    aspect_ratio: str = "16:9"
    total_pages: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeckConfig":
        return cls(
            title=data.get("title", "Presentation Deck"),
            preset_theme=data.get("preset_theme", "indigo_coral"),
            seed_color=data.get("seed_color"),
            is_dark=data.get("is_dark", False),
            aspect_ratio=data.get("aspect_ratio", "16:9"),
            total_pages=data.get("total_pages", 1)
        )

@dataclass
class SlidePlan:
    archetype: str
    content: Dict[str, Any] = field(default_factory=dict)
    page_num: int = 1

    def __post_init__(self):
        if self.archetype not in VALID_ARCHETYPES:
            raise ValueError(f"Unknown archetype '{self.archetype}'. Valid options: {VALID_ARCHETYPES}")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SlidePlan":
        return cls(
            archetype=data.get("archetype", "bento_grid"),
            content=data.get("content", {}),
            page_num=data.get("page_num", 1)
        )

@dataclass
class DeckPlan:
    config: DeckConfig
    slides: List[SlidePlan] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "config": self.config.to_dict(),
            "slides": [s.to_dict() for s in self.slides]
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeckPlan":
        config = DeckConfig.from_dict(data.get("config", {}))
        raw_slides = data.get("slides", [])
        slides = []
        for i, s in enumerate(raw_slides, start=1):
            if isinstance(s, dict):
                sp = SlidePlan.from_dict(s)
                if not sp.page_num:
                    sp.page_num = i
                slides.append(sp)
        config.total_pages = len(slides)
        return cls(config=config, slides=slides)

    @classmethod
    def from_json(cls, json_str: str) -> "DeckPlan":
        return cls.from_dict(json.loads(json_str))
