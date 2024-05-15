import mysql.connector
import configparser
import os
from argparse import ArgumentParser

def reset_database(config):
    host = config['database']['host']
    database_name = config['database']['database_name'] 
    password = config['database']['password']
    port = config['database']['port']

   
    try: 
        db = mysql.connector.connect(
            host=host,
            user="root",
            password=password,
            port=port
        )
        cursor = db.cursor()

        # Drop existing database if it exists
        cursor.execute("DROP DATABASE IF EXISTS {}".format(database_name))

        cursor.execute("CREATE DATABASE {}".format(database_name))
        cursor.execute("USE {}".format(database_name))
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                uuid VARCHAR(36) UNIQUE,
                date DATETIME
            )
        """)

        print("Database '{}' reset successfully!".format(database_name))
        cursor.close()
        db.close()

    except mysql.connector.Error as e:
        print("An error occurred:", e)


def create_config(config_file, host, database_name, password, port):
    config = configparser.ConfigParser()
    config['database'] = {
        'host': host,
        'database_name': database_name,
        'password': password,
        'port': port
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


if __name__ == "__main__":

    config_file = "dbconfig.ini"

    while True:
        if os.path.exists(config_file):
            print("Use current config? (yes/no): ")
            x = input()
            if x.lower() == "yes":
                config = read_config(config_file)
                break
            elif x.lower() == "no":
                print("Database name:")
                database_name = input()
                print("Password:")
                password = input()
                print("Host:")
                host = input()
                print("Port:")
                port = input()

                create_config(config_file, host, database_name, password, port)
                config = read_config(config_file)
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        else:
            print("Database name:")
            database_name = input()
            print("Password:")
            password = input()
            print("Host:")
            host = input()

            create_config(config_file, host, database_name, password)
            config = read_config(config_file)
            break


    reset_database(config)
