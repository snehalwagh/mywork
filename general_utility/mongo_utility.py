from pymongo import MongoClient
from type_util import is_list, is_dict
client = MongoClient()


def create_connection():
	dbname = mongo_connection[dbname]
    input_collection = dbname[collectionname]
    return dbname, input_collection



def insert(mongo_connection, dbname, collectionname, documents):
	dbname, input_collection = create_connection(mongo_connection, dbname, collectionname)

    if is_dict(documents):
        input_collection.insert_one(documents)
        return True
    elif is_list(documents):
        for document in documents:
            input_collection.insert_one(document)


def update(mongo_connection, dbname, collectionname, find_query=None, update_query):
	dbname, input_collection = create_connection(mongo_connection, dbname, collectionname)

	if find_query:
		input_collection.find(find_query, update_query)




def remove(mongo_connection, dbname, collectionname, documents):
    dbname, input_collection = create_connection(mongo_connection, dbname, collectionname)

    if is_dict(documents):
        input_collection.remove(documents)
        return True
    elif is_list(documents):
        for document in documents:
            input_collection.remove(document)


if __name__ == "__main__":
    insert(client, 'test', 'tes_congresses', {'name': 'snehal'})
    remove(client, 'test', 'tes_congresses', {'name': 'snehal'})
    update(client, 'test', 'tes_congresses', {'name': 'snehal'}, {'$rename':{'name':'SNEHAL'}})
