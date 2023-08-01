from typing import Tuple, List

import src.utils.requester as requester
import src.utils.bsParser as bsParser

from src.universities.university_init import University, UniversityInfo, RangedAbiturientData
from src.universities.GUAP.specs import SPECS


class GUAP(University):
    def __init__(self):
        super().__init__("ГУАП")
        self.set_specs(SPECS)

    def get_info(self) -> UniversityInfo:
        return UniversityInfo("ГУАП",
                              "Санкт-Петербургский Государственный Университет Аэрокосмического Приборостроения",
                              "Санкт-Петербург")

    def parse_spec_net(self, link) -> tuple[str, list[RangedAbiturientData]]:
        raw_data = requester.request_it(link)
        table = bsParser.get_table(raw_data.content)
        name = bsParser.get_table_name(raw_data.content)
        normalized_table = [RangedAbiturientData(**x) for x in table]
        return name, normalized_table

    def parse_all_specs_net(self, specs: dict = SPECS) -> list[tuple[str, list[RangedAbiturientData]]]:
        data = []
        for _, link in specs.items():
            # I can replace items with values
            data.append(self.parse_spec_net(link))
        return data


a = GUAP()
print(a.parse_all_specs_net())
