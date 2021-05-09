# TODO create new needed views and implement the whole thing
# TODO permission are needed to disable certain elements of the interface
# TODO also need to create special views for all tables with foreign keys
post_tables = {
    # format
    # Post name: [
    #     {
    #         'name': Table #1 name,
    #         'heading': Table #1 heading,
    #         'columns': [Column #1, Column #2, ..., Column #N],
    #         'col_headings': [Heading #1, Heading #2, ..., Heading #N],
    #         'CREATE': permission (bool),
    #         'UPDATE': permission (bool),
    #         'DELETE': permission (bool)
    #     },
    #     ...
    # ],
    # ...
    'Кассир': [
        # {
        #     'name': 'schedule_week',
        #     'heading': 'Расписание на неделю',
        #     'columns': ['ddate', 'route', 'stops', 'train', ],
        #     'col_headings': ['Дата', 'Номер маршрута', 'Остановки', 'Поезд', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
        {
            'name': 'tickets',
            'heading': 'Билеты',
            'columns': ['payment_date', 'depart_st', 'arrive_st', 'tariff', 'round_trip', 'cashier', ],
            'col_headings': ['Дата', 'Откуда', 'Куда', 'Тип', 'Туда-обратно', 'Кассир', ],
            'CREATE': True,
            'UPDATE': False,
            'DELETE': True
        },
    ],
    'Заведующий направлением': [
        {
            'name': 'trains',
            'heading': 'Поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
        },
        # {
        #     'name': 'active_trains',
        #     'heading': 'Активные поезда',
        #     'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
        #     'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
        # {
        #     'name': 'machinists',  # TODO Sure machinists? Not employees?
        #     'heading': 'Машинисты',
        #     'columns': ['tabno', 'post', 'full_name', 'passport', 'birth_date', 'sex', 'snils', 'inn', 'emp_date',
        #                 'quit_date', ],
        #     'col_headings': ['Таб. номер', 'Должность', 'ФИО', 'Паспорт', 'Дата рождения', 'Пол', 'СНИЛС', 'ИНН',
        #                      'Дата приема', 'Дата увольнения', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
        # {
        #     'name': 'active_machinists',  # TODO Sure machinists? Not employees?
        #     'heading': 'Активные машинисты',
        #     'columns': ['tabno', 'post', 'full_name', 'passport', 'birth_date', 'sex', 'snils', 'inn', 'emp_date',
        #                 'quit_date', ],
        #     'col_headings': ['Таб. номер', 'Должность', 'ФИО', 'Паспорт', 'Дата рождения', 'Пол', 'СНИЛС', 'ИНН',
        #                      'Дата приема', 'Дата увольнения', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
        # {
        #     'name': 'manager_routes_verbose',
        #     'heading': 'Маршруты',
        #     'columns': ['id', 'tariff', 'wdays', 'way', 'stops', ],
        #     'col_headings': ['Номер', 'Тип', 'Режим движения', 'Сторона', 'Остановки'],
        #     'CREATE': True,
        #     'UPDATE': True,
        #     'DELETE': True
        # },
        {
            'name': 'rides',
            'heading': 'Рейсы',
            'columns': ['ddate', 'route', 'train', ],
            'col_headings': ['Дата', 'Номер маршрута', 'Поезд', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        {
            'name': 'stations',
            'heading': 'Станции',
            'columns': ['direction', 'name', 'sub_area', 'distance', ],
            'col_headings': ['Направление', 'Название', 'Приг. зона', 'Километр', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
    ],
    'Менеджер по персоналу': [
        {
            'name': 'posts',
            'heading': 'Должности',
            'columns': ['post', 'salary', ],
            'col_headings': ['Название должности', 'Оклад', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        {
            'name': 'employees',
            'heading': 'Сотрудники',
            'columns': ['tabno', 'post', 'full_name', 'passport', 'birth_date', 'sex', 'snils', 'inn', 'emp_date',
                        'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'ФИО', 'Паспорт', 'Дата рождения', 'Пол', 'СНИЛС', 'ИНН',
                             'Дата приема', 'Дата увольнения', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        # {
        #     'name': 'active_staff',
        #     'heading': 'Активный штат',
        #     'columns': ['tabno', 'post', 'full_name', 'passport', 'birth_date', 'sex', 'snils', 'inn', 'emp_date',
        #                 'quit_date', ],
        #     'col_headings': ['Таб. номер', 'Должность', 'ФИО', 'Паспорт', 'Дата рождения', 'Пол', 'СНИЛС', 'ИНН',
        #                      'Дата приема', 'Дата увольнения', ],
        #     'CREATE': True,
        #     'UPDATE': True,
        #     'DELETE': True
        # },
        # {
        #     'name': 'workload',
        #     'heading': 'Нагрузка машинистов',
        #     'columns': ['route', 'full_name', 'ddate', 'train', ],
        #     'col_headings': ['Номер маршрута', 'Дата', 'ФИО машиниста', 'Поезд'],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
    ],
    'Машинист': [
        # FIXME this will cause a crash unless the view is created and these lines are uncommented
        # {
        #     'name': 'machinist_rides',
        #     'heading': 'Назначенные рейсы',
        #     'columns': ['ddate', 'route', 'train', 'tariff', 'stops'],
        #     'col_headings': ['Дата', 'Номер маршрута', 'Поезд', 'Тип', 'Остановки', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
    ],
    'Директор депо': [
        {
            'name': 'train_models',
            'heading': 'Модели поездов',
            'columns': ['models'],  # TODO model ?
            'col_headings': ['Модель', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        {
            'name': 'trains',
            'heading': 'Поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        # {
        #     'name': 'active_trains',
        #     'heading': 'Активные поезда',
        #     'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
        #     'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
        #     'CREATE': True,
        #     'UPDATE': True,
        #     'DELETE': True
        # },
        # {
        #     'name': 'machinists',  # TODO mb only active ? dunno
        #     'heading': 'Машинисты',
        #     'columns': ['tabno', 'post', 'full_name', 'passport', 'birth_date', 'sex', 'snils', 'inn', 'emp_date',
        #                 'quit_date', ],
        #     'col_headings': ['Таб. номер', 'Должность', 'ФИО', 'Паспорт', 'Дата рождения', 'Пол', 'СНИЛС', 'ИНН',
        #                      'Дата приема', 'Дата увольнения', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
        # {
        #     'name': 'active_machinists',
        #     'heading': 'Активные машинисты',
        #     'columns': ['tabno', 'post', 'full_name', 'passport', 'birth_date', 'sex', 'snils', 'inn', 'emp_date',
        #                 'quit_date', ],
        #     'col_headings': ['Таб. номер', 'Должность', 'ФИО', 'Паспорт', 'Дата рождения', 'Пол', 'СНИЛС', 'ИНН',
        #                      'Дата приема', 'Дата увольнения', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
    ],
    'Менеджер направлений': [
        {
            'name': 'trains',
            'heading': 'Поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
        },
        # {
        #     'name': 'active_trains',
        #     'heading': 'Активные поезда',
        #     'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
        #     'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
        # {
        #     'name': 'machinists',
        #     'heading': 'Машинисты',
        #     'columns': ['tabno', 'post', 'full_name', 'passport', 'birth_date', 'sex', 'snils', 'inn', 'emp_date',
        #                 'quit_date', ],
        #     'col_headings': ['Таб. номер', 'Должность', 'ФИО', 'Паспорт', 'Дата рождения', 'Пол', 'СНИЛС', 'ИНН',
        #                      'Дата приема', 'Дата увольнения', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
        # {
        #     'name': 'active_machinists',
        #     'heading': 'Активные машинисты',
        #     'columns': ['tabno', 'post', 'full_name', 'passport', 'birth_date', 'sex', 'snils', 'inn', 'emp_date',
        #                 'quit_date', ],
        #     'col_headings': ['Таб. номер', 'Должность', 'ФИО', 'Паспорт', 'Дата рождения', 'Пол', 'СНИЛС', 'ИНН',
        #                      'Дата приема', 'Дата увольнения', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
        # {
        #     'name': 'routes_verbose',
        #     'heading': 'Маршруты',
        #     'columns': ['id', 'tariff', 'wdays', 'way', 'stops', ],
        #     'col_headings': ['Номер', 'Тип', 'Режим движения', 'Сторона', 'Остановки'],
        #     'CREATE': True,
        #     'UPDATE': True,
        #     'DELETE': True
        # },
        {
            'name': 'rides',
            'heading': 'Рейсы',
            'columns': ['ddate', 'route', 'train', ],
            'col_headings': ['Дата', 'Номер маршрута', 'Поезд', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        {
            'name': 'stations',
            'heading': 'Станции',
            'columns': ['direction', 'name', 'sub_area', 'distance', ],
            'col_headings': ['Направление', 'Название', 'Приг. зона', 'Километр', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
    ],
}
