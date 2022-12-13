# Fast Retrieval of Pairs of Message-Reply Conversations
This project provides a solution to retrieve pairs of messages-replies.
The proposed method is to compute the BERT embedding of all messages and persist them using a Facebook AI Similarity Search (Faiss) index
Since Faiss is limited to store integer as an index, we have to denormalize message-reply pairs into two databases:
1) storing the messages and their corresponding IDs in a Faiss index.
2) storing the replying and their corresponding IDs in a RDBMS (i.e. mysql in this case)

## Data Migration
The script read messages and IDs from a mysql table, calculate their embedding vectors, and store the vectors and ids into fais map index:
```
index = faiss.IndexFlatL2(dimension)
index_map = faiss.IndexIDMap(index)
index_map.add_with_ids(vector, ids)
```
## API
This waitress/flask rest API receives a message and returns top n similar conversations.
This method calculates embedding vectors of receives text, and query the Faiss index to retrieve the ids of similar messages. Finally, it queries the mysql database based on the ids to retrieve corresponding replies.
