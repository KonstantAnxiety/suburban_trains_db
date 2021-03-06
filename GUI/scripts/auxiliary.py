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
        {
            'name': 'rides_verbose',
            'heading': 'Расписание',
            'columns': ['ddate', 'train', 'id', 'tariff', 'stops', ],
            'col_headings': ['Дата', 'Номер поезда', 'Номер маршрута', 'Тариф', 'Остановки', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': True
        },
        {
            'name': 'tickets',
            'heading': 'Билеты',
            'columns': ['id', 'cost', 'tariff', 'payment_date', 'round_trip', 'depart_st', 'arrive_st', 'cashier', ],
            'col_headings': ['ID', 'Стоимость', 'Тип', 'Дата', 'Туда-обратно', 'Откуда', 'Куда', 'Кассир', ],
            'CREATE': True,
            'UPDATE': False,
            'DELETE': True,
            'SEARCH': True
        },
    ],
    'Заведующий направлением': [
        {
            'name': 'trains',
            'heading': 'Поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['ID', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
        {
            'name': 'active_trains',
            'heading': 'Активные поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['ID', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
        {
            'name': 'machinists',
            'heading': 'Машинисты',
            'columns': ['tabno', 'post', 'last_name', 'first_name', 'patronymic', 'passport', 'birth_date',
                        'sex', 'snils', 'inn', 'emp_date', 'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Паспорт', 'Дата рождения',
                             'Пол', 'СНИЛС', 'ИНН', 'Дата приема', 'Дата увольнения', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': True
        },
        {
            'name': 'active_machinists',
            'heading': 'Активные машинисты',
            'columns': ['tabno', 'post', 'last_name', 'first_name', 'patronymic', 'birth_date',
                        'sex', 'snils', 'inn', 'emp_date', 'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Паспорт', 'Дата рождения',
                             'Пол', 'СНИЛС', 'ИНН', 'Дата приема', 'Дата увольнения', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': True
        },
        {
            'name': 'manager_routes_verbose',
            'heading': 'Маршруты',
            'columns': ['id', 'tariff', 'wdays', 'way', 'stops', ],
            'col_headings': ['ID', 'Тип', 'Режим движения', 'Сторона', 'Остановки', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'rides',
            'heading': 'Рейсы',
            'columns': ['id', 'ddate', 'route', 'train', 'machinist', ],
            'col_headings': ['ID', 'Дата', 'Номер маршрута', 'Поезд', 'Машинист', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': True
        },
        {
            'name': 'manager_stations',
            'heading': 'Станции направления',
            'columns': ['id', 'name', 'sub_area', 'distance', 'direction', ],
            'col_headings': ['ID', 'Название', 'Приг. зона', 'Километр', 'Направление', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'tickets_stat',
            'heading': 'Статистика билетов',
            'columns': ['tariff', 'amount', 'total', ],
            'col_headings': ['Тариф', 'Количество', 'Общая выручка', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
        {
            'name': 'rides_verbose',
            'heading': 'Расписание',
            'columns': ['ddate', 'train', 'id', 'tariff', 'stops', ],
            'col_headings': ['Дата', 'Номер поезда', 'Номер маршрута', 'Тариф', 'Остановки', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': True
        },
        {
            'name': 'route_stations',
            'heading': 'Станции маршрутов',
            'columns': ['station', 'route', 'arrive_time', ],
            'col_headings': ['Станция', 'Маршрут', 'Время прибытия', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
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
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'employees',
            'heading': 'Сотрудники',
            'columns': ['tabno', 'post', 'last_name', 'first_name', 'patronymic', 'passport', 'birth_date',
                        'sex', 'snils', 'inn', 'emp_date', 'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Паспорт', 'Дата рождения',
                             'Пол', 'СНИЛС', 'ИНН', 'Дата приема', 'Дата увольнения', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': True
        },
        {
            'name': 'active_staff',
            'heading': 'Активный штат',
            'columns': ['tabno', 'post', 'last_name', 'first_name', 'patronymic', 'passport', 'birth_date',
                        'sex', 'snils', 'inn', 'emp_date', 'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Паспорт', 'Дата рождения',
                             'Пол', 'СНИЛС', 'ИНН', 'Дата приема', 'Дата увольнения', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': True
        },
        {
            'name': 'machinist_workload',
            'heading': 'Нагрузка машинистов',
            'columns': ['rt_id', 'machinist', 'ddate', 'tr_id', ],
            'col_headings': ['Номер маршрута', 'Машинист', 'Дата', 'Номер поезда'],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
        {
            'name': 'tickets_stat',
            'heading': 'Статистика билетов',
            'columns': ['tariff', 'amount', 'total', ],
            'col_headings': ['Тариф', 'Количество', 'Общая выручка', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
    ],
    'Машинист': [
        {
            'name': 'machinist_rides',
            'heading': 'Назначенные рейсы',
            'columns': ['ddate', 'train', 'id', 'tariff', 'stops'],
            'col_headings': ['Дата', 'Поезд', 'Номер маршрута', 'Тип', 'Остановки', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
        {
            'name': 'rides_verbose',
            'heading': 'Расписание',
            'columns': ['ddate', 'train', 'id', 'tariff', 'stops', ],
            'col_headings': ['Дата', 'Номер поезда', 'Номер маршрута', 'Тариф', 'Остановки', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': True
        },
    ],
    'Директор депо': [
        {
            'name': 'train_models',
            'heading': 'Модели поездов',
            'columns': ['model'],
            'col_headings': ['Модель', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'trains',
            'heading': 'Поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['ID', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'active_trains',
            'heading': 'Активные поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['ID', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'machinists',
            'heading': 'Машинисты',
            'columns': ['tabno', 'post', 'last_name', 'first_name', 'patronymic', 'passport', 'birth_date',
                        'sex', 'snils', 'inn', 'emp_date', 'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Паспорт', 'Дата рождения',
                             'Пол', 'СНИЛС', 'ИНН', 'Дата приема', 'Дата увольнения', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': True
        },
        {
            'name': 'active_machinists',
            'heading': 'Активные машинисты',
            'columns': ['tabno', 'post', 'last_name', 'first_name', 'patronymic', 'passport', 'birth_date',
                        'sex', 'snils', 'inn', 'emp_date', 'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Паспорт', 'Дата рождения',
                             'Пол', 'СНИЛС', 'ИНН', 'Дата приема', 'Дата увольнения', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': True
        },
    ],
    'Менеджер направлений': [
        {
            'name': 'directions',
            'heading': 'Направления',
            'columns': ['name', 'dcost', 'manager', ],
            'col_headings': ['Название', 'Базовая стоимость', 'Заведующий', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'tariffs',
            'heading': 'Тарифы',
            'columns': ['name', 'coef', ],
            'col_headings': ['Название', 'Множитель стоимости', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'trains',
            'heading': 'Поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['ID', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
        {
            'name': 'active_trains',
            'heading': 'Активные поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['ID', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
        {
            'name': 'machinists',
            'heading': 'Машинисты',
            'columns': ['tabno', 'post', 'last_name', 'first_name', 'patronymic', 'passport', 'birth_date',
                        'sex', 'snils', 'inn', 'emp_date', 'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Паспорт', 'Дата рождения',
                             'Пол', 'СНИЛС', 'ИНН', 'Дата приема', 'Дата увольнения', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': True
        },
        {
            'name': 'active_machinists',
            'heading': 'Активные машинисты',
            'columns': ['tabno', 'post', 'last_name', 'first_name', 'patronymic', 'passport', 'birth_date',
                        'sex', 'snils', 'inn', 'emp_date', 'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Паспорт', 'Дата рождения',
                             'Пол', 'СНИЛС', 'ИНН', 'Дата приема', 'Дата увольнения', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
        {
            'name': 'routes',
            'heading': 'Маршруты',
            'columns': ['id', 'direction', 'tariff', 'wdays', 'way', ],
            'col_headings': ['ID', 'Направление', 'Тип', 'Режим движения', 'Сторона', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'rides',
            'heading': 'Рейсы',
            'columns': ['id', 'ddate', 'route', 'train', 'machinist'],
            'col_headings': ['ID', 'Дата', 'Номер маршрута', 'Поезд', 'Номер машиниста'],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': True
        },
        {
            'name': 'stations',
            'heading': 'Станции',
            'columns': ['id', 'name', 'sub_area', 'distance', 'direction', ],
            'col_headings': ['id', 'Название', 'Приг. зона', 'Километр', 'Направление'],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
        {
            'name': 'tickets_stat',
            'heading': 'Статистика билетов',
            'columns': ['tariff', 'amount', 'total', ],
            'col_headings': ['Тариф', 'Количество', 'Общая выручка', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': False
        },
        {
            'name': 'rides_verbose',
            'heading': 'Расписание',
            'columns': ['ddate', 'train', 'id', 'tariff', 'stops', ],
            'col_headings': ['Дата', 'Номер поезда', 'Номер маршрута', 'Тариф', 'Остановки', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False,
            'SEARCH': True
        },
        {
            'name': 'route_stations',
            'heading': 'Станции маршрутов',
            'columns': ['station', 'route', 'arrive_time', ],
            'col_headings': ['Станция', 'Маршрут', 'Время прибытия', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True,
            'SEARCH': False
        },
    ],
}
