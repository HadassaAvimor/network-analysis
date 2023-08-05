import mysql.connector
from mysql.connector import Error
import DB_connection

connection = DB_connection.db_connection


def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    cursor.execute(query)
    result = cursor.fetchall()
    return result


create_technicians_table = """
CREATE TABLE Technicians (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255),
    Password VARCHAR(255)
);
"""

create_clients_table = """
CREATE TABLE Clients (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255)
);
"""

create_technician_client_connection_table = """
CREATE TABLE User_Client_Connection (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    TechnicianId INT,
    FOREIGN KEY(TechnicianId) REFERENCES Technicians(Id),
    ClientId INT,
    FOREIGN KEY(ClientId) REFERENCES Clients(Id)
);
"""

create_network_table = """
CREATE TABLE Network (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    ClientId INT,
    FOREIGN KEY(ClientId) REFERENCES Clients(Id),
    Date DATE,
    Location VARCHAR(255)
);
"""

create_device_table = """
CREATE TABLE Device (
    Type VARCHAR(255) NULL,
    Vendor VARCHAR(255),
    MACAddress VARCHAR(255),
    NetworkId INT,
    FOREIGN KEY(NetworkId) REFERENCES Network(Id)
);
"""

create_devices_connections_table = """
CREATE TABLE Devices_connections (
    SourceId VARCHAR(255),
    DestinationId VARCHAR(255),
    Protocol VARCHAR(255)
);

"""

create_Technician_permission_table = """
CREATE TABLE Technician_permission (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    TechnicianId INT,
    FOREIGN KEY(TechnicianId) REFERENCES Technicians(Id),
    ClientId INT,
    FOREIGN KEY(ClientId) REFERENCES Clients(Id)
);
"""
drop_table1 = """
DROP TABLE Devices_connections
"""

# execute_query(connection, create_technicians_table)1
# execute_query(connection, create_clients_table)1
# execute_query(connection, create_technician_client_connection_table)
# execute_query(connection, create_network_table)1
# execute_query(connection, create_device_table)
# execute_query(connection, create_devices_connections_table)
# execute_query(connection, create_Technician_permission_table)
# execute_query(connection, drop_table1)
