using Mongoc
client = Mongoc.Client("mongodb://da1.eecs.utk.edu")
Mongoc.ping(client)
dbs = Mongoc.get_database_names(client)
database = client["WoC"]
Mongoc.get_collection_names(database)
# Example to access a collection
auth_metadata = database["auth_metadata.R"]
# Example to access a document
document = Mongoc.find_one(auth_metadata)
