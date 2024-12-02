from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

# Настройки подключения к базе данных MySQL
db_config = {
    'host': 'localhost',  # Адрес сервера базы данных
    'user': 'user_name',  # Имя пользователя для подключения
    'password': 'password123',  # Пароль пользователя
    'database': 'mail_database'  # Название базы данных
}

# Главная страница, отображающая данные из таблиц
@app.route('/')
def index():
    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Извлекаем данные из таблицы "organization_addresses"
        cursor.execute("SELECT organization_name, address, director_lastname FROM organization_addresses")
        organization_records = cursor.fetchall()  # Сохраняем записи организаций

        # Извлекаем данные из таблицы "correspondence"
        cursor.execute("SELECT correspondence_type, preparation_date, organization_name FROM correspondence")
        correspondence_records = cursor.fetchall()  # Сохраняем записи корреспонденции

    except mysql.connector.Error as e:
        # Если произошла ошибка при подключении, выводим её в консоль
        print(f"Ошибка подключения к базе данных: {e}")
        organization_records = []
        correspondence_records = []  # Если произошла ошибка, возвращаем пустые списки
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Передаем извлеченные данные в HTML-шаблон для отображения
    return render_template('index.html',
                           organization_records=organization_records,
                           correspondence_records=correspondence_records)

# Добавление записи в таблицу "organization_addresses"
@app.route('/organization/add', methods=['POST'])
def add_organization():
    # Получаем данные из формы
    organization_name = request.form.get('organization_name')  # Название организации
    address = request.form.get('address')  # Адрес организации
    director_lastname = request.form.get('director_lastname')  # Фамилия руководителя

    # Проверяем, что все поля заполнены
    if not organization_name or not address or not director_lastname:
        print("Ошибка: Одно или несколько полей пустые.")  # Сообщение об ошибке
        return redirect('/')  # Возврат на главную страницу

    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL-запрос для добавления новой записи в таблицу "organization_addresses"
        query = """
        INSERT INTO organization_addresses (organization_name, address, director_lastname)
        VALUES (%s, %s, %s)
        """
        # Выполняем запрос с переданными данными
        cursor.execute(query, (organization_name.strip(), address.strip(), director_lastname.strip()))
        connection.commit()  # Сохраняем изменения в базе данных

    except mysql.connector.Error as e:
        # Если произошла ошибка при добавлении записи, выводим её в консоль
        print(f"Ошибка при добавлении записи: {e}")
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect('/')  # Возвращаемся на главную страницу для обновления данных

# Добавление записи в таблицу "correspondence"
@app.route('/correspondence/add', methods=['POST'])
def add_correspondence():
    # Получаем данные из формы
    correspondence_type = request.form.get('correspondence_type')  # Тип корреспонденции
    preparation_date = request.form.get('preparation_date')  # Дата подготовки
    organization_name = request.form.get('organization_name')  # Название организации

    # Проверяем, что все поля заполнены
    if not correspondence_type or not preparation_date or not organization_name:
        print("Ошибка: Одно или несколько полей пустые.")  # Сообщение об ошибке
        return redirect('/')  # Возврат на главную страницу

    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL-запрос для добавления новой записи в таблицу "correspondence"
        query = """
        INSERT INTO correspondence (correspondence_type, preparation_date, organization_name)
        VALUES (%s, %s, %s)
        """
        # Выполняем запрос с переданными данными
        cursor.execute(query, (correspondence_type.strip(), preparation_date.strip(), organization_name.strip()))
        connection.commit()  # Сохраняем изменения в базе данных

    except mysql.connector.Error as e:
        # Если произошла ошибка при добавлении записи, выводим её в консоль
        print(f"Ошибка при добавлении записи: {e}")
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect('/')  # Возвращаемся на главную страницу для обновления данных

# Удаление записи из таблицы "organization_addresses"
@app.route('/organization/delete/<organization_name>', methods=['GET'])
def delete_organization(organization_name):
    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL-запрос для удаления записи из таблицы "organization_addresses"
        query = "DELETE FROM organization_addresses WHERE organization_name = %s"
        cursor.execute(query, (organization_name,))
        connection.commit()  # Сохраняем изменения в базе данных

    except mysql.connector.Error as e:
        # Если произошла ошибка при удалении записи, выводим её в консоль
        print(f"Ошибка при удалении записи: {e}")
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect('/')  # Возвращаемся на главную страницу для обновления данных

# Удаление записи из таблицы "correspondence"
@app.route('/correspondence/delete/<organization_name>', methods=['GET'])
def delete_correspondence(organization_name):
    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL-запрос для удаления записи из таблицы "correspondence"
        query = "DELETE FROM correspondence WHERE organization_name = %s"
        cursor.execute(query, (organization_name,))
        connection.commit()  # Сохраняем изменения в базе данных

    except mysql.connector.Error as e:
        # Если произошла ошибка при удалении записи, выводим её в консоль
        print(f"Ошибка при удалении записи: {e}")
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect('/')  # Возвращаемся на главную страницу для обновления данных

# Запуск Flask-приложения
if __name__ == '__main__':
    # Запуск приложения в режиме отладки для отслеживания ошибок
    app.run(debug=True)
