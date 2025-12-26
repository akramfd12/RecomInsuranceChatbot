import pandas as pd
from .config import * 
import sqlite3


#Import from local to vector database qdrant for insurance product
URL_DATASET = os.getenv("URL_DATASET")

df = pd.read_excel(URL_DATASET)

data = df[["product_id","product_name","content","category","coverage_type"]]

documents = []
for i in range(data.shape[0]):
  product_id = data["product_id"][i]
  product_name = data["product_name"][i]
  content = data["content"][i]
  category = data["category"][i]
  coverage_type = data["coverage_type"][i]
  doc = Document(
      page_content=f"{content}",
      metadata={"product_id": str(product_id), "product_name": str(product_name),
                "category": str(category), "coverage_type": str(coverage_type),
                },
  )
  documents.append(doc)

uuids = [str(uuid4()) for _ in range(len(documents))]

qdrant = QdrantVectorStore.from_documents(
    documents,
    embedding_engine = EMBEDDING_MODEL,
    url=QDRANT_URL,
    prefer_grpc=True,
    api_key=QDRANT_API_KEY,
    collection_name="insurance_product",
)


#import data for track claim
df_claim = pd.read_excel("claim_dataset.xlsx")

conn = sqlite3.connect("claimdata.db")
df_claim.to_sql("claims", conn, if_exists="replace", index=False)
conn.close()

#import data for information policy
df_policy = pd.read_excel("data_polis_asuransi.xlsx")

conn = sqlite3.connect("policydata.db")
df_policy.to_sql("policies", conn, if_exists="replace", index=False)
conn.close()
