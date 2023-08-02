from abc import ABC, abstractmethod
from databases.db_init import get_spec
from src.universities.uni_dataclasses import UniversityInfo, RangedAbiturientData


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

    def parse_spec_db(self, spec_code: str) -> list[RangedAbiturientData]:
        spec_code = spec_code.replace(".", "_")
        db_name = f"{self.get_code_name()}_{spec_code}"
        return get_spec(db_name)

    def parse_all_specs_db(self) -> list[str, list[RangedAbiturientData]]:
        data: list = []
        for name, _ in self._specs.items():
            spec_code = name.replace(".", "_")
            db_name = f"{self.get_code_name()}_{spec_code}"
            print(db_name)
            data.append([name, get_spec(db_name)])
        return data

    def parse_all_specs_net(self) -> list[tuple[str, list[RangedAbiturientData]]]:
        data = []
        for _, link in self._specs.items():
            data.append(self.parse_spec_net(link))
        return data

    @abstractmethod
    def get_code_name(self) -> str:
        ...

    @abstractmethod
    def get_info(self) -> UniversityInfo:
        ...

    @abstractmethod
    def parse_spec_net(self, link) -> tuple[str, list[RangedAbiturientData]]:
        ...
