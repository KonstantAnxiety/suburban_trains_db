# TODO fill the rest, create new needed views and implement the whole thing
# TODO permission are needed to disable certain elements of the interface
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
        # This is not an actual view or anything, this is just for testing
        {
            'name': 'rides',
            'heading': 'Рейсы',
            'columns': ['ddate', 'route', 'train', ],
            'col_headings': ['Дата', 'Номер маршрута', 'Поезд', ],
            'CREATE': False,
            'UPDATE': False,
            'DELETE': False
        },
        # These are the actual but yet to be created views
        # {
        #     'name': 'rides',
        #     'heading': 'Рейсы',
        #     'columns': ['ddate', 'route', 'from_to', 'train', ],
        #     'col_headings': ['Дата', 'Номер маршрута', 'Маршрут', 'Поезд', ],
        #     'CREATE': False,
        #     'UPDATE': False,
        #     'DELETE': False
        # },
        # {
        #     'name': 'tickets',
        #     'heading': 'Билеты',
        #     'columns': ['payment_date', 'from_to', 'tariff', 'round_trip', 'cashier', ],
        #     'col_headings': ['Дата', 'Станции', 'Тип', 'Туда-обратно', 'Кассир', ],
        #     'CREATE': True,
        #     'UPDATE': False,
        #     'DELETE': True
        # },
    ],
}

# This is the previous format - irrelevant but may be used to fill the thing above
# 'Заведующий направлением': {
#     'trains': [],
#     'active_trains': [],
#     'machinists': [],
#     'active_machinists': [],
#     'routes': [],
#     'rides': [],
#     'stations': [],
# },
# 'Менеджер по персоналу': {
#     'employees': [],
#     'active_staff': [],
#     'workload': [],  # ???
# },
# 'Машинист': {
#     'machinist_rides': [],
# },
# 'Директор депо': {
#     'trains': [],
#     'active_trains': [],
#     'machinists': [],
#     'active_machinists': [],
# },
# 'Менеджер направлений': {
#     'trains': [],
#     'active_trains': [],
#     'machinists': [],
#     'active_machinists': [],
#     'routes': [],
#     'rides': [],
#     'stations': [],
# },
