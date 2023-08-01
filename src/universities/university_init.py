from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class UniversityInfo:
    name: str
    full_name: str
    location: str
    # Updatable for other projects


@dataclass
class RangedAbiturientData:
    SNILS: str
    priority: int
    total_points: int
    exam_points: int
    achievements_points: int
    isOriginal: bool
    isQuota: bool
    isHigherPriority: bool
    innerPosition: int
    examResults: str  # TODO: dict if needed


class University(ABC):
    def __init__(self, name):
        self._name = name
        self._full_name = None
        self._location = None
        self._specs = None

    def set_info(self, info: UniversityInfo):
        self._name = info.name
        self._full_name = info.full_name
        self._location = info.location

    def set_specs(self, specs: dict):
        self._specs = specs

    def get_specs(self):
        return self._specs

    @abstractmethod
    def get_code_name(self) -> str:
        ...

    @abstractmethod
    def get_info(self) -> UniversityInfo:
        ...

    @abstractmethod
    def parse_spec_net(self, link) -> tuple[str, list[RangedAbiturientData]]:
        ...

    @abstractmethod
    def parse_all_specs_net(self) -> list[tuple[str, list[RangedAbiturientData]]]:
        # SPECS should be hardcoded inside files.
        ...
