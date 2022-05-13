from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Result:
    outcome: bool
    wireflies: int
    flips: int
    sequence: str


@dataclass
class Data:
    n: int
    flips: int
    opp_hp: int
    wf_data: Dict = field(default_factory=dict)
    flip_data: Dict = field(default_factory=dict)
    success: int = 0
    last_wf: int = 0
    last_flips: int = 0
    last_sequence: str = ""
    max_wf: int = 0
    max_flips: int = 0
    max_sequence: str = ""

    def parse(self, result: Result):
        self.success += 1
        self.last_wf = result.wireflies
        self.last_flips = result.flips
        self.last_sequence = result.sequence
        try:
            self.wf_data[result.wireflies] += 1
        except KeyError:
            self.wf_data.update({result.wireflies: 1})
        try:
            self.flip_data[result.flips] += 1
        except KeyError:
            self.flip_data.update({result.flips: 1})
        if self.max_wf < result.wireflies:
            self.max_wf = result.wireflies
        if self.max_flips < result.flips:
            self.max_flips = result.flips
            self.max_sequence = result.sequence
