# Database
Сервис хранения и обработки данных.

## / 
- GET(database, collection)  
Получить из БД данные по атрибутам, перечисленным в параметрах запроса.  
Возвращает массив JSON с выводом или статус 404.

- POST(database, collection, data)  
Внести в БД данные, указанные в атрибуте "data".  
Возвращает вывод функции БД вставки данных в атрибуте "output" и статус 201. 

- DELETE(database, collection, data)  
Удалить из БД элементы, подходящие под условия в атрибуте "data".  
Возвращает количество удаленных элементов в атрибуте "deleted" и статус 201. 

- PUT(database, collection, query, data)  
Изменить элементы, подходящие под условия атрибута "query", установив им значения, перечисленные в атрибуте "data".  
Возвращает {"status": "success"}, если какие-либо данные были изменены, иначе 404. 