# import sqlite3
# from datetime import datetime
# import requests, json
# import pandas as pd
#
# #%%
# import os
# import glob
# home_directory = os.path.expanduser('~')
# db_path = os.path.join(home_directory, 'Library','Containers',
#                        'com.apple.iBooksX','Data','Documents')
# book_parent_path = os.path.join(db_path,'BKLibrary')
# notation_parent_path = os.path.join(db_path,'AEAnnotation')
#
# book_db_path = glob.glob(os.path.join(book_parent_path, '*.sqlite'))[0]
# notation_db_path = glob.glob(os.path.join(notation_parent_path, '*.sqlite'))[0]
# print(book_db_path,notation_db_path)
# #%%
# book_title = 'Surrounded by Idiots'
# #%%
# # Define the path to the Apple Books SQLite database
# # book_db_path = '/Users/bingtinghuangfu/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-1-091020131601.sqlite'
# # notation_db_path = '/Users/bingtinghuangfu/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/AEAnnotation_v10312011_1727_local.sqlite'
# # Connect to the SQLite database
# conn_book = sqlite3.connect(book_db_path)
# conn_notation = sqlite3.connect(notation_db_path)
# # Create a cursor object
# cursor_book = conn_book.cursor()
# cursor_notation = conn_notation.cursor()
# # Example: List all tables in the database
# # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# # tables = cursor.fetchall()
# # print("Tables in the database:")
# # for table in tables:
# #     print(table[0])
# #%%
# df = pd.read_sql_query("SELECT * FROM ZBKLIBRARYASSET;", conn_book)
# #%%
# # Example: Query the data from a specific table
# # Replace 'ZBOOK' with the actual table name you are interested in
# df = pd.read_sql_query("SELECT DISTINCT ZTITLE, ZASSETID FROM ZBKLIBRARYASSET;", conn_book)
# book = dict(zip(df.ZTITLE, df.ZASSETID))
# df_book = pd.read_sql_query(f"SELECT ZTITLE, ZASSETID FROM ZBKLIBRARYASSET WHERE ZTITLE='{book_title}';",
#                             conn_book)
# # book_id = df_book.loc[0, 'ZASSETID']
# book_id = book.get(book_title)
# print(book_id)
# #%%
# df_notation = pd.read_sql_query(f'''SELECT ZANNOTATIONSELECTEDTEXT, ZANNOTATIONNOTE, ZANNOTATIONASSETID, ZANNOTATIONSTYLE,
#                                         CASE
#                                             WHEN ZANNOTATIONSTYLE=0 THEN 'Underlined'
#                                             WHEN ZANNOTATIONSTYLE=1 THEN 'Green'
#                                             WHEN ZANNOTATIONSTYLE=2 THEN 'Blue'
#                                             WHEN ZANNOTATIONSTYLE=3 THEN 'Yellow'
#                                             WHEN ZANNOTATIONSTYLE=4 THEN 'Pink'
#                                             WHEN ZANNOTATIONSTYLE=5 THEN 'Purple'
#                                         END AS STYLE,
#                                         ZANNOTATIONMODIFICATIONDATE
#                                         FROM ZAEANNOTATION WHERE ZANNOTATIONASSETID='{book_id}' AND ZANNOTATIONDELETED=0
#                                         ORDER BY ZANNOTATIONMODIFICATIONDATE DESC;''',
#                                 conn_notation)
#
# # Display the first few rows of the dataframe
# print(df_notation)
# #%%
# # custom_start_time = pd.Timestamp('2001-01-01 08:00:00')
# datediff = (datetime(2001, 1, 1) - datetime(1970, 1, 1)).days
#
# df_notation['DATE'] = df_notation['ZANNOTATIONMODIFICATIONDATE'].apply(
#     lambda x: (pd.Timestamp(x, unit='s') + pd.Timedelta(days=datediff, hours=8)).strftime('%Y-%m-%d %H:%M')
# )
# #%%
# # df_notation['ZANNOTATIONNOTE'].apply(lambda x: x if x is not None else None)
# # df_notation['ZANNOTATIONNOTE'].apply(lambda x: print(x))
# #%%
# # Close the connection
# conn_book.close()
# conn_notation.close()
#
# #%%
# # https://www.notion.so/tess-huangfu/iBook-cb64186ef4e84ffdbb2f572f5ddf3255?pvs=4
#
# #%%
# token = 'secret_wK0644opLGdosRGhvst31UzIvfwoS4yy0TCAcD92qLZ'
# pageID = 'cb64186ef4e84ffdbb2f572f5ddf3255'
#
# databaseID = "09e23355432a486cb8b079ddba99bd44"
# headers = {
#     "Authorization": "Bearer " + token,
#     "Content-Type": "application/json",
#     "Notion-Version": "2022-06-28"
# }
#
#
# #%%
# def createDatabase(headers, payload):
#     createUrl = "https://api.notion.com/v1/databases"
#     response = requests.post(createUrl, json=payload, headers=headers)
#     if response.status_code == 200:
#         # Parse the JSON response
#         response_data = response.json()
#
#         # Get the database ID
#         database_id = response_data['id']
#         print(f"Database created successfully! ID: {database_id}")
#         return database_id
#     else:
#         print(f"Failed to create database: {response.status_code}, {response.text}")
#
#
# book_payload = {
#     "parent": {
#         "type": "page_id",
#         "page_id": pageID
#     },
#     "icon": {
#         "type": "emoji",
#         "emoji": "📖"
#     },
#     "title": [{
#         'type': "text",
#         "text": {
#             "content": "Ibook List",
#         }
#     }],
#     "properties": {
#         "Name": {
#             "title": {}
#         },
#         "Description": {
#             "rich_text": {}
#         },
#         "Status": {
#             "select": {
#                 "options": [
#                     {
#                         "name": "Reading",
#                         "color": "yellow"
#                     },
#                     {
#                         "name": "Not yet",
#                         "color": "red"
#                     },
#                     {
#                         "name": "Finished",
#                         "color": "green"
#                     }
#                 ]
#             }
#         },
#         "Notes": {
#             "number": {
#                 "format": "number"
#             }
#         },
#         "Date": {
#             "date": {}
#         },
#     }
# }
# book_database = createDatabase(headers, book_payload)
# print(book_database)
# #%%
# note_payload = {
#     "parent": {
#         "type": "page_id",
#         "page_id": pageID
#     },
#     "icon": {
#         "type": "emoji",
#         "emoji": "📖"
#     },
#     "title": [{
#         'type': "text",
#         "text": {
#             "content": "Note List",
#         }
#     }],
#     "properties": {
#         "Name": {
#             "title": {}
#         },
#         "Content": {
#             "rich_text": {}
#         },
#         "Type": {
#             "select": {
#                 "options": [
#                     {
#                         "name": "Words",
#                         "color": "yellow"
#                     },
#                     {
#                         "name": "GoodSentences",
#                         "color": "red"
#                     },
#                     {
#                         "name": "Grammar",
#                         "color": "green"
#                     }
#                 ]
#             }
#         },
#         "Note": {"rich_text": {}},
#         "Date": {"date": {}},
#         "Book": {
#             "relation": {
#                 "database_id": book_database,
#                 "single_property": {}
#             }
#         },
#     }
# }
#
# note_database = createDatabase(headers, note_payload)
# print(note_database)
#
#
# #%% Response a Database
# def responseDatabase(databaseID, headers):
#     readUrl = f"https://api.notion.com/v1/databases/{databaseID}"
#     res = requests.request("GET", readUrl, headers=headers)
#     print(res.status_code)
#
#
# # responseDatabase(databaseID,headers)
# #%%
# def readDatabase(databaseID, headers):
#     readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"
#     res = requests.request("POST", readUrl, headers=headers)
#     data = res.json()
#     print(res.status_code)
#     # print(res.text)
#
#     with open('./full-properties.json', 'w', encoding='utf8') as f:
#         json.dump(data, f, ensure_ascii=False)
#     return data
#
#
# responseDatabase(databaseID, headers)
#
#
# #%%
# # Create a Page
# def createPage(headers, payload, cover_path):
#     createUrl = 'https://api.notion.com/v1/pages'
#     # data = json.dumps(newPageData)
#     # res = requests.request("POST", createUrl, headers=headers, data=payload)
#     res = requests.post(createUrl, headers=headers, json=payload)
#     print(res.status_code)
#
#
# def input_book_data(name, status, notes, date):
#     data = {
#         "Name": {
#             "title": [
#                 {"text": {"content": name}}
#             ]
#         },
#         "Status": {
#             "select": {
#                 "name": status
#             }
#         },
#         "Notes": {"number": notes},
#         "Date": {"start": date},
#     }
#     return data
#
#
# def input_payload(databaseID, cover_path, data_list):
#     book_data = input_book_data(**data_list)
#     payload = {"parent": {"database_id": databaseID},
#                "icon": {
#                    "emoji": "🥬"
#                },
#                "cover": {
#                    "external": {
#                        "url": cover_path
#                    }
#                },
#                "properties": book_data}
#
#
