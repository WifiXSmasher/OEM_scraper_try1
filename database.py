import sqlite3


class DB:

    @staticmethod
    def erase_database(db):
        connection = sqlite3.connect(db)
        c = connection.cursor()

        c.execute("select name from sqlite_master where type = 'TABLE';")
        tables = c.fetchall()

        for table_name in tables:
            table_name = table_name[0]  # Extract table name
            c.execute(f"DROP TABLE IF EXISTS {table_name};")
            print(f"Table '{table_name}' dropped.")

        connection.commit()
        connection.close()


    @staticmethod
    def make_table(db):
        connection = sqlite3.connect(db)
        c = connection.cursor()
        # creates a table
        command1 = """create TABLE if not exists 
            properties(product TEXT  PRIMARY KEY, advisory_ID TEXT, published_date TEXT , 
                        workaround TEXT, cisco_bug_ID TEXT, CVSS FLOAT ,link TEXT) """
        print("table crated")
        c.execute(command1)
        connection.commit()
        connection.close()

    @staticmethod
    def append(db, data, table):
        try:
            connection = sqlite3.connect(db)
            c = connection.cursor()
            data["cisco_bug_ID"] = ",".join(data["cisco_bug_ID"])
            #append the data
            comamnd1 = f"""insert into {table}(product , advisory_ID, published_date, workaround, cisco_bug_ID, CVSS, link)
                           VALUES(:product , :advisory_ID, :published_date, :workaround, :cisco_bug_ID, :CVSS, :link)"""
            c.execute(comamnd1, data)
            connection.commit()
            print("Data appended successfully")
        except sqlite3.IntegrityError as e:
            print(f"integrity error: {e} \n the data probably already in the table ")
        except Exception as e:
            print(f"an error occurred: {e}")

        finally:
            connection.close()

    @staticmethod
    def view(db, table):
        try:
            connection = sqlite3.connect(db)
            c = connection.cursor()
            command = f"select * from {table};"
            c.execute(command)
            rows = c.fetchall()

            if rows:
                for row in rows:
                    print(row)

            else:
                print("no data")


        except:
            print("something failed")
        finally:
            connection.close()




    # data = {
    #     "product": "6300 Series Embedded Services APs",
    #     "advisory_ID": "cisco-sa-12345",
    #     "published_date": "2024-12-18",
    #     "workaround": "No workaround available.",
    #     "cisco_bug_ID": "CSC12345",
    #     "CVSS": 8.2,
    #     "link": "https://example.com/advisory"
    # }
    # append("vulnerabilities.db", data, "properties")
    # erase_database("vulnerabilities.db")
    # make_table("vulnerabilities.db")
    # view("vulnerabilities.db", "properties")
