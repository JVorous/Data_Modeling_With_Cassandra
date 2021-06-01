# Import Python packages
from cassandra.cluster import Cluster
import os
import glob
import csv
from prettytable import PrettyTable
from cql_queries import create_table_queries, drop_table_queries, insert_data_queries

def process_files():
    """
    Description:
        processes individual data .csv files into new .csv with formatting
        specific for Cassanda import

        new file output to current working directory

    Arguments:
        None

    Returns:
        relative path to new file

    """
    output_file = 'event_datafile_new.csv'

    # Get your current folder and subfolder event data
    filepath = os.getcwd() + '\event_data'

    # Create a for loop to create a list of files and collect each filepath
    for root, dirs, files in os.walk(filepath):
        # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root, '*'))

    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = []

    # for every filepath in the file path list
    for f in file_path_list:

        # reading csv file
        with open(f, 'r', encoding='utf8', newline='') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            next(csvreader)

            # extracting each data row one by one and append it
            for line in csvreader:
                full_data_rows_list.append(line)

    # creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
    # Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open(output_file, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist', 'firstName', 'gender', 'itemInSession', 'lastName', 'length',
                         'level', 'location', 'sessionId', 'song', 'userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))

    return output_file

def create_tables(session):
    """
    Description:
        Creates each table using the queries in `create_table_queries` list.

    Arguments:
        session: current cassandra session

    Returns:
        None

    """

    for query in create_table_queries:
        try:
            session.execute(query)
        except Exception as e:
            print("problem with query: {}".format(e))

def drop_tables(session):
    """
    Description:
        Drops each table using the queries in `create_table_queries` list.

    Arguments:
        session: current cassandra session

    Returns:
        None

    """
    for query in drop_table_queries:
        try:
            rows = session.execute(query)
        except Exception as e:
            print(e)


def populate_tables(session, file):
    """
       Description:
           processes source CSV file into Cassandra tables

       Arguments:
           session: current cassandra session
           file: source file (csv)

       Returns:
           None

       """
    with open(file, encoding='utf8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip header

        for line in csv_reader:
            for query, dest in insert_data_queries:
                if dest == 'session_library':
                    session.execute(query, (int(line[8]), int(line[3]), line[0], line[9], float(line[5])))
                elif dest == 'user_song_library':
                    session.execute(query, (line[9], int(line[10]), line[1], line[4]))
                else:
                    session.execute(query, (int(line[10]), int(line[8]), int(line[3]), line[1], line[4],
                                            line[0], line[8]))


def run_queries(session):
    """
        Description:
            runs queries against Cassandra table(s) to answer the following questions:

            new file output to current working directory

        Arguments:
            session: the current cassandra session

        Returns:
            None

        """

    print('Query #1: list the artist name, song title, and song length where session_id = 38 and item_in_session = 4')
    query = "SELECT artist_name, song_title, song_length FROM session_library " \
            "WHERE session_id = 338 and item_in_session = 4"

    try:
        rows = session.execute(query)
        t = PrettyTable(['artist_name', 'song_title', 'song_length'])
        for row in rows:
            t.add_row([row.artist_name, row.song_title, row.song_length])
        print(t)
        print('\n')
    except Exception as e:
        print(e)

    print('Query #2: list the artist name, song title, item in session, user first_name, and user last_name '
          'where user_id = 10 and session_id = 182')

    query = "SELECT artist_name, song_title, item_in_session, first_name, last_name FROM user_session_library " \
              "WHERE user_id = 10 and session_id = 182"

    try:
        rows = session.execute(query)
        t = PrettyTable(['artist_name', 'song_title', 'item_in_session', 'first_name', 'last_name'])
        for row in rows:
            t.add_row([row.artist_name, row.song_title, row.item_in_session, row.first_name, row.last_name])
        print(t)
        print('\n')
    except Exception as e:
        print(e)

    print('Query #3: List all of the users (first and last name) who listened to the '
          'song "All Hands Against His Own"')

    query = "SELECT first_name, last_name FROM user_song_library WHERE song_title = 'All Hands Against His Own'"

    try:
        rows = session.execute(query)
        t =PrettyTable(['first_name', 'last_name'])
        for row in rows:
            t.add_row([row.first_name, row.last_name])
        print(t)
    except Exception as e:
        print(e)

def main():
    """
    Description:
        Main function. calls for file processing and establishes a connection and keyspace for Cassandra
        then populates, queries, and drops relavent tables

        new file output to current working directory

    Arguments:
        None

    Returns:
        None

    """
    #process data files into usable source .csv
    source_csv = process_files()


    # To establish connection and begin executing queries, need a session
    cluster = Cluster()
    session = cluster.connect()

    #Create Keyspace
    try:
        session.execute("""
        CREATE KEYSPACE IF NOT EXISTS udacity
        WITH REPLICATION = 
        { 'class' : 'SimpleStrategy', 'replication_factor' : 1}
        """)
    except Exception as e:
        print(e)

    #set Keyspace
    try:
        session.set_keyspace('udacity')
    except Exception as e:
        print(e)

    #Create tables
    create_tables(session)

    #populate tables
    print('Populating tables. This may take a while...')
    populate_tables(session, source_csv)


    # query tables
    run_queries(session)

    #drop tables
    drop_tables(session)

    #close out connection
    session.shutdown()
    cluster.shutdown()

if __name__ == '__main__':
    main()
