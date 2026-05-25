from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    #metodo per estrarre i nodi, tc solo aeroporto id di chi ha un numero compagnie > %s
    @staticmethod
    def getNodi(numeroNodi):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.ID , a.IATA_CODE, count(distinct(f.AIRLINE_ID)) as numeroCompagnieAeroporto
        from flights f, airports a 
        where a.ID = f.DESTINATION_AIRPORT_ID or a.ID = f.ORIGIN_AIRPORT_ID 
        group by a.ID, a.IATA_CODE 
        having count(distinct(f.AIRLINE_ID)) >= %s"""

        cursor.execute(query, (numeroNodi,))

        for row in cursor:
            result.append(row["ID"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchiPesati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID as partenza, f.DESTINATION_AIRPORT_ID as arrivo, count(*) as peso
FROM flights f 
group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["partenza"], row["arrivo"], row["peso"]))

        cursor.close()
        conn.close()
        return result
