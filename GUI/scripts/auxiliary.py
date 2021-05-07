# TODO fill the rest, create new needed views and implement the whole thing
post_tables = {
    # format
    # Post name: {
    #     Table #1 name: [
    #         (Column #1 name, Column #1 heading),
    #         (Column #2 name, Column #2 heading),
    #         ...
    #     ],
    #     ...
    # },
    'Кассир': {
        'rides': [
            ('ddate', 'Дата'),
            ('route', 'Номер маршрута'),
            ('from_to', 'Маршрут'),  # first and last stations
            ('train', 'Поезд'),
        ],
        'tickets': [
            ('payment_date', 'Дата'),
            ('from_to', 'Станции'),  # depart and arrive stations
            ('tariff', 'Тип'),
            ('round_trip', 'Туда-обратно'),
            ('cashier', 'Кассир'),
        ]
    },
    'Заведующий направлением': {
        'trains': [],
        'active_trains': [],
        'machinists': [],
        'active_machinists': [],
        'routes': [],
        'rides': [],
        'stations': [],
    },
    'Менеджер по персоналу': {
        'employees': [],
        'active_staff': [],
        'workload': [],  # ???
    },
    'Машинист': {
        'machinist_rides': [],
    },
    'Директор депо': {
        'trains': [],
        'acrive_trains': [],
        'machinists': [],
        'active_machinists': [],
    },
    'Менеджер направлений': {
        'trains': [],
        'active_trains': [],
        'machinists': [],
        'active_machinists': [],
        'routes': [],
        'rides': [],
        'stations': [],
    },
}