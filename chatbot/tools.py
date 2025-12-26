from typing import * 
from .config import *
from .functions import *
from langchain_core.tools import tool

# Tools for qdrant vector database
@tool
def search_insurance(query: str, top_k: int = 20) -> str:
  """
  Function for retrieve and rerank information about relevant insurance from 
  qdrant vector store based on query
  args:
    query (str): The search query string.
    top_k (int): Number of top results from index searching, default 20 data. 
  """
  results = vector_store_product.similarity_search(query, k=10)
  documents = [d.page_content for d in results]
  reranked = reranker.rank(query,documents,return_documents=True,top_k=top_k,)
  return reranked

#tools for calculation premi health 
@tool
def premi_calc_health(usia: int, jumlah_peserta: int, jenis_asuransi_kesehatan: str) -> int:
  """
  Function untuk menghitung premi asuransi kesehatan.

  Ketentuan:
    - Premi ditentukan berdasarkan usia peserta.
    - Total premi = rate usia × jumlah peserta.
    - Jika jumlah peserta lebih dari 1 orang atau berkeluarga, otomatis premi diberikan diskon 10%.
    - Diskon tidak ditampilkan secara terpisah dalam hasil.
    - Tampilkan hanya nilai akhir premi.
    - Jangan menampilkan detail rumus atau rate.
    - Sampaikan bahwa hasil bersifat estimasi dan bukan nilai resmi polis.
  """

  if usia <= 17:
      base_rate = 150_000
  elif usia <= 30:
      base_rate = 200_000
  elif usia <= 45:
      base_rate = 250_000
  elif usia <= 60:
      base_rate = 350_000
  else:
      base_rate = 500_000

  if jumlah_peserta <= 1:
      diskon = 0
  else:
    diskon = 0.1

  premi = (base_rate * jumlah_peserta) - ((base_rate * jumlah_peserta) * diskon)

  return premi

#tools for calculation premi vehicle
@tool
def premi_calc_vehicle(usia_kendaraan: int,jenis_asuransi_kendaraan: str,harga_kendaraan: int) -> str:
    """
    Function untuk menghitung estimasi premi asuransi kendaraan.

    Ketentuan:
    - All Risk: umur kendaraan 1–5 tahun
    - TLO: umur kendaraan 1 tahun ke atas
    - Rate ditentukan berdasarkan umur kendaraan
    - Hanya tampilkan hasil akhir (tanpa rumus)
    - Hasil bersifat estimasi, bukan nilai resmi polis
    - Total premi = rate usia × harga mobil.
    """

    # Normalisasi input
    jenis = jenis_asuransi_kendaraan.lower()

    # Tentukan rate
    if jenis == "all risk":
        if usia_kendaraan <= 1:
            rate = 0.015
        elif usia_kendaraan <= 3:
            rate = 0.02
        elif usia_kendaraan <= 5:
            rate = 0.025
        else:
            return (
                "Asuransi All Risk tidak tersedia untuk kendaraan "
                "dengan usia di atas 5 tahun."
            )

    elif jenis == "tlo":
        if usia_kendaraan <= 3:
            rate = 0.008
        elif usia_kendaraan <= 5:
            rate = 0.01
        else:
            rate = 0.012
    else:
        return "Jenis asuransi kendaraan tidak dikenali."

    # Hitung premi
    premi = harga_kendaraan * rate

    # Return ke LLM (STRING)
    return premi

#tools for calculation premi home
@tool
def premi_calc_home(nilai_rumah: int, produk: str) -> str:
    """
    Function untuk menghitung estimasi premi asuransi rumah.

    Ketentuan:
    - Homesafe basic perlindungan rumah tidak dengan isinya
    - Premi dihitung berdasarkan nilai atau harga rumah.
    - Jangan menampilkan detail rumus atau rate ke pengguna.
    - Tampilkan hanya hasil akhir estimasi premi.
    - Sampaikan bahwa hasil bersifat estimasi dan bukan nilai resmi polis.
    - Hasil bersifat estimasi, bukan nilai resmi polis
    - Total premi = rate usia × harga rumah.

    """
    produk = produk.lower()

    if produk == "homesafe basic":
        rate = 0.0015
    elif produk == "homesafe plus":
        rate = 0.003
    else:
        return "Produk asuransi rumah tidak valid. Pilih HomeSafe Basic atau HomeSafe Plus."

    premi = int(nilai_rumah * rate)
    return premi


#tools for send reccomend email
@tool
def insurance_recomend_email(to_email: str, subject: str, body: str)-> str:
    """
    Docstring for insurance_reccomend_email
    
    :type to_email: str
    :param subject: Description
    :type subject: str
    :param body: Description
    :type body: str
    :return: Description
    """
    email = send_email(to_email, subject, body)
    return email

@tool
def policy_information(policy_number:str)->str:
    """
    Function for retrieve information about policy information from policy_data
    """    
    policy_info = policy(policy_number)
    return policy_info

#tools for send policy information email
@tool
def policy_information_email(to_email: str, subject: str, body: str)-> str:
    """
    Docstring for insurance_reccomend_email
    
    :type to_email: str
    :param subject: Description
    :type subject: str
    :param body: Description
    :type body: str
    :return: Description
    """
    email = send_email(to_email, subject, body)
    return email

@tool
def claim_information(claim_id: str)-> str:
    """
    Function for retrieve information about track claim information from claim_data
    """
    claim_info = claim(claim_id)
    return claim_info

# def search_insurance_qdrant(query, k=10):
#   results = vector_store.similarity_search_with_score(
#       query,
#       k=k)
#   for idx,result in enumerate(results):
#     # product_id = result[0].metadata["product_id"]
#     product_name = result[0].metadata["product_name"]
#     category = result[0].metadata["category"]
#     coverage_type = result[0].metadata["coverage_type"]
#     # product_name = result[0].metadata["product_name"]
#     content = result[0].page_content.replace(f"{product_name} - ", "")
#     match_score = "{:.2f}".format(result[1]*100)
#     print(f"""
#     {idx+1}. Sesuai {match_score}% | {product_name} ({category}) {coverage_type}
#     content : {content}
#     """)

# search_insurance_qdrant("Asuransi Rumah ada apa aja ?")
