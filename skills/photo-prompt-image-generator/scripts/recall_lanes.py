"""Opt-in lane reservation; it changes recall ordering, never semantic judgments."""
from __future__ import annotations
from typing import Sequence


def reserve_lane_leaders(ranked_ids: Sequence[str], lanes: Sequence[Sequence[str]], budget: int) -> list[str]:
    """Reserve each eligible lane leader within the same bounded output size.

    Lane order breaks ties when the budget cannot accommodate every leader.
    No candidate outside the already eligible ranked union may enter.
    """
    ranked = list(dict.fromkeys(ranked_ids))
    eligible = set(ranked)
    reserved = []
    for lane in lanes:
        leader = next((item for item in lane if item in eligible), None)
        if leader is not None and leader not in reserved:
            reserved.append(leader)
    return list(dict.fromkeys(reserved + ranked))[:max(0, budget)]
