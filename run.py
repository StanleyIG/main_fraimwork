import os
from main_fraimwork.main import Framework
from wsgi_static_middleware import StaticMiddleware
from views import routes
from components.front_controllers import front_controllers
from wsgiref.simple_server import make_server
from components import settings


# BASE_DIR = os.path.dirname(__name__) # os.path.dirname(__file__)
# STATIC_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
# #print(BASE_DIR)
# #print(STATIC_DIRS)

# # Создаем объект WSGI-приложения
# application = Framework(routes, front_controllers)
# app_static = StaticMiddleware(application,
#                               static_root='staticfiles',
#                               static_dirs=STATIC_DIRS)


# with make_server('', 8080, app_static) as httpd:
#     print('Запуск сервера на порту http://127.0.0.1:8080')
#     httpd.serve_forever()


application = Framework(settings, routes, front_controllers)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080: 127.0.0.1:8080")
    httpd.serve_forever()
