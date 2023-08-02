import psycopg2
from psycopg2.extensions import connection, cursor
from databases.db_config import host, user, password, db_name
from src.universities.uni_dataclasses import RangedAbiturientData
from src.utils.other_utils import snils_normalize


def get_connection() -> connection | None:
    try:
        conn = psycopg2.connect(host=host,
                                user=user,
                                password=password,
                                dbname=db_name)
        conn.autocommit = True
    except psycopg2.OperationalError as error:
        print("Error while connecting to PostgreSQL:", error)
        return None
    return conn


def create_spec_table(spec: str):
    conn: connection = get_connection()
    if conn is not None:
        cur: cursor = conn.cursor()
        spec = spec.replace(".", "_")
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {spec} (
                    SNILS VARCHAR,
                    priority INTEGER,
                    total_points INTEGER,
                    exam_points INTEGER,
                    achievements_points INTEGER,
                    isOriginal BOOLEAN,
                    isQuota BOOLEAN,
                    isHigherPriority BOOLEAN,
                    innerPosition INTEGER,
                    examResults VARCHAR
                    );
                     """)
    conn.close()


def fill_spec_table(spec: str, data: list[RangedAbiturientData]):
    conn: connection = get_connection()
    if conn is not None:
        cur: cursor = conn.cursor()
        spec = spec.replace(".", "_")
        insert_statement = f"""
                INSERT INTO {spec} (
                    SNILS,
                    priority,
                    total_points,
                    exam_points,
                    achievements_points,
                    isOriginal,
                    isQuota,
                    isHigherPriority,
                    innerPosition,
                    examResults
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
        data_tuples = [(snils_normalize(d.SNILS), d.priority, d.total_points, d.exam_points, d.achievements_points,
                        d.isOriginal, d.isQuota, d.isHigherPriority, d.innerPosition, d.examResults)
                       for d in data]
        try:
            cur.executemany(insert_statement, data_tuples)
            print(f"Filled for {spec}")
        except Exception as e:
            conn.rollback()
            print("An error occurred:", e)
        finally:
            cur.close()
            conn.close()


def get_spec(spec_db_code: str) -> list[RangedAbiturientData]:
    conn: connection = get_connection()
    if conn is not None:
        cur: cursor = conn.cursor()
        cur.execute(f"""SELECT * FROM {spec_db_code};""")
        rows = cur.fetchall()
        ranged_abiturients = []
        for row in rows:
            ranged_abiturient = RangedAbiturientData(*row)
            ranged_abiturients.append(ranged_abiturient)
        return ranged_abiturients


def create_users_table():
    conn: connection = get_connection()
    if conn is not None:
        cur: cursor = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS tgUsers (
                        tgId VARCHAR,
                        status VARCHAR,
                        SNILS VARCHAR,
                        universities VARCHAR[]
                        );
                         """)
    conn.close()


def create_user(tg_user) -> bool:
    conn: connection = get_connection()
    if conn is not None:
        cur: cursor = conn.cursor()
        # First, lets check that user not exists
        cur.execute(f"""SELECT COUNT(*) FROM tgUsers WHERE tgId = (%s)""", (tg_user.tgId, ))
        if cur.fetchone()[0] > 0:
            return False
        cur.execute(f"""
            INSERT INTO tgUsers (tgId, status, SNILS, universities)
            VALUES (%s, %s, %s, %s)
        """, (tg_user.tgId, "waiting SNILS", "", []))
    conn.close()
    return True
