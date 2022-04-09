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

import json
import requests
import time


# 2. Complete la declaración if para solicitar al usuario el token de acceso de Webex Teams.
choice = input ("¿Desea usar el token de Webex codificado? (y/n) ")

print(choice)

if choice == "n" or choice == "N":

    while True:
        AccessToken = input("Ingrese el token: ")
        if len(AccessToken) >= 106:
            break
elif choice == "y" or choice == "Y":
	AccessToken = 'OGQyNWVlZTgtZDFkMC00YWRjLWEzNzItZTcwYzlkNmRkYzE1MDI0YTkyMDAtZDZi_P0A1_f71b3b0c-41aa-4432-a8ec-0fba0a4e36ad'

# 3. Proporcione la URL de la API de sala de Webex.
url = 'https://webexapis.com/v1/rooms'
headers = {
'Authorization': 'Bearer {}'.format(AccessToken)
}
r = requests.get(url, headers=headers)

#####################################################################################
# NO EDITAR NINGÚN BLOCK CON r.status_code
if not r.status_code == 200:
    raise Exception ("Respuesta incorrecta de la API de Webex Teams. Status code: {} Text: {}" .format (r.status_code, r.text))
######################################################################################

# 4. Cree un bucle para imprimir el tipo y el título de cada sala.
print ("Lista de salas:")
rooms = r.json () ["items"]
for room in rooms:
    print(f'Sala: {room["title"]} Tipo: {room["type"]}')
    
#######################################################################################
# BUSCAR SALA DE EQUIPOS DE WEBEX PARA MONITOREAR
# - Busca el nombre de sala proporcionado por el usuario.
# - Si se encuentra, imprima el mensaje "found", de lo contrario imprime el error.
# - Almacena valores para su uso posterior por bot.
# NO EDITAR CÓDIGO EN ESTE BLOQUE
#######################################################################################

while True:
    RoomNameToSearch = input ("¿Qué sala debe ser monitoreada para mensajes /location? ")
    RoomidTogetMessages = None


    for room in rooms:
        if(room["title"].find(RoomNameToSearch) != -1):
            print ("Found rooms with the word " + RoomNameToSearch)

        print (room["title"])
        RoomidTogetMessages = room ["id"]
        RoomTitleTogetMessages = room ["title"]
        print ("sala encontrada:" + RoomTitleTogetMessages)
        break

    if (RoomidTogetMessages == None):
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
                            "roomId": RoomidTogetMessages,
                            "max": 1
                    }
# 5. Proporcione la URL de la API de mensajes de Webex.
    url = 'https://webexapis.com/v1/messages'
    headers = {
    'Authorization': 'Bearer {}'.format(AccessToken)
    }
    
    r = requests.get(url, headers=headers, params=GetParameters)

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
    
        print(location)
# 6. Proporcione la clave de consumidor de la API de MapQuest.
        MapsaPigetParameters = { 
                                "location": location, 
                                "key": "Fg8KMOPJkpKlIn0VRKSYOU8QUFYmcQl7"
                               }

# 7. Proporcione la URL de la API de direcciones de MapQuest.
        r = requests.get("http://www.mapquestapi.com/geocoding/v1/address", 
                             params = MapsaPigetParameters
                        )
        json_data = r.json()

        if not json_data["info"]["statuscode"] == 0:
            raise Exception ("Respuesta incorrecta de MapQuest API. Status code: {}" .format (r.statuscode))

        locationResults = json_data["results"][0]["providedLocation"]["location"]
        print ("Ubicación:" + locationResults)
		
# 8. Proporcione los valores clave de MapQuest para obtener la latitud y la longitud.
        # print(json_data)
        # print(json_data["results"])
        # print(json_data["results"][0])
        # print(json_data["results"][0]["locations"])
        # print(json_data["results"][0]["locations"][0])
        displayLatLong = json_data["results"][0]["locations"][0]["displayLatLng"]
        
        LocationLat = displayLatLong["lat"]
        locationLng = displayLatLong["lng"]
        print ("Localización coordenadas GPS:" + str (LocationLat) + "," + str (locationLng))
        
        IssaPigetParameters = { 
                                "lat": LocationLat, 
                                "lon": locationLng
                              }
# 9. Proporcione la URL de la API de tiempos de paso de ISS.
        r = requests.get("http://api.open-notify.org/iss-pass.json", 
                             params = IssaPigetParameters
                        )

        json_data = r.json()

        if not "response" in json_data:
            raise Exception ("Respuesta incorrecta de la API open-notify.org. Status code: {} Texto: {}" .format (r.status_code, r.text))

# 10. Proporcione los valores clave ISS del tiempo de espera y duración.
        risetimeinEpochSeconds = json_data ["response"][0]["risetime"]
        durationInSeconds = json_data ["response"][0]["duration"]

# 11. Convierta el valor de risetime epoch en una fecha y hora legible para humanos.
        risetimeInFormattedString = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(risetimeinEpochSeconds))

# 12. Complete el código para formatear el mensaje de respuesta.
# Ejemplo de resultado de un mensaje de respuesta: En Austin, Texas, la ISS sobrevolará el jue Jun 18 18:42:36 2020 durante 242 segundos.
        responseMessage = f"In {location} the ISS will fly over on {risetimeInFormattedString} for {durationInSeconds} seconds."

        print ("Envío a Webex:" + responseMessage)

    # 13. Complete el código para publicar el mensaje en la sala de Webex. 
        HttpHeaders = {
                        "Authorization": 'Bearer {}'.format(AccessToken),
                        "Content-Type": "application/json"
                        }
        PostData = {
                            "roomId": RoomidTogetMessages,
                            "text": responseMessage
                        }
        url = 'https://webexapis.com/v1/messages'

        r = requests.post (url, 
                                data = json.dumps(PostData), 
                                headers= HttpHeaders
                            )
        if not r.status_code == 200:
            raise Exception ("Respuesta incorrecta de la API de Webex. Status code: {} Text: {}" .format (r.status_code, r.text))

        exit("El programa ha finalizado con éxito")