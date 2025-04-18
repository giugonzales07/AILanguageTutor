# Gerar consulta e buscar nos documentos
# def gerar_e_buscar_consulta(content, DataFrame, model):
#   # Gerar o embedding da consulta
#   embedding_da_consulta = genai.embed_content(model=model,
#                                  content=content,
#                                  task_type="RETRIEVAL_QUERY")["embedding"]

#   # calcular a distância entre a consulta e os documentos
#   produtos_escalares = np.dot(np.stack(DataFrame['embeddings']), embedding_da_consulta)

#   # pegar o indicie do token maior produto escalar que represente o mais próximo
#   index = np.argmax(produtos_escalares)

#   # pegar o conteúdo de acordo com o indíce
#   return_text = DataFrame.iloc[index]["content"]

#   return return_text

# consulta = "How do you shift gears in the Google car?"

# trecho = gerar_e_buscar_consulta(consulta, df_documents, model)

# print(trecho)