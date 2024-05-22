import mysql.connector
import uuid

class DatabaseConnector:
    def __init__(self, host, port, user, password, database):
        self.table_name = None
        self.mydb = mysql.connector.connect(
            host=host,
            port= port,
            user=user,
            password=password,
            database=database
        )

    def set_table_name(self, table_name):
        self.table_name = table_name

    def get_by_uuid(self, uuid_val):
        if self.table_name is None:
            return "Set Table Name first"
        select_query = f"SELECT * FROM {self.table_name} WHERE uuid='{uuid_val}'"
        result = None
        with self.mydb.cursor() as cursor:
            cursor.execute(select_query)
            result = cursor.fetchall()
        return result

    def insert_data(self, input_path):
        if self.table_name is None:
            return "Set Table Name first"
        uuid_val = str(uuid.uuid4())
        insert_query = f"""
        INSERT INTO {self.table_name} (uuid, input_path, status)
        values ("{uuid_val}", "{input_path}", "Processing")
        """
        print(insert_query)
        with self.mydb.cursor() as cursor:
            cursor.execute(insert_query)
            self.mydb.commit()
        return uuid_val

    def update_status(self, uuid_val, status):
        if self.table_name is None:
            return "Set Table Name first"
        update_query = f"""
        UPDATE
            {self.table_name}
        SET
            status = "{status}"
        WHERE
            uuid = "{uuid_val}"
        """
        with self.mydb.cursor() as cursor:
            cursor.execute(update_query)
            self.mydb.commit()
        return True

    def update_output_path(self, uuid_val, output_path):
        if self.table_name is None:
            return "Set Table Name first"
        update_query = f"""
        UPDATE
            {self.table_name}
        SET
            output_path = "{output_path}"
        WHERE
            uuid = "{uuid_val}"
        """
        with self.mydb.cursor() as cursor:
            cursor.execute(update_query)
            self.mydb.commit()
        return True

    def update_output_status(self, uuid_val, output_path, status):
        if self.table_name is None:
            return "Set Table Name first"
        update_query = f"""
        UPDATE
            {self.table_name}
        SET
            output_path = "{output_path}",
            status = "{status}"
        WHERE
            uuid = "{uuid_val}"
        """
        with self.mydb.cursor() as cursor:
            cursor.execute(update_query)
            self.mydb.commit()
        return True



