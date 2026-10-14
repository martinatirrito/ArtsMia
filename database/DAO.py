from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():

    @staticmethod
    def getAllNodes():
        try:
            conn = DBConnect.get_connection()  # me lo scrivo uguale a sopra nell'import
            cursor = conn.cursor(dictionary=True)  # leggere il database
            # dictionary perche ogni riga del cursore mi crea un dizionario
        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """select *
                    from objects o"""
        cursor.execute(query)

        for row in cursor:
            result.append(ArtObject(**row))
            # result.append(ArtObject(object_id = row ["object_id"], ...))  faccio tutto con **row sopra
            # nome colonna DTO = nome colonna DAO
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getEdgePeso(v1, v2):
        #archi collegano due oggetti se sono stati esposti contemporaneamente in un exhibition,
        #peso degli archi è il numero di exhibition in cui tali oggetti sono stati esposti contemporaneamente

        #--> trovo coppia di oggetti che è stata mostrata in una stessa exhibition

        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        #dati due object id trovo il loro peso
        query = """select eo1.object_id as o1, eo2.object_id  as o2, count(*) as peso
                    from exhibition_objects eo1, exhibition_objects eo2 
                    where eo1.exhibition_id = eo2.exhibition_id 
                    and eo1.object_id < eo2.object_id  
                    and eo1.object_id = %s and eo2.object_id = %s
                    group by eo1.object_id, eo2.object_id """
        #SE TOGLIAMO IL FILTRO E TOLGO %S MI EVITO DI FARE IL DOPPIO CICLO FOR NEL MODEL E STAMPO PIU VELOCEMENTE

        cursor.execute(query, (v1.object_id, v2.object_id)) #passo la tupla dei due valori scritti sopra

        for row in cursor:
            result.append(row["peso"])
            #facendo cosi potrebbe essere che peso non esiste tra due oggetti
            #quindi scrivo if sotto


        cursor.close()
        conn.close()

        if len(result) == 0:
            return None

        return result

    @staticmethod
    def getAllEdges(idMapAO):
        try:
            conn = DBConnect.get_connection()  # me lo scrivo uguale a sopra nell'import
            cursor = conn.cursor(dictionary=True)  # leggere il database
            # dictionary perche ogni riga del cursore mi crea un dizionario
        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []
        #selezione coppie id oggetto col suo peso
        query = """select eo1.object_id as o1, eo2.object_id  as o2, count(*) as peso
                    from exhibition_objects eo1, exhibition_objects eo2 
                    where eo1.exhibition_id = eo2.exhibition_id 
                    and eo1.object_id < eo2.object_id  
                    group by eo1.object_id, eo2.object_id 
                    order by peso desc"""
        cursor.execute(query)

        for row in cursor:
            #result.append((o1, 02, peso))
            result.append(Arco(idMapAO[row["o1"]], idMapAO[row["o2"]], row["peso"]))
            #mi sono creata oggetto arco nel model

        cursor.close()
        conn.close()
        return result

