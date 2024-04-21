import socket
import pickle
import os
import _thread


def load_phonebook():
    if os.path.exists("phonebook.pkl"):
        with open("phonebook.pkl", "rb") as file:
            return pickle.load(file)
    return {}


def save_phonebook(phonebook):
    with open("phonebook.pkl", "wb") as file:
        pickle.dump(phonebook, file)


def handle_request(request, phonebook):
    command = request.get("command")
    if command == "add":
        name = request.get("name")
        if name not in phonebook:
            phonebook[name] = request.get("data")
            save_phonebook(phonebook)
            return "Запись добавлена"
        else:
            return "Запись с таким именем уже существует"
    elif command == "delete":
        name = request.get("name")
        if name in phonebook:
            del phonebook[name]
            save_phonebook(phonebook)
            return "Запись удалена"
        else:
            return "Записи с таким именем не существует"
    elif command == "search":
        field = request.get("field")
        value = request.get("value")
        if field in phonebook:
            if value in phonebook[field].values():
                for k, v in phonebook[field].items():
                    if v == value: ans = (k, v)
                return f'{ans}'
            else:
                return "Запись не найдена"
        else:
            return "Поля с таким именем не существует"
    elif command == "view":
        name = request.get("name")
        if name in phonebook:
            return f'{phonebook[name]}'
        else:
            return "Записи с таким именем не существует"
    else:
        return "Неверная команда"


def handle_client_connection(client_socket, phonebook):
    try:
        while True:
            request_data = client_socket.recv(1024)
            if not request_data:
                break
            request = pickle.loads(request_data)
            response = handle_request(request, phonebook)
            print(response)
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print("Ошибка при обработке запроса:", e)
        client_socket.close()

    finally:
        client_socket.close()
        
        
def start_server(): 
    phonebook = load_phonebook()
    host = 'localhost'
    port = 5000 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port)) 
    server.listen(5) 
    
    while True:
        client, address = server.accept() 
        print("Connection from: " + str(address))     
        _thread.start_new_thread(handle_client_connection,(client,phonebook))
    
if __name__ == "__main__":
    start_server()