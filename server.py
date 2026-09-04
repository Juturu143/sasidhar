import mysql.connector
from mysql.connector import Error
from datetime import datetime


def manage_numberplate_db(numberplate):
    """
    Connect to MySQL/XAMPP, create the database and table if needed,
    and save the detected number plate with date and time.
    """

    # ============================================================
    # DATABASE CONFIGURATION
    # ============================================================

    host = "127.0.0.1"
    user = "root"
    password = ""
    database = "numberplate"
    port = 3306

    connection = None
    cursor = None

    try:
        # ========================================================
        # VALIDATE NUMBER PLATE
        # ========================================================

        if not numberplate:
            print("Empty number plate. Nothing to save.")
            return

        numberplate = str(numberplate).strip()

        if not numberplate:
            print("Invalid number plate. Nothing to save.")
            return

        # ========================================================
        # CONNECT TO MYSQL SERVER
        # ========================================================

        print("Connecting to MySQL server...")

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )

        if not connection.is_connected():
            print("Could not connect to MySQL server.")
            return

        print("MySQL connection successful.")

        cursor = connection.cursor()

        # ========================================================
        # CREATE DATABASE IF IT DOES NOT EXIST
        # ========================================================

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{database}`"
        )

        # ========================================================
        # SELECT DATABASE
        # ========================================================

        cursor.execute(
            f"USE `{database}`"
        )

        # ========================================================
        # CREATE TABLE IF IT DOES NOT EXIST
        # ========================================================

        create_table_query = """
        CREATE TABLE IF NOT EXISTS numberplate (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numberplate VARCHAR(50) NOT NULL,
            entry_date DATE NOT NULL,
            entry_time TIME NOT NULL
        )
        """

        cursor.execute(create_table_query)
        connection.commit()

        # ========================================================
        # GET CURRENT DATE AND TIME
        # ========================================================

        current_datetime = datetime.now()

        current_date = current_datetime.date()
        current_time = current_datetime.time()

        # ========================================================
        # INSERT NUMBER PLATE
        # ========================================================

        insert_query = """
        INSERT INTO numberplate
        (numberplate, entry_date, entry_time)
        VALUES (%s, %s, %s)
        """

        data = (
            numberplate,
            current_date,
            current_time
        )

        cursor.execute(insert_query, data)
        connection.commit()

        print(
            f"Number plate '{numberplate}' "
            f"saved successfully."
        )
        print(
            f"Date: {current_date} | "
            f"Time: {current_time}"
        )

    except Error as e:
        print(f"MySQL Error: {e}")

    except Exception as e:
        print(f"Unexpected Error: {e}")

    finally:
        # ========================================================
        # CLOSE CURSOR
        # ========================================================

        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass

        # ========================================================
        # CLOSE DATABASE CONNECTION
        # ========================================================

        if connection is not None:
            try:
                if connection.is_connected():
                    connection.close()
                    print("MySQL connection closed.")
            except Exception:
                pass
