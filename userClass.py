import psycopg2
import random
import threading
import time
from db_connect import execute_get_sql_query, execute_set_sql_query


def change_language(message, language):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("UPDATE users SET language='%s' where id='%s'" % (
        str(language), str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()


def generate_and_save_code(user_id):
    verification_code = random.randint(1000, 9999)
    sql_query = "UPDATE users_info SET verif_code = %s WHERE id = %s"
    params = (str(verification_code), user_id)
    execute_set_sql_query(sql_query, params)
    return verification_code


# Функция для получения сохраненного кода из БД
def get_saved_verification_code(user_id):
    sql_query = "SELECT verif_code FROM users_info WHERE id = %s"
    params = (user_id,)
    code = execute_get_sql_query(sql_query, params)[0][0]
    return code

def check_registration_message_in_history(user_id):
    """
    Проверяет, вводил ли пользователь команду '💸Регистрация на обучение "Финансовая грамотность"'
    среди последних четырех записей в столбце commands_name таблицы commands_history.

    :param user_id: ID пользователя.
    :return: True, если команда найдена среди последних четырех сообщений, иначе False.
    """
    sql_query = """
    SELECT EXISTS(
        SELECT 1 
        FROM (
            SELECT commands_name 
            FROM commands_history 
            WHERE id = %s
            ORDER BY date DESC  -- Сортировка по дате
            LIMIT 2
        ) AS recent_commands
        WHERE recent_commands.commands_name LIKE '💸Регистрация на обучение "Финансовая грамотность"'
    )
    """
    params = (str(user_id),)
    result = execute_get_sql_query(sql_query, params)

    # Проверяем, найден ли хотя бы один результат
    return result is not None and result[0][0]



def delete_registration_message_in_history(user_id):
    sql_query = """
    DELETE * 
    FROM commands_history 
    WHERE id = %s 
    AND commands_name LIKE '💸Регистрация на обучение "Финансовая грамотность"'
    """
    params = (str(user_id),)
    result = execute_set_sql_query(sql_query, params)

    # Проверяем, найден ли хотя бы один результат
    return result is not None and result[0][0]

def check_registration_message_in_history_decl(user_id):
    """
    Проверяет, вводил ли пользователь когда-либо текст '📄Подтверждение сдачи декларации'
    в таблице commands_history.

    :param user_id: ID пользователя.
    :return: True, если текст найден в любом из сообщений пользователя, иначе False.
    """
    sql_query = """
        SELECT EXISTS(
            SELECT 1 
            FROM (
                SELECT commands_name 
                FROM commands_history 
                WHERE id = %s
                ORDER BY date DESC  -- Сортировка по дате
                LIMIT 2
            ) AS recent_commands
            WHERE recent_commands.commands_name LIKE '📄Подтверждение сдачи декларации'
        )
        """
    params = (str(user_id),)
    result = execute_get_sql_query(sql_query, params)

    # Проверяем, найден ли хотя бы один результат
    if result is not None and result[0][0]:
        return True
    return False

def check_registration_message_in_history_decl_kaz(user_id):
    """
    Проверяет, вводил ли пользователь когда-либо текст '📄Подтверждение сдачи декларации'
    в таблице commands_history.

    :param user_id: ID пользователя.
    :return: True, если текст найден в любом из сообщений пользователя, иначе False.
    """
    sql_query = """
        SELECT EXISTS(
            SELECT 1 
            FROM (
                SELECT commands_name 
                FROM commands_history 
                WHERE id = %s
                ORDER BY date DESC  -- Сортировка по дате
                LIMIT 2
            ) AS recent_commands
            WHERE recent_commands.commands_name LIKE '📄Декларацияны тапсыруды растау'
        )
        """
    params = (str(user_id),)
    result = execute_get_sql_query(sql_query, params)

    # Проверяем, найден ли хотя бы один результат
    if result is not None and result[0][0]:
        return True
    return False

verification_timers = {}

def get_user_verification_status(user_id):
    """
    Проверяет статус пользователя 'is_verified_decl' в базе данных.

    :param user_id: ID пользователя.
    :return: True, если пользователь верифицирован (is_verified_decl = True), иначе False.
    """
    params = (str(user_id),)
    sql_query = 'SELECT is_verified_decl FROM users WHERE id = %s'
    result = execute_get_sql_query(sql_query, params)

    # Возвращаем статус верификации, если пользователь найден, иначе False
    if result and isinstance(result[0][0], bool):
        return result[0][0]
    return False

def get_user_verification_status_reg(user_id):
    """
    Проверяет статус пользователя 'is_verified' в базе данных.

    :param user_id: ID пользователя.
    :return: True, если пользователь верифицирован (is_verified = True), иначе False.
    """
    params = (str(user_id),)
    sql_query = 'SELECT is_verified FROM users WHERE id = %s'
    result = execute_get_sql_query(sql_query, params)

    # Возвращаем статус верификации, если пользователь найден, иначе False
    if result is None:
        return False
    elif result[0][0] is True:
        return True
    else:
        return False

def check_if_registered(user_id):
    params = (str(user_id),)
    # SQL-запрос для проверки наличия записи в таблице financial_literacy по user_id
    sql_query = "SELECT EXISTS(SELECT 1 FROM financial_literacy WHERE user_id = %s)"

    # Выполнение запроса
    result = execute_get_sql_query(sql_query, params)

    # Возвращаем True, если пользователь зарегистрирован, иначе False
    if result is not None and result[0][0]:
        return True
    return False

def check_if_registered_reg(user_id):
    params = (str(user_id),)
    # SQL-запрос для проверки наличия записи в таблице financial_literacy по user_id
    sql_query = "SELECT is_verified FROM users WHERE id = %s"

    # Выполнение запроса
    result = execute_get_sql_query(sql_query, params)

    # Возвращаем True, если пользователь зарегистрирован, иначе False
    if result is not None and result[0][0]:
        return True
    return False

def get_users_id():
    sql_query = 'SELECT id FROM users'
    users = execute_get_sql_query(sql_query)
    users_array = []
    for user in users:
        users_array.append(str(user[0]))
    return users_array

def set_firstname(message, firstname):
    sql_query = 'UPDATE users SET firstname = %s WHERE id=%s'
    params = (firstname, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def set_lastname(message, lastname):
    sql_query = 'UPDATE users SET lastname = %s WHERE id=%s'
    params = (lastname, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_firstname(message):
    sql_query = 'SELECT firstname FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    name = execute_get_sql_query(sql_query, params)[0][0]
    return name


def get_lastname(message):
    sql_query = 'SELECT lastname FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    name = str(execute_get_sql_query(sql_query, params)[0][0])
    return name


def get_language(message):
    sql_query = 'SELECT language FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    name = str(execute_get_sql_query(sql_query, params)[0][0])
    return name


def set_table_number(message, table_num):
    sql_query = 'UPDATE users SET table_number =%s WHERE id=%s'
    params = (table_num, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_table_number(message):
    sql_query = 'SELECT table_number FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def get_phone_number(message):
    sql_query = 'SELECT phone_number FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def get_email(message):
    sql_query = 'SELECT email FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_email_for_verif(user_id):
    sql_query = 'SELECT email FROM users WHERE id=%s'
    params = (str(user_id),)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_verif_decl_status(user_id):
    sql_query = 'SELECT verif_decl FROM users WHERE id=%s'
    params = (str(user_id),)
    return execute_get_sql_query(sql_query, params)[0][0]

def set_phone_number(message, phone_number):
    sql_query = 'UPDATE users SET phone_number = %s WHERE id=%s'
    params = (phone_number, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)

def set_email(message, email):
    sql_query = 'UPDATE users SET email=%s WHERE id=%s'
    params = (email, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_branch(user_id):
    sql_query = 'SELECT users.branch FROM users WHERE id=%s'
    params = (str(user_id),)  # Make sure to create a tuple
    branch = execute_get_sql_query(sql_query, params)
    return branch[0][0] if branch else None


def set_branch(user_id, branch):
    sql_query = 'UPDATE users SET branch=%s WHERE id=%s'
    params = (str(branch), str(user_id),)
    execute_set_sql_query(sql_query, params)


def delete_user(message):
    user_id = str(message.chat.id)

    # Подключение к базе данных
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()

    try:
        # Удаление пользователя из таблицы users
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

        # Подтверждение транзакции
        conn.commit()

    except Exception as e:
        # Откат транзакции в случае ошибки
        conn.rollback()
        print(f"Ошибка при удалении пользователя: {e}")

    finally:
        # Закрытие курсора и соединения
        cur.close()
        conn.close()

def delete_participation(message):
    user_id = str(message.chat.id)

    # Подключение к базе данных
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()

    try:
        # Удаление пользователя из таблицы financial_literacy
        cur.execute("DELETE FROM financial_literacy WHERE user_id = %s", (user_id,))

        # Подтверждение транзакции
        conn.commit()

    except Exception as e:
        # Откат транзакции в случае ошибки
        conn.rollback()
        print(f"Ошибка при удалении пользователя: {e}")

    finally:
        # Закрытие курсора и соединения
        cur.close()
        conn.close()

def delete_users_info():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("DROP TABLE users_info")
    conn.commit()
    cur.close()
    conn.close()

def alter_users():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("ALTER TABLE users ADD COLUMN is_verified_decl BOOLEAN DEFAULT FALSE")
    conn.commit()
    cur.close()
    conn.close()

def alter_users_reg():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE")
    conn.commit()
    cur.close()
    conn.close()

def get_user(user_id):
    sql_query = "SELECT * FROM users where id = %s"
    params = (str(user_id),)
    return execute_get_sql_query(sql_query, params)[0]