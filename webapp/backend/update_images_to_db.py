import sqlite3
from sqlite3 import Error

db_file = "aiserver.db"
images_table = "Container"
ports_table = "ContainerPort"

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def delete_all(conn,table):
    """
    Delete all rows in the given table
    :param conn: Connection to the SQLite database
    :param table: table to delete
    :return:
    """
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def add_row_to_images(conn, docker_image_name, name_to_show_in_frontend, description):
    """
    Create a new task
    :param conn:
    :param docker_image_name:
    :param name_to_show_in_frontend:
    :param description:
    :return:
    """

    sql = f''' insert into Container (public, imageName, name, description) values (?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, ("true", docker_image_name, name_to_show_in_frontend,description))
    conn.commit()

    return cur.lastrowid

def add_row_to_ports(conn, container_id, service_name, port):
    """
    Create a new task
    :param conn:
    :param container_id:
    :param service_name:
    :param port:
    :return:
    """

    sql = f''' insert into ContainerPort (containerId, serviceName, port) values (?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql, (container_id, service_name, port))
    conn.commit()

    return cur.lastrowid

def main():
    # create a database connection
    conn = create_connection(db_file)
    with conn:
        delete_all(conn,images_table)
        delete_all(conn,ports_table)

        f = open('images_to_db.txt', 'r')
        lines = f.readlines()
        for count, line in enumerate(lines):
            x = line.split(",")
            x.pop(-1)
            add_row_to_images(conn,x.pop(0),x.pop(0),x.pop(0))
            for _ in range(len(x)//2):
                add_row_to_ports(conn,count+1,x.pop(0),x.pop(0))

if __name__ == '__main__':
    main()