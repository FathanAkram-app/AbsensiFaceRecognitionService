
import psycopg2

def execute(query: str):
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="absensi_ml",
            user="postgres",
            password="123")

        # create a cursor
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()
        
        
        # display the PostgreSQL database server version
        fetch = cur.fetchall()
        print(fetch)
        
        # close the communication with the PostgreSQL
        cur.close()
        return fetch
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error
    finally:
        if conn is not None:
            conn.close()
        
