"""Cubone reference data for quick lookup and formatted summaries.

This module stores core facts about the Ground-type Pokémon Cubone across
mainline games. It is intended as a concise, code-friendly knowledge base for
creative or tooling purposes.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Stats:
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    def as_dict(self) -> Dict[str, int]:
        return {
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "special_attack": self.special_attack,
            "special_defense": self.special_defense,
            "speed": self.speed,
        }


@dataclass(frozen=True)
class Evolution:
    into: str
    trigger: str
    notes: Optional[str] = None


@dataclass(frozen=True)
class Move:
    name: str
    move_type: str
    category: str
    power: Optional[int]
    accuracy: Optional[int]
    description: str


@dataclass(frozen=True)
class Pokemon:
    name: str
    national_dex: int
    species: str
    types: List[str]
    height_m: float
    weight_kg: float
    abilities: List[str]
    hidden_ability: str
    base_stats: Stats
    evolutions: List[Evolution]
    notable_moves: List[Move]
    flavor: str

    def summary(self) -> str:
        """Return a formatted summary string for Cubone."""

        lines = [
            f"Pokédex #{self.national_dex}: {self.name} — {self.species}",
            f"Types: {', '.join(self.types)}",
            f"Height/Weight: {self.height_m} m / {self.weight_kg} kg",
            f"Abilities: {', '.join(self.abilities)} (Hidden: {self.hidden_ability})",
            "Base Stats:",
        ]

        for stat, value in self.base_stats.as_dict().items():
            lines.append(f"  {stat.title()}: {value}")

        lines.append("Evolutions:")
        for evo in self.evolutions:
            detail = f"  → {evo.into} via {evo.trigger}"
            if evo.notes:
                detail += f" ({evo.notes})"
            lines.append(detail)

        lines.append("Notable Moves:")
        for move in self.notable_moves:
            power = "—" if move.power is None else str(move.power)
            accuracy = "—" if move.accuracy is None else f"{move.accuracy}%"
            lines.append(
                f"  {move.name} ({move.move_type}, {move.category}, Power {power}, Accuracy {accuracy})"
                f" — {move.description}"
            )

        lines.append("Flavor:")
        lines.append(f"  {self.flavor}")
        return "\n".join(lines)


CUBONE = Pokemon(
    name="Cubone",
    national_dex=104,
    species="Lonely Pokémon",
    types=["Ground"],
    height_m=0.4,
    weight_kg=6.5,
    abilities=["Rock Head", "Lightning Rod"],
    hidden_ability="Battle Armor",
    base_stats=Stats(hp=50, attack=50, defense=95, special_attack=40, special_defense=50, speed=35),
    evolutions=[
        Evolution(
            into="Marowak",
            trigger="Level 28",
            notes="Alolan Marowak when evolved at night in Alola",
        )
    ],
    notable_moves=[
        Move(
            name="Bone Club",
            move_type="Ground",
            category="Physical",
            power=65,
            accuracy=85,
            description="A signature bone strike that can make the target flinch.",
        ),
        Move(
            name="Bonemerang",
            move_type="Ground",
            category="Physical",
            power=50,
            accuracy=90,
            description="Throws a bone that hits twice before returning.",
        ),
        Move(
            name="Headbutt",
            move_type="Normal",
            category="Physical",
            power=70,
            accuracy=100,
            description="Physical tackle that may cause the target to flinch.",
        ),
        Move(
            name="Focus Energy",
            move_type="Normal",
            category="Status",
            power=None,
            accuracy=None,
            description="Raises critical-hit ratio for a short duration.",
        ),
        Move(
            name="Growl",
            move_type="Normal",
            category="Status",
            power=None,
            accuracy=100,
            description="Lowers the target's Attack with a plaintive cry.",
        ),
    ],
    flavor=(
        "Cubone wears the skull of its deceased mother, often crying as it gazes at the moon. "
        "It protects itself with its bone club and grows into Marowak once it has accepted its loss."
    ),
)


if __name__ == "__main__":
    print(CUBONE.summary())
