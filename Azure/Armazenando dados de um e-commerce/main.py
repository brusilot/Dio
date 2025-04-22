import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()




blobConnectionString = os.getenv('CONNECTION_STRING')
blobContainerName = os.getenv('CONTAINER_NAME')
blobAccountName = os.getenv('ACCOUNT_NAME')

sqlServer = os.getenv('SQL_SERVER')
sqlDatabase = os.getenv('SQL_DATABASE')
sqlUser = os.getenv('SQL_USER')
sqlPassword = os.getenv('SQL_PASSWORD')

st.title('Cadastro de Produtos')

product_name = st.text_input('Nome do Produto')
product_price = st.number_input('Preço do Produto', min_value=0.0, format='%.2f')
product_description = st.text_input('Descrição do Produto')
product_image = st.file_uploader('Imagem do Produto', type=['jpg', 'png', 'jpeg'])

def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid64()) + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite = True)
    image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    return image_url

def insert_product(product_name, product_price, product_description, product_image):
    try:
        conn = pymssql.connect(server=sqlServer, user=sqlUser, password=sqlPassword, database=sqlDatabase)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO dbo.Produtos (nome, preco, descricao, imagem_url) VALUES  ('{product_name}',{product_price},'{product_description}','{product_image}')")
        conn.commit()
        conn.close()

        return True
    except Exception as e:
        st.error(f'Erro ao inserir produto: {e}')
        return False
    
 
def list_products():
    try:
        conn = pymssql.connect(server=sqlServer, user=sqlUser, password=sqlPassword, database=sqlDatabase)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM dbo.Produtos")
        rows = cursor.fetchall()

        conn.close()

        return rows
    except Exception as e:
        st.error(f'Erro ao listar produto: {e}')
        return False
    
 
def list_products_screen():
    products = list_products()
    if products:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product[1]}")
                st.write(f"**Descricao**: {product[2]}")
                st.write(f"**Preco**: {product[3]}")
                if product[4]:
                    html_img = f'<img src="{product[4]}" width="200" height="200" alt="Imagem do produto">'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.markdown("----")
            if( i+1 ) % cards_por_linha ==0 and (i+1) < len(products):
                cols = st.columns(cards_por_linha)
    else
        st.info("Nenhum produto encontrado.")


if st.button('Salvar Produto'):
    insert_product(product_name, product_price, product_description, product_image)
    return_message = 'Produto salvo com sucesso'

st.header('Listar Produtos')

if st.button('Listar Produtos'):
    list_products_screen()
    return_message = 'Produto salvo com sucesso'