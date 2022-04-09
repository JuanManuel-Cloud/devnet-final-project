###############################################################
# Este programa:
# - Pide al usuario que ingrese un token de acceso o use el token de acceso codificado.
# - Enumera las salas de Webex Teams del usuario.
# - Pregunta al usuario qué sala de Webex Teams debe supervisar las solicitudes "/location".
# - Supervisa cada segundo la sala de Webex Teams seleccionada en busca de mensajes "/location".
# - Descubre las coordenadas GPS para la "ubicación" usando la API de MapQuest.
# - Descubre la fecha y la hora del siguiente paso de ISS sobre la "ubicación" usando la API de ISS
# - Formatea y envía los resultados a la sala de Webex Teams.
#
# El estudiante debe:
# 1. Importar librerías para solicitudes, JSON y tiempo.
# 2. Complete la declaración if para solicitar al usuario el token de acceso de Webex Temas.
# 3. Proporcione la URL de la API de sala de Webex Temas.
# 4. Cree un bucle para imprimir el tipo y el título de cada sala.
# 5. Proporcione la URL de la API de mensajes de Webex Teams.
# 6. Proporcione la clave de consumidor de la API de MapQuest.
# 7. Proporcione la URL de la API de direcciones de MapQuest.
# 8. Proporcione los valores clave de MapQuest para obtener la latitud y la longitud.
# 9. Proporcione la URL de la API de tiempos de paso de ISS.
# 10. Proporcione los valores clave ISS del tiempo de ascenso y duración.
# 11. Convierta el valor del tiempo epoch de subida en una fecha y hora legibles por humanos.
# 12. Complete el código para formatear el mensaje de respuesta.
# 13. Complete el código para publicar el mensaje en la sala de Webex Teams.
###############################################################

# 1. Importar bibliotecas para solicitudes, JSON y tiempo.

<!!!REEMPLAZAR con código para librerías>

# 2. Complete la declaración if para solicitar al usuario el token de acceso de Webex Teams.
choice = input ("¿Desea usar el token de Webex codificado? (y/n) ")

<!!!REEMPLAZAR con instrucciones if para pedir al usuario el token de acceso de WebexTeams!!!>
else:
	AccessToken = "Bearer<!!!REEMPLAZAR con token codificado!!!>"

# 3. Proporcione la URL de la API de sala de Webex.
r = requests.get ("<!!!!REEMPLAZAR URL!!!>",
                    headers = {"Authorization": accessToken}
                ).

#####################################################################################
# NO EDITAR NINGÚN BLOCK CON r.status_code
if not r.status_code == 200:
    raise Exception ("Respuesta incorrecta de la API de Webex Teams. Status code: {} Text: {}" .format (r.status_code, r.text))
######################################################################################

# 4. Cree un bucle para imprimir el tipo y el título de cada sala.
print ("Lista de salas:")
rooms = r.json () ["items"]
for room in rooms:
    <!!!REEMPLAZAR con código de impresión para terminar el bucle >

#######################################################################################
# BUSCAR SALA DE EQUIPOS DE WEBEX PARA MONITOREAR
# - Busca el nombre de sala proporcionado por el usuario.
# - Si se encuentra, imprima el mensaje "found", de lo contrario imprime el error.
# - Almacena valores para su uso posterior por bot.
# NO EDITAR CÓDIGO EN ESTE BLOQUE
#######################################################################################

while True:
    RoomNameToSearch = input ("¿Qué sala debe ser monitoreada para mensajes /location? ")
    RoomIDToGetMessages = None
    
    for room in rooms:
        if(room["title"].find(roomNameToSearch) != -1):
            print ("Found rooms with the word " + roomNameToSearch)

 print (sala ["title"])
            RoomidTogetMessages = room ["id"]
            RoomTitleTogetMessages = room ["title"]
            print ("sala encontrada:" + RoomTitleToGetMessages)
            break

    if (RoomIDToGetMessages == None):
        print ("Lo siento, no encontré ninguna sala con" + RoomNameToSearch +".")
        print ("Inténtelo de nuevo...")
    else:
        break

######################################################################################
# CÓDIGO BOT DE WEBEX TEAMS
# Inicia el bot de Webex para escuchar y responder a los mensajes /location.
######################################################################################

while True:
    time.sleep (1)
    GetParameters = {
                            "roomId": RoomIDToGetMessages,
                            "max": 1
                    }
# 5. Proporcione la URL de la API de mensajes de Webex.
    r = requests.get ("<!!!!REEMPLAZAR URL!!!>", 
                         params = getParameters, 
                         headers = {"Authorization": accessToken}
                    ).

    if not r.status_code == 200:
        raise Exception ("Respuesta incorrecta de la API de Webex Teams. Status code: {} Texto: {}" .format (r.status_code, r.text))
    
    json_data = r.json ()
    if len (json_data ["items"]) == 0:
        raise Exception ("No hay mensajes en la sala.")
    
    messages = json_data ["items"]
    message = messages [0] ["text"]
    print("Received message: " + message)
    
    if message.find ("/") == 0:
        location = message [1:]
# 6. Proporcione la clave de consumidor de la API de MapQuest.
        MapsaPigetParameters = { 
                                "location": location, 
                                "clave": "<!!!REEMPLAZAR con su clave de API de MapQuest!!!>"
                               }

# 7. Proporcione la URL de la API de direcciones de MapQuest.
        r = requests.get("<!!!REEMPLAZAR URL!!!>", 
                             params = MapsaPigetParameters
                        ).
        json_data = r.json()

        if not json_data ["info"] ["statuscode"] == 0:
            raise Exception ("Respuesta incorrecta de MapQuest API. Status code: {}" .format (r.statuscode))

        locationResults = json_data ["results"] [0] ["ProvidedLocation"] ["location"]
        print ("Ubicación:" + LocationResults)
		
# 8. Proporcione los valores clave de MapQuest para obtener la latitud y la longitud.
        LocationLat = json_data ["<!!!!REEMPLAZAR!!!> con la ruta a la tecla de latitud!!!> "]
        locationLng = json_data ["<!!!!REEMPLAZAR!!!> con la ruta a la clave de longitud!!!> "]
        print ("Localización coordenadas GPS:" + str (LocationLat) + "," + str (LocationLng))
        
        IssaPigetParameters = { 
                                "lat": locationLat, 
                                "lon": locationLng
                              }
# 9. Proporcione la URL de la API de tiempos de paso de ISS.
        r = requests.get("<!!!REPLACE with URL!!!>", 
                             params = IssaPigetParameters
                        ).

        json_data = r.json()

        if not"response" en json_data:
            raise Exception ("Respuesta incorrecta de la API open-notify.org. Status code: {} Texto: {}" .format (r.status_code, r.text))

# 10. Proporcione los valores clave ISS del tiempo de espera y duración.
        risetimeinEpochSeconds = json_data ["<!!!!REEMPLAZAR!!!> con la ruta a la clave de tiempo de ascenso!!!> "]
        durationInSeconds = json_data ["<!!!!REEMPLAZAR!!!> con la ruta a la clave de duración!!!> "]

# 11. Convierta el valor de risetime epoch en una fecha y hora legible para humanos.
        risetimeInFormattedString = <!!!REEMPLAZAR con código de conversión!!!>

# 12. Complete el código para formatear el mensaje de respuesta.
# Ejemplo de resultado de un mensaje de respuesta: En Austin, Texas, la ISS sobrevolará el jue Jun 18 18:42:36 2020 durante 242 segundos.
        responseMessage = "In {} the ISS will fly over on {} for {} seconds.".format(<!!!REPLACE with required variables!!!>)

print ("Envío a Webex:" +ResponseSage)

# 13. Complete el código para publicar el mensaje en la sala de Webex. 
        HttpHeaders = { 
                             "Authorization": <!!!REEMPLAZAR!!!>,
                             "Content-Type": "application/json"
                           }
        PostData = {
                            "RoomID": <!!!REEMPLAZAR!!!>,
                            "text": <!!!REEMPLAZAR!!!>
                        }

        r = requests.post ("<!!!!REEMPLAZAR URL!!!>", 
                              data = json.dumps (<!!!REEMPLAZAR!!!>), 
                              headers= <!!!REEMPLAZAR!!!>
                         ).
        if not r.status_code == 200:
            raise Exception ("Respuesta incorrecta de la API de Webex. Status code: {} Text: {}" .format (r.status_code, r.text))