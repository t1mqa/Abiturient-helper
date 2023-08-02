from dataclasses import dataclass


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