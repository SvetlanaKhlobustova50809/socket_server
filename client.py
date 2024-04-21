import socket
import pickle

def send_request(request):      
    client_socket.send((pickle.dumps(request)))
    response = client_socket.recv(1024)
    print('----------------------------------------------------')
    print(response.decode())
    print('----------------------------------------------------')

if __name__ == "__main__":
    host = 'localhost' 
    port = 5000 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port)) 
    while True:
        print("1. Добавить запись")
        print("2. Удалить запись")
        print("3. Поиск")
        print("4. Просмотр записи")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Введите имя: ")
            data = {
                "command": "add",
                "name": name,
                "data": {
                    "surname": input("Введите фамилию: "),
                    "patronymic": input("Введите отчество: "),
                    "phone": input("Введите номер телефона: "),
                    "note": input("Введите заметку: ")
                }
            }
            send_request(data)
        elif choice == "2":
            name = input("Введите имя записи для удаления: ")
            data = {
                "command": "delete",
                "name": name
            }
            send_request(data)
        elif choice == "3":
            field = input("Введите имя записи для поиска: ")
            value = input("Введите значение для поиска: ")
            data = {
                "command": "search",
                "field": field,
                "value": value
            }
            send_request(data)
        elif choice == "4":
            name = input("Введите имя записи для просмотра: ")
            data = {
                "command": "view",
                "name": name
            }
            send_request(data)
        elif choice == "5":
            break
        else:
            print('----------------------------------------------------')
            print("Неверный ввод")
            print('----------------------------------------------------')
