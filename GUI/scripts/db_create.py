# from GUI.scripts.db_config import db

CREATE_DATABASE = [
    """CREATE TABLE IF NOT EXISTS posts (
        post   VARCHAR(30) CONSTRAINT pk_posts PRIMARY KEY,
        salary NUMERIC(9, 2) NOT NULL,
            CONSTRAINT check_salary CHECK (SALARY >= 12000)
    );
    """,

    """CREATE TABLE IF NOT EXISTS employees (
        tabno      VARCHAR(30) CONSTRAINT pk_employees PRIMARY KEY,
        post       VARCHAR(30) CONSTRAINT ref_posts REFERENCES posts,
        full_name  VARCHAR(40) NOT NULL,
        passport   VARCHAR(40) NOT NULL,
        birth_date DATE NOT NULL,
        sex        CHAR(1) NOT NULL DEFAULT 'м',
            CONSTRAINT check_sex CHECK (sex IN ('м', 'ж')),
        snils      CHAR(11) NOT NULL,
        inn        CHAR(12) NOT NULL,
        emp_date   DATE NOT NULL,
        quit_date  DATE
    );
    """,

    """CREATE TABLE IF NOT EXISTS directions (
        name    VARCHAR(40) CONSTRAINT pk_directions PRIMARY KEY,
        dcost   NUMERIC(6, 2) NOT NULL,
            CONSTRAINT check_dcost CHECK (dcost > 0),
        manager VARCHAR(30) CONSTRAINT ref_manager REFERENCES employees
    );
    """,

    """ CREATE TABLE IF NOT EXISTS stations (
        id        NUMERIC(6) CONSTRAINT pk_stations PRIMARY KEY,
        name      VARCHAR(40) NOT NULL,
        sub_area  NUMERIC(2) NOT NULL,
        distance  NUMERIC(3) NOT NULL,
        direction VARCHAR(40) CONSTRAINT ref_direction REFERENCES directions
    );
    """,

    """CREATE TABLE IF NOT EXISTS tariffs (
        name VARCHAR(20) CONSTRAINT pk_tariffs PRIMARY KEY,
        coef NUMERIC(3, 2) NOT NULL,
            CONSTRAINT check_coef CHECK (coef > 0)
    );
    """,

    """CREATE TABLE IF NOT EXISTS routes (
        id     NUMERIC(6) CONSTRAINT pk_routes PRIMARY KEY,
        tariff VARCHAR(15) CONSTRAINT ref_route_tariff REFERENCES tariffs,
        wdays  VARCHAR(15) NOT NULL DEFAULT 'ежедневно',
            CONSTRAINT check_wdays
            CHECK (wdays IN ('ежедневно', 'по рабочим', 'по выходным')),
        way    VARCHAR(10) NOT NULL DEFAULT 'в город',
            CONSTRAINT check_way
            CHECK (way IN ('в город', 'из города'))
    );
    """,

    """CREATE TABLE IF NOT EXISTS route_stations (
        station     NUMERIC(6) CONSTRAINT ref_rout_st_st REFERENCES stations,
        route       NUMERIC(6) CONSTRAINT ref_rout_st_rout REFERENCES routes,
        arrive_time TIME WITHOUT TIME ZONE NOT NULL,
        PRIMARY KEY(station, route)
    );
    """,

    """CREATE TABLE IF NOT EXISTS train_models (
        models VARCHAR(20) CONSTRAINT pk_models PRIMARY KEY
    );
    """,

    """CREATE TABLE IF NOT EXISTS trains (
        id              NUMERIC(6) CONSTRAINT pk_trains PRIMARY KEY,
        model           VARCHAR(20) CONSTRAINT ref_models REFERENCES train_models,
        serv_start_date DATE NOT NULL,
        serv_end_date   DATE
    );
    """,

    """CREATE TABLE IF NOT EXISTS rides (
        id        NUMERIC(6) CONSTRAINT pk_rides PRIMARY KEY,
        ddate     TIMESTAMP NOT NULL,
        route     NUMERIC(6) CONSTRAINT ref_route_ride REFERENCES routes,
        train     NUMERIC(6) CONSTRAINT ref_train REFERENCES trains,
        machinist VARCHAR(30) CONSTRAINT ref_machinist REFERENCES employees
    );
    """,

    """CREATE TABLE IF NOT EXISTS tickets (
        id           NUMERIC(6) CONSTRAINT pk_tickets PRIMARY KEY,
        cost         NUMERIC(6, 2) NOT NULL,
            CONSTRAINT check_cost CHECK (cost >= 0),
        tariff VARCHAR(15) CONSTRAINT ref_route_tariff REFERENCES tariffs,
        payment_date TIMESTAMP NOT NULL,
        round_trip   NUMERIC(1) NOT NULL DEFAULT 0,
            CONSTRAINT check_round_trip CHECK (round_trip IN (0, 1)),
        depart_st    NUMERIC(6) CONSTRAINT ref_dep_st REFERENCES stations,
        arrive_st    NUMERIC(6) CONSTRAINT ref_arrive_st REFERENCES stations,
        cashier      VARCHAR(30) CONSTRAINT ref_cashier REFERENCES employees
    );
    """
]

# for table in CREATE_DATABASE:
#     db.execute(table)
