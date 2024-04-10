from datetime import date

from main_fraimwork.templator import render
from components.models import Engine, MapperRegistry
from components.decorators import AppRoute
from components.cbv import ListView, CreateView
from components.unit_of_work import UnitOfWork

site = Engine()
routes = {}
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

# Класс-контроллер - Главная страница
@AppRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        mapper = MapperRegistry.get_current_mapper('category')
        all_category = mapper.all()
        print('Категории Index', site.categories)
        # return '200 OK', render('index.html', objects_list=site.categories, geo=request.get('geo', None))
        return '200 OK', render('index.html', objects_list=all_category, geo=request.get('geo', None))

# Класс-контроллер - Страница "О проекте"


@AppRoute(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', render('about.html', geo=request.get('geo', None))


# Класс-контроллер - Страница "Расписания"
@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html', geo=request.get('geo', None))


# Класс-контроллер - Страница 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Класс-контроллер - Страница "Список курсов"
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    def __call__(self, request):
        print(f'Вызван CategoryList, категория')
        print(site.categories)
        
        mapper = MapperRegistry.get_current_mapper('category')
        try:
            category = site.find_category_by_id(
                 int(request['request_params']['id']))
            #category = mapper.get_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'



# Класс-контроллер - Страница "Создать курс"
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1
    mapper = MapperRegistry.get_current_mapper('category')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                category2 = self.mapper.get_by_id(self.category_id)
                print(id(category))
                print(id(category2))
                
                course = site.create_course('record', name, category)
                print(course.category.courses)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(
                     int(self.category_id))
                
                #category = self.mapper.get_by_id(self.category_id)

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# Класс-контроллер - Страница "Создать категорию"
@AppRoute(routes=routes, url='/create-category/')
class CategoriesCreateView(CreateView):
    template_name = 'create_category.html'

    def create_obj(self, data: dict):

        name = data.get('name')

        name = site.decode_value(name)

        new_category = site.create_category()

        #site.categories.append(new_category)

        schema = {'name': name}
        new_category.mark_new(schema)
        UnitOfWork.get_current().commit()
        print('Категории', site.categories)
        mapper = MapperRegistry.get_current_mapper('category')
        all_category = mapper.all()
        print(new_category.__dict__)
        print(all_category[-1].__dict__)
        site.categories.append(all_category[-1])
        
        # return '200 OK', render('index.html',
        #                             objects_list=site.categories)


# Класс-контроллер - Страница "Список категорий"
@AppRoute(routes=routes, url='/category-list/')
class CategoryList(ListView):
    template_name = 'category_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data.get('name')
        name = site.decode_value(name)
        new_obj = site.create_user('student')

        site.students.append(new_obj)
        schema = {'name': name}
        new_obj.mark_new(schema)
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)
