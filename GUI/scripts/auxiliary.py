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
            'DELETE': False
        },
        {
            'name': 'tickets',
            'heading': 'Билеты',
            'columns': ['payment_date', 'depart_st', 'arrive_st', 'tariff', 'round_trip', 'cashier', 'cost', ],
            'col_headings': ['Дата', 'Откуда', 'Куда', 'Тип', 'Туда-обратно', 'Кассир', 'Стоимость', ],
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
        {
            'name': 'active_trains',
            'heading': 'Активные поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
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
            'DELETE': False
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
            'DELETE': False
        },
        {
            'name': 'manager_routes_verbose',
            'heading': 'Маршруты',
            'columns': ['id', 'tariff', 'wdays', 'way', 'stops', ],
            'col_headings': ['Номер', 'Тип', 'Режим движения', 'Сторона', 'Остановки', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        {
            'name': 'rides',
            'heading': 'Рейсы',
            'columns': ['id', 'ddate', 'route', 'train', 'machinist', ],
            'col_headings': ['ID', 'Дата', 'Номер маршрута', 'Поезд', 'Машинист', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        {
            'name': 'manager_stations',
            'heading': 'Станции направления',
            'columns': ['direction', 'name', 'sub_area', 'distance', ],
            'col_headings': ['Направление', 'Название', 'Приг. зона', 'Километр', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        {
            'name': 'tickets_stat',
            'heading': 'Статистика билетов',
            'columns': ['tariff', 'amount', 'total', ],
            'col_headings': ['Тариф', 'Количество', 'Общая выручка', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
        },
        {
            'name': 'rides_verbose',
            'heading': 'Расписание',
            'columns': ['ddate', 'train', 'id', 'tariff', 'stops', ],
            'col_headings': ['Дата', 'Номер поезда', 'Номер маршрута', 'Тариф', 'Остановки', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
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
            'columns': ['tabno', 'post', 'last_name', 'first_name', 'patronymic', 'passport', 'birth_date',
                        'sex', 'snils', 'inn', 'emp_date', 'quit_date', ],
            'col_headings': ['Таб. номер', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Паспорт', 'Дата рождения',
                             'Пол', 'СНИЛС', 'ИНН', 'Дата приема', 'Дата увольнения', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
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
            'DELETE': True
        },
        {
            'name': 'machinist_workload',
            'heading': 'Нагрузка машинистов',
            'columns': ['rt_id', 'ddate', 'machinist', 'tr_id', ],
            'col_headings': ['Номер маршрута', 'Дата', 'Машинист', 'Номер поезда'],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
        },
        {
            'name': 'tickets_stat',
            'heading': 'Статистика билетов',
            'columns': ['tariff', 'amount', 'total', ],
            'col_headings': ['Тариф', 'Количество', 'Общая выручка', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
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
            'DELETE': False
        },
        {
            'name': 'rides_verbose',
            'heading': 'Расписание',
            'columns': ['ddate', 'train', 'id', 'tariff', 'stops', ],
            'col_headings': ['Дата', 'Номер поезда', 'Номер маршрута', 'Тариф', 'Остановки', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
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
        {
            'name': 'active_trains',
            'heading': 'Активные поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
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
            'DELETE': False
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
            'DELETE': False
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
            'DELETE': True
        },
        {
            'name': 'tariffs',
            'heading': 'Тарифы',
            'columns': ['name', 'coef', ],
            'col_headings': ['Название', 'Множитель стоимости', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
        {
            'name': 'trains',
            'heading': 'Поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
        },
        {
            'name': 'active_trains',
            'heading': 'Активные поезда',
            'columns': ['id', 'model', 'serv_start_date', 'serv_end_date', ],
            'col_headings': ['Номер', 'Модель', 'Введен в эксплуатацию', 'Списан', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
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
            'DELETE': False
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
            'DELETE': False
        },
        {
            'name': 'routes',
            'heading': 'Маршруты',
            'columns': ['id', 'tariff', 'wdays', 'way', ],
            'col_headings': ['Номер', 'Тип', 'Режим движения', 'Сторона', ],
            'CREATE': True,
            'UPDATE': True,
            'DELETE': True
        },
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
        {
            'name': 'tickets_stat',
            'heading': 'Статистика билетов',
            'columns': ['tariff', 'amount', 'total', ],
            'col_headings': ['Тариф', 'Количество', 'Общая выручка', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
        },
        {
            'name': 'rides_verbose',
            'heading': 'Расписание',
            'columns': ['ddate', 'train', 'id', 'tariff', 'stops', ],
            'col_headings': ['Дата', 'Номер поезда', 'Номер маршрута', 'Тариф', 'Остановки', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
        },
    ],
}
