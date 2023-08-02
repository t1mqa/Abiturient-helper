import src.utils.requester as requester
import src.utils.bsParser as bsParser

from src.universities.university_init import University
from src.universities.uni_dataclasses import UniversityInfo, RangedAbiturientData
from src.universities.GUAP.specs import SPECS


class GUAP(University):
    def __init__(self):
        super().__init__("ГУАП")
        self.set_specs(SPECS)

    def get_info(self) -> UniversityInfo:
        return UniversityInfo("ГУАП",
                              "Санкт-Петербургский Государственный Университет Аэрокосмического Приборостроения",
                              "Санкт-Петербург")

    def get_code_name(self) -> str:
        return "GUAP"

    def parse_spec_net(self, link) -> tuple[str, list[RangedAbiturientData]]:
        raw_data = requester.request_it(link)
        table = bsParser.get_table_guap(raw_data.content)
        name = bsParser.get_table_name_guap(raw_data.content)
        normalized_table = [RangedAbiturientData(**x) for x in table]
        return name, normalized_table


a = GUAP()
print(a.parse_all_specs_db()[3])
