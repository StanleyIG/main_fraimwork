from quopri import decodestring
from components.content_types import CONTENT_TYPES_MAP
from main_fraimwork.framework_requests import GetRequestClass
from os import path
import quopri

class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Класс Framework - основа WSGI-фреймворка"""

    def __init__(self, settings, routes_obj, fronts_obj):
        self.settings = settings
        self.routes_lst = routes_obj
        self.fronts_applications = fronts_obj

    def __call__(self, environ, start_response):
        # Получаем адрес, по которому пользователь выполнил переход
        path = environ['PATH_INFO']

        # Добавляем закрывающий слеш
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        # обрабатываем запрос с помощью соотвествующего класса
        method_class = GetRequestClass(method)
        data = method_class.get_request_params(environ)
        request[method_class.dict_value] = Framework.decode_value(data)
        #print(f'{method}: {Framework.decode_value(data)}')
        for front_app in self.fronts_applications:
            front_app(environ, request)

        # Находим нужный контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]
            print(view)
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')
            

        elif path.startswith(self.settings.STATIC_URL):
            # /static/images/logo.jpg/ -> images/logo.jpg
            file_path = path[len(self.settings.STATIC_URL):len(path)-1]
            #print(file_path)
            content_type = self.get_content_type(file_path)
            #print(content_type)
            code, body = self.get_static(self.settings.STATIC_FILES_DIR,
                                         file_path)

        else:
            view = PageNotFound404()
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')
            
        
        start_response(code, [('Content-Type', content_type)])

        return [body]


    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = path.basename(file_path).lower() # styles.css
        extension = path.splitext(file_name)[1] # .css
        #print(extension)
        return content_types_map.get(extension, "text/html")

    @staticmethod
    def get_static(static_dir, file_path):
        path_to_file = path.join(static_dir, file_path)
        with open(path_to_file, 'rb') as f:
            file_content = f.read()
        status_code = '200 OK'
        return status_code, file_content

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
