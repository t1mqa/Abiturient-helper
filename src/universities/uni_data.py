from src.universities.GUAP.guap_spb import GUAP

guap = GUAP()

AVAILABLE_UNIVERSITIES = [guap]


def get_all_universities_positions(snils):
    parsed_data = {}
    for uni in AVAILABLE_UNIVERSITIES:
        uni_data = {}
        for spec in uni.get_specs():
            spec = spec.replace('.', '_')
            name = uni.get_code_name()
            spec_db = f"{name}_{spec}"
            data = uni.get_place_by_snils(snils, spec_db)
            if data is not None:
                uni_data[spec_db] = [data[0], data[1], data[5], data[8]]
        parsed_data[uni.get_code_name()] = uni_data
    print(parsed_data)
    return parsed_data

