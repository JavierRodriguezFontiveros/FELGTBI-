@app.post("/personalizar_prompt_usuario_no_ss")
async def personalizar_prompt_usuario_no_ss(user_data: UserData):
    print(f"API Key en uso: {gemini_api_key}")

    try:
        # Determinar el tipo de sección y construir el prompt dinámicamente
        for key, seccion in user_data.data.items():
            titulo = seccion.get("titulo", " ")
            preguntas = seccion.get("preguntas", {})

# SI NO ES SOCIOSANITARIO

            if key.startswith("1"):
    #EXTRAER ID_USUARIO
                id_usuario = None

                id_usuario = seccion.get("id_usuario")
                # id_usuario = str(id_usuario)
                print(f"ID Usuario recibido: {id_usuario}")   
                if not id_usuario.isalnum():
                    return {"error": "ID de usuario no válido."}     
                
                connection = connect_to_db()

                if connection is None:
                    return {"error": "No se pudo conectar a la base de datos."}

                cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

                try:
                    # Escribir la consulta SQL para obtener los datos
                    query = """
                        SELECT provincia, pronombre_elle, pronombre_el, pronombre_ella
                        FROM no_sociosanit_formulario
                        WHERE id_usuario = %s
                    """
                    cursor.execute(query, (id_usuario,))

                    # Obtener el resultado de la consulta
                    resultados = cursor.fetchone()

                    if not resultados:
                        return {"error": "No se encontraron datos para el ID de usuario proporcionado."}
                
                    provincia = resultados["provincia"]
                    pronombres = []

                    if resultados["pronombre_el"]:
                        pronombres.append("Él")
                    if resultados["pronombre_ella"]:
                        pronombres.append("Ella")
                    if resultados["pronombre_elle"]:
                        pronombres.append("Elle/Pronombre neutro")

                    pronombres = ", ".join(pronombres)

                except Exception as e:
                    # Cerrar la conexión en caso de error
                    if connection:
                        cursor.close()
                        connection.close()
                    return {"error": f"Error al procesar la solicitud: {str(e)}"}
                cursor.close()
                connection.close()
## TRAS EXTRAER DATOS, CONFECCIONAR PROMPT
                if key.startswith("1.1"):
                    tiempo_diagnostico = preguntas.get("¿Cuándo te diagnosticaron?", [""])[0]
                    en_tratamiento = preguntas.get("¿Estás en tratamiento TAR?", [""])[0]
                    acceso_medico = preguntas.get("¿Tienes acceso a un médico?", [""])[0]
                    informacion_necesaria = preguntas.get("¿Quieres información sobre algún tema?", ["Ninguna"])[0]

                    # Crear el prompt para la sección 1.1
                    prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Tengo VIH diagnosticado desde " + tiempo_diagnostico + ". \n"
                            "¿Qué si estoy en tratamiento?" + en_tratamiento + ". \n"
                            ". Y además " + acceso_medico + ". \n"
                            "tengo acceso médico. La información que solicito es:"+ informacion_necesaria + "."
                    )

                elif key.startswith("1.2"):
                    tipo_exposicion = preguntas.get("¿Qué tipo de exposición fue?", [" "])[0]
                    tiempo_exposicion = preguntas.get("¿Cuándo ocurrió la posible infección?", [" "])[0]
                    acceso_medico = preguntas.get("¿Tienes acceso a un médico?", [" "])[0]
                    chem_sex = preguntas.get("¿Ha sido en un entorno de 'chem-sex'?", [" "])[0]
                    preocupacion = preguntas.get("¿Has compartido tu preocupación con alguien?", [" "])[0]
                    conocimiento_pep = preguntas.get("¿Sabes qué es la PEP?", [" "])[0]

                    # Crear el prompt para la sección 1.2
                    prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Creo que me he expuesto al virus en " + tiempo_exposicion + ". \n"
                            "El tipo de exposición ha sido:" + tipo_exposicion + ". \n"
                            + chem_sex + "ha sido en entorno de chem-sex. \n"
                            "He compartido mi preocupación con"+ preocupacion + "Y quiero más información sobre la PEP."
                    )

                elif key.startswith("1.3"):
                    tema_informacion = preguntas.get("¿Sobre qué tema quieres información?", [" "])[0]

                    # Crear el prompt para la sección 1.3
                    prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Quiero información sobre:" + tema_informacion)

                elif key.startswith("1.4"):
                    acceso_grupos = preguntas.get("¿Tienes acceso a recursos locales o grupos de apoyo?", [" "])[0]
                    preocupacion4 = preguntas.get("¿Has compartido tu preocupación con alguien?", [" "])[0]
                    apoyo_necesario = preguntas.get("¿Qué apoyo necesitas?", [" "])[0]

                    # Crear el prompt para la sección 1.4
                    prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Estoy acompañando a una persona seropositiva." + acceso_grupos + "tengo acceso a recursos locales o grupos de apoyo. /n"
                            "He compartido mi preocupación con" + preocupacion4 + ". /n"
                            "Me gustaría orientación para conseguir" + apoyo_necesario)

                # Generar la respuesta del modelo
                respuesta_chatbot = generar_respuesta(prompt)

                # Devolver la respuesta del chatbot
                return {"respuesta_chatbot": respuesta_chatbot}
        else:
            prompt = "Título: "

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/personalizar_prompt_usuario_ss")
async def personalizar_prompt_usuario_ss(user_data: UserData):
    print(f"API Key en uso: {gemini_api_key}")

    try:
        # Determinar el tipo de sección y construir el prompt dinámicamente
        for key, seccion in user_data.data.items():
            titulo = seccion.get("titulo", " ")
            preguntas = seccion.get("preguntas", {})

        if key.startswith("2"):
                #EXTRAER ID_USUARIO
                id_usuario = None

                id_usuario = seccion.get("id_usuario")
                # id_usuario = str(id_usuario)
                print(f"ID Usuario recibido: {id_usuario}")   
                if not id_usuario.isalnum():
                    return {"error": "ID de usuario no válido."}    
            # Conectar a la base de datos
                connection = connect_to_db()

                if connection is None:
                    return {"error": "No se pudo conectar a la base de datos."}

                cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

                try:
                    # Escribir la consulta SQL para obtener los datos
                    query = """
                        SELECT ambito_laboral, provincia
                        FROM sociosanit_formulario
                        WHERE id_usuario = %s
                    """
                    cursor.execute(query, (id_usuario,))

                    # Obtener el resultado de la consulta
                    resultados = cursor.fetchone()
                    if not resultados:
                        return {"error": "No se encontraron datos para el ID de usuario proporcionado."}

                    
                    provincia = resultados["provincia"]
                    ambito_laboral = resultados["ambito_laboral"]

                except Exception as e:
                    # Cerrar la conexión en caso de error
                    if connection:
                        cursor.close()
                        connection.close()
                    return {"error": f"Error al procesar la solicitud: {str(e)}"}
                cursor.close()
                connection.close()
                
                if key.startswith("2.1"):
                    eleccion = preguntas.get("¿Qué necesitas?", [" "])[0]

                    # Crear el prompt para la sección 2.1
                    prompt = ("Usa el pronombre neutro (elle) conmigo"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Soy personal sanitario y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                            "Necesito información sobre" + eleccion + ".")
                    
                elif key.startswith("2.2"):
                    eleccion2 = preguntas.get("¿Qué necesitas?", [" "])[0]

                    # Crear el prompt para la sección 2.1
                    prompt = ("Usa el pronombre neutro (elle) conmigo"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Soy trabajador social y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                            "Necesito información sobre" + eleccion2 + ".")

                elif key.startswith("2.3"):
                    eleccion3 = preguntas.get("¿Qué necesitas?", [" "])[0]

                    # Crear el prompt para la sección 2.1
                    prompt = ("Usa el pronombre neutro (elle) conmigo"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Soy psicólogo y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                            "Necesito información sobre" + eleccion3 + ".")
                    
                elif key.startswith("2.4"):
                    eleccion4 = preguntas.get("¿Qué necesitas?", [" "])[0]

                    # Crear el prompt para la sección 2.1
                    prompt = ("Usa el pronombre neutro (elle) conmigo"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Soy educador y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                            "Necesito información sobre" + eleccion4 + ".")
                    
                elif key.startswith("2.5"):
                    eleccion5 = preguntas.get("¿Qué necesitas?", [" "])[0]

                    # Crear el prompt para la sección 2.1
                    prompt = ("Usa el pronombre neutro (elle) conmigo"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Soy voluntario/cuidador y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                            "Necesito información sobre" + eleccion5 + ".")

                else:
                    prompt = "Título: "

                # Generar la respuesta del modelo
                respuesta_chatbot = generar_respuesta(prompt)

                # Devolver la respuesta del chatbot
                return {"respuesta_chatbot": respuesta_chatbot}
    
        else:
            prompt = "Título: "
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))