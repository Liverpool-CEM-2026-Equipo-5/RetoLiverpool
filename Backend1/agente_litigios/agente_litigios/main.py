from agent import pinecone_search

while True:
    pregunta = input("\nPregunta sobre los litigios: ")

    if pregunta.lower() in ["salir", "exit", "quit"]:
        break

    respuesta = pinecone_search(pregunta)
    print("\nContexto encontrado:")
    print(respuesta)