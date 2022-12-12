import mysql.connector
from machine_learning.unsafe.api.vector_encoding import encoder765
import numpy as np
import time
import faiss
start = time.time()
mydb = mysql.connector.connect(
    host="localhost",
    user="service",
    password="9F5EB1CB0919CD0ED15B67C8F8"
)
mycursor = mydb.cursor()
def create_index():
    mycursor.execute("SELECT id, content FROM persona.mc_uk_messages_unified limit 10")
    myresult = mycursor.fetchall()
    import pandas as pd
    data=pd.DataFrame(myresult)
    data.columns =['id','msg']
    data=data.set_index('id')
    model= encoder765.tf_hub_model_generation()
    encoder765.model_loading()
    print ("read done")
    encoded= encoder765.predict_batch(data['msg'], model)
    print(encoded)
    encoded2= encoder765.predict_serial(data['msg'], model)
    print('encoding done')
    d=768
    index = faiss.IndexFlatL2(d)
    index_map = faiss.IndexIDMap(index)
    index_map.add_with_ids(encoded, np.array(data.index))
    faiss.write_index( index_map,'faiss_index_765_test.bin')
    print('indexing done')
if __name__ == "__main__":
     create_index()

