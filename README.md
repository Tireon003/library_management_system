# Library management system
Простая система управления библиотекой. Взаимодействие с системой осуществляется с помощью набора консольных команд.

### Функционал:
1. Добавление книги при помощи команды ```/add <title> <author> <year>```.
2. Удаление книги при помощи команды ```/remove <book_id>```
3. Поиск книги по нужному полю при помощи команды ```/search <field> <value> [limit]```.
   Команда находит все строки, в поле которого есть указанная подстрока.
4. Получение списка всех книг по команде ```/list [limit]```.
5. Изменение статуса книги при помощи команды ```/update_status <book_id> <status>```.
6. Получение списка всех команд при помощи ```/help```
7. Завершение работы программы при помощи ```/exit```

### Примечания:
 - Параметр ```limit``` является опциональным, по умолчанию равен 0 (выводится весь список). При указании отрицательных значений выводятся количество элементов с конца.
 - Параметры ```title``` и ```author``` указываются в кавычках в случае, если в тексте содержатся пробелы.
 - Ограничения по длине ```title``` и ```author``` составляет от 6 до 36 включительно.
 - Ограничения по полю ```year``` - с 1900 по 2100.
 - Поле ```status``` должно быть валидной строкой ```available``` или ```issued```.

### Особенности реализации:
 - Проект написан на Python 3.12.
 - Использован объектно ориентированный подход.
 - Проект соответствует принципам SOLID.
 - Настроена обработка исключений.
 - Используются только библиотеки из стандартного пакета Python.
 - В проекте используются аннотации типов.
 - Код проекта задокументирован.

#### Как запустить:
1. Устанавилваем Git если не установлен
2. Клонируем репозиторий при помощи команды: ```git clone https://github.com/Tireon003/library_management_system```
3. Создаем в корне проекта файл .env c параметром ```BOOK_STORAGE_NAME="book_storage.json"```. В кавычках указывается требуемый json-файл либо название файла. Если файла не существует, он будет создан автоматически после запуска программы.
4. Запускаем модуль ```main.py```