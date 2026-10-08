from __future__ import annotations

from dataclasses import dataclass

from forge.controller.capability import CapabilityReport


@dataclass(frozen=True)
class ResearchPriority:
    capability: str
    score: float
    rationale: str


class CapabilityResearchController:
    """Selects what to investigate next; it does not autonomously edit the system."""

    def prioritize(self, report: CapabilityReport, *, limit: int = 3) -> list[ResearchPriority]:
        priorities = []
        for item in report.bottlenecks(limit=limit):
            priorities.append(
                ResearchPriority(
                    capability=item.name,
                    score=item.score,
                    rationale=(
                        f"score={item.score:.3f}, failure_rate={item.failure_rate:.3f}, "
                        f"impact={item.impact:.2f}; design a falsifiable experiment"
                    ),
                )
            )
        return priorities
