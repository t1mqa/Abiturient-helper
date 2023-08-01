import requests
from bs4 import BeautifulSoup


def get_table_name(table: requests.Response.content) -> str:
    soup = BeautifulSoup(table, 'html.parser')
    name_elem = soup.select_one("body > main > div:nth-child(3) > div:nth-child(6) > h3")
    name = name_elem.text
    return name


def get_table(table: requests.Response.content) -> list:
    soup = BeautifulSoup(table, 'html.parser')
    table_element = soup.select_one("body > main > div:nth-child(3) > div:nth-child(9) > div.table-responsive")
    table = table_element.find('table', class_='table-hover')
    data = []
    for row in table.select('tbody tr'):
        cells = row.select('td')
        row_data = {
            'SNILS': cells[1].text.strip(),
            'priority': int(cells[2].text.strip()) if cells[2].text.strip().isnumeric() else 1,
            'total_points': int(cells[3].text.strip()) if cells[3].text.strip().isnumeric() else 0,
            'exam_points': int(cells[4].text.strip()) if cells[4].text.strip().isnumeric() else 0,
            'achievements_points': int(cells[5].text.strip()) if cells[5].text.strip().isnumeric() else 0,
            'isOriginal': True if cells[6].text.strip() == 'Да' else False,
            'isQuota': True if cells[7].text.strip() == 'Да' else False,
            'isHigherPriority': True if cells[8].text.strip() == 'Да' else False,
            'innerPosition': int(cells[9].text.strip()) if cells[9].text.strip().isnumeric() else 0,
            'examResults': cells[10].text.strip(),
        }
        data.append(row_data)
    return data
