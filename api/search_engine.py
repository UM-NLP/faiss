import faiss
import numpy as np
import mysql.connector
from vector_encoding  import encoder765
from google.cloud import storage
initialized=False
import yaml
from pathlib import Path
def initiate_765():
    global initialized
    global FAISS_MODEL765
    yaml_dict = yaml.safe_load(Path("setting.yml").read_text())
    FAISS_MODEL765=yaml_dict["FAISS_MODEL765"]
    global host
    host=yaml_dict["mysql_host"]
    global user
    user=yaml_dict["mysql_user"]
    global password
    password=yaml_dict["mysql_password"]
    global SIMILAR_THRESHOLD
    SIMILAR_THRESHOLD=yaml_dict["SIMILAR_THRESHOLD"]
    global vectorizer
    vectorizer=yaml_dict["vectorizer"]
    load_faiss_index(FAISS_MODEL765)
    load_encoder_model_765()
    connect_mysql()
    initialized=True
    print("initialized")
def connect_mysql():
    global mydb
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    return mydb
def gcs_handler(paths):
    from os import path
    local_file_path=""
    if "local_file_path" in paths:
        local_file_path=paths["local_file_path"]
    if path.exists(local_file_path):
        return "exists"
    elif "gcs_project" in paths and "bucket_name" in  paths and "gcs_path_file" in paths :
        storage_client = storage.Client(paths["gcs_project"])
        # Create a bucket object for our bucket
        bucket = storage_client.get_bucket(paths["bucket_name"])
        gcs_path_file=paths["gcs_path_file"]
        blobs = bucket.list_blobs(prefix=gcs_path_file)  # Get list of files
        for blob in blobs:
            if blob.name.endswith("/"):
                continue
            file_split = blob.name.split("/")
            directory = "/".join(file_split[0:-1])
            Path(directory).mkdir(parents=True, exist_ok=True)
            blob.download_to_filename(blob.name)
        return "downloaded"
    else:
        print ("faiss model not loaded")
def load_faiss_index(FAISS_MODEL):
    global index
    file_result=gcs_handler(FAISS_MODEL)
    if file_result=="exists":
        index=faiss.read_index( FAISS_MODEL["local_file_path"])
    else:
        index=faiss.read_index( FAISS_MODEL["gcs_path_file"])
    return index
def load_encoder_model_765():
    global encoding_model
    file_result=gcs_handler(vectorizer)
    if file_result=="exists":
        encoding_model= encoder765.model_loading(vectorizer["local_file_path"])
    else:
        encoding_model= encoder765.model_loading(vectorizer["gcs_path_file"])
    return encoding_model
def search_765(text):
    if initialized==False:
        initiate_765()
    results=[]
    encoded= encoder765.predict_single(text, encoding_model).tolist()
    encoded=np.array(encoded ,dtype=np.float32)
    D, I = index.search(encoded, SIMILAR_THRESHOLD)
    mycursor = mydb.cursor()
    for id in I[0]:
        mycursor.execute("SELECT response FROM table where id="+ str(id))
        myresult = mycursor.fetchall()
        results.append(str(myresult[0][0]))
    return results