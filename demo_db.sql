-- Демо БД

--TABLES===================================================================================
CREATE TABLE posts (
    post   VARCHAR(30) CONSTRAINT pk_posts PRIMARY KEY,
    salary NUMERIC(9, 2) NOT NULL,
        CONSTRAINT check_salary CHECK (SALARY >= 12000)
);

CREATE TABLE IF NOT EXISTS employees (
    tabno      VARCHAR(30) CONSTRAINT pk_employees PRIMARY KEY,
    post       VARCHAR(30) NOT NULL CONSTRAINT ref_posts REFERENCES posts,
    last_name  VARCHAR(20) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    patronymic VARCHAR(20) NOT NULL,
    passport   VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,
    sex        CHAR(1) NOT NULL DEFAULT 'м',
        CONSTRAINT check_sex CHECK (sex IN ('м', 'ж')),
    snils      CHAR(11) NOT NULL,
    inn        CHAR(12) NOT NULL,
    emp_date   DATE NOT NULL,
    quit_date  DATE
);

CREATE TABLE directions (
    name    VARCHAR(20) CONSTRAINT pk_directions PRIMARY KEY,
    dcost   NUMERIC(6, 2) NOT NULL,
        CONSTRAINT check_dcost CHECK (dcost > 0),
    manager VARCHAR(30) CONSTRAINT ref_manager REFERENCES employees
);

CREATE TABLE IF NOT EXISTS stations (
    id        NUMERIC(6) CONSTRAINT pk_stations PRIMARY KEY,
    name      VARCHAR(30) NOT NULL,
    sub_area  NUMERIC(2) NOT NULL,
    distance  NUMERIC(3) NOT NULL,
    direction VARCHAR(20) CONSTRAINT ref_direction REFERENCES directions,
    UNIQUE (name, direction)
);

CREATE TABLE tariffs (
    name VARCHAR(20) CONSTRAINT pk_tariffs PRIMARY KEY,
    coef NUMERIC(3, 2) NOT NULL,
        CONSTRAINT check_coef CHECK (coef > 0)
);

CREATE TABLE routes (
    id        NUMERIC(6) CONSTRAINT pk_routes PRIMARY KEY,
    direction VARCHAR(20) NOT NULL CONSTRAINT ref_direction REFERENCES directions,
    tariff    VARCHAR(15) NOT NULL CONSTRAINT ref_route_tariff REFERENCES tariffs,
    wdays     VARCHAR(15) NOT NULL DEFAULT 'ежедневно',
        CONSTRAINT check_wdays
        CHECK (wdays IN ('ежедневно', 'по рабочим', 'по выходным')),
    way       VARCHAR(10) NOT NULL DEFAULT 'в город',
        CONSTRAINT check_way
        CHECK (way IN ('в город', 'из города'))
);

CREATE TABLE IF NOT EXISTS route_stations (
    station     NUMERIC(6) CONSTRAINT ref_rout_st_st REFERENCES stations,
    route       NUMERIC(6) CONSTRAINT ref_rout_st_rout REFERENCES routes,
    arrive_time TIME WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY(station, route)
);

CREATE TABLE train_models (
    model VARCHAR(20) CONSTRAINT pk_models PRIMARY KEY
);

CREATE TABLE trains (
    id              NUMERIC(6) CONSTRAINT pk_trains PRIMARY KEY,
    model           VARCHAR(20) NOT NULL CONSTRAINT ref_models REFERENCES train_models,
    serv_start_date DATE NOT NULL,
    serv_end_date   DATE
);

CREATE TABLE rides (
    id        NUMERIC(6) CONSTRAINT pk_rides PRIMARY KEY,
    ddate     TIMESTAMP NOT NULL,
    route     NUMERIC(6) NOT NULL CONSTRAINT ref_route_ride REFERENCES routes,
    train     NUMERIC(6) NOT NULL CONSTRAINT ref_train REFERENCES trains,
    machinist VARCHAR(30) NOT NULL CONSTRAINT ref_machinist REFERENCES employees
);

CREATE TABLE tickets (
    id           NUMERIC(6) CONSTRAINT pk_tickets PRIMARY KEY,
    cost         NUMERIC(6, 2) NOT NULL,
    tariff       VARCHAR(15) NOT NULL CONSTRAINT ref_route_tariff REFERENCES tariffs,
    payment_date TIMESTAMP NOT NULL,
    round_trip   NUMERIC(1) NOT NULL DEFAULT 0,
        CONSTRAINT check_round_trip CHECK (round_trip IN (0, 1)),
    depart_st    NUMERIC(6) NOT NULL CONSTRAINT ref_dep_st REFERENCES stations,
    arrive_st    NUMERIC(6) NOT NULL CONSTRAINT ref_arrive_st REFERENCES stations,
    cashier      VARCHAR(30) NOT NULL CONSTRAINT ref_cashier REFERENCES employees
);
 
--VIEWS===================================================================================

CREATE OR REPLACE VIEW active_staff AS
    SELECT * FROM employees
    WHERE emp_date <= current_date AND
        (quit_date IS NULL OR quit_date IS NOT NULL AND current_date <= quit_date);

CREATE OR REPLACE VIEW machinists AS
    SELECT * FROM employees
    WHERE post = 'Машинист';

CREATE OR REPLACE VIEW cashiers AS
    SELECT * FROM employees
    WHERE post = 'Кассир';
 
CREATE OR REPLACE VIEW route_managers AS
    SELECT * FROM employees
    WHERE post = 'Заведующий направлением';
 

CREATE OR REPLACE VIEW active_machinists AS
    SELECT * FROM active_staff
    WHERE post = 'Машинист';

CREATE OR REPLACE VIEW manager_routes_verbose AS
    SELECT rt.id, rt.direction, rt.tariff, rt.wdays, rt.way,
            CASE WHEN EXISTS (SELECT * FROM route_stations WHERE route = rt.id) THEN 
                (SELECT STRING_AGG(st.name, ', ' ORDER BY
                           CASE WHEN rt.way = 'из города' THEN st.distance END ASC,
                           CASE WHEN rt.way = 'в город' THEN st.distance END DESC)
                     FROM route_stations AS rs, stations AS st  
                     WHERE rs.station = st.id AND rs.route = rt.id)
                 ELSE '-'
            END
        FROM directions AS d, routes AS rt
        WHERE d.manager = user AND rt.direction = d.name
        GROUP BY rt.id;
ALTER VIEW manager_routes_verbose RENAME COLUMN "case" TO stops;

CREATE OR REPLACE VIEW machinist_workload AS
    SELECT rt.id AS rt_id, emp.last_name || ' ' || emp.first_name || ' ' || emp.patronymic AS machinist, rd.ddate, tr.id AS tr_id
        FROM routes AS rt, employees AS emp, rides AS rd, trains AS tr
        WHERE rd.machinist = emp.tabno AND rd.route = rt.id AND rd.train = tr.id
    ORDER BY rd.ddate;

CREATE OR REPLACE VIEW active_trains AS
    SELECT * FROM trains
    WHERE serv_start_date <= current_date AND
        (serv_end_date IS NULL OR serv_end_date IS NOT NULL AND current_date <= serv_end_date);
 
CREATE OR REPLACE VIEW rides_verbose AS
    SELECT DISTINCT rides.ddate, rides.train, r.id, r.tariff,
            STRING_AGG(s.name, ', ' ORDER BY
                CASE WHEN r.way = 'из города' THEN s.distance END ASC,
                CASE WHEN r.way = 'в город' THEN s.distance END DESC)
        FROM directions AS d, stations AS s, route_stations AS rs, routes AS r, rides
        WHERE s.direction = d.name AND
            rs.station = s.id AND r.id = rs.route AND r.id = rides.route
    GROUP BY rides.ddate, rides.train, r.id;
ALTER VIEW rides_verbose RENAME COLUMN string_agg TO stops;
 
CREATE OR REPLACE VIEW machinist_rides AS
    SELECT DISTINCT rides.ddate, rides.train, r.id, r.tariff,
            STRING_AGG(s.name, ', ' ORDER BY
                CASE WHEN r.way = 'из города' THEN s.distance END ASC,
                CASE WHEN r.way = 'в город' THEN s.distance END DESC)
        FROM directions AS d, stations AS s,
            route_stations AS rs, routes AS r, rides
        WHERE rides.machinist = user AND s.direction = d.name AND
            rs.station = s.id AND r.id = rs.route AND
            r.id = rides.route AND rides.ddate >= current_timestamp 
    GROUP BY rides.ddate, rides.train, r.id;
ALTER VIEW machinist_rides RENAME COLUMN string_agg TO stops;
 
CREATE OR REPLACE VIEW manager_stations AS
    SELECT * FROM stations
    WHERE direction IN (SELECT name FROM directions WHERE manager = user);
 
CREATE OR REPLACE VIEW tickets_stat AS
    SELECT name AS tariff,
            (SELECT COUNT(*) FROM tickets AS tc
                WHERE tc.tariff = tr.name) AS amount,
            (SELECT COALESCE(SUM(tc.cost), 0) FROM tickets AS tc
                WHERE tc.tariff = tr.name) AS total
        FROM tariffs AS tr;
 
--USERS AND TABLE PERMISSIONS===============================================================
 
-- CREATE USER e1001 WITH PASSWORD '132132';
GRANT SELECT ON stations TO e1001;
GRANT SELECT ON routes TO e1001;
GRANT SELECT ON route_stations TO e1001;
GRANT SELECT ON directions TO e1001;
GRANT SELECT, INSERT, DELETE ON tickets TO e1001;
GRANT SELECT ON tariffs TO e1001;
GRANT SELECT ON posts TO e1001;
GRANT SELECT ON employees TO e1001;
GRANT SELECT ON rides TO e1001;

-- CREATE USER e201001 WITH PASSWORD '132132';
GRANT SELECT, INSERT, UPDATE, DELETE ON stations TO e201001;
GRANT SELECT, INSERT, UPDATE, DELETE ON routes TO e201001;
GRANT SELECT, INSERT, UPDATE, DELETE ON route_stations TO e201001;
GRANT SELECT ON directions TO e201001;
GRANT SELECT ON tickets TO e201001;
GRANT SELECT ON tariffs TO e201001;
GRANT SELECT ON posts TO e201001;
GRANT SELECT ON employees TO e201001;
GRANT SELECT, INSERT, UPDATE, DELETE ON rides TO e201001;
GRANT SELECT ON train_models TO e201001;
GRANT SELECT ON trains TO e201001;

-- CREATE USER e202001 WITH PASSWORD '132132';
GRANT SELECT, INSERT, UPDATE, DELETE ON stations TO e202001;
GRANT SELECT, INSERT, UPDATE, DELETE ON routes TO e202001;
GRANT SELECT, INSERT, UPDATE, DELETE ON route_stations TO e202001;
GRANT SELECT ON directions TO e202001;
GRANT SELECT ON tickets TO e202001;
GRANT SELECT ON tariffs TO e202001;
GRANT SELECT ON posts TO e202001;
GRANT SELECT ON employees TO e202001;
GRANT SELECT, INSERT, UPDATE, DELETE ON rides TO e202001;
GRANT SELECT ON train_models TO e202001;
GRANT SELECT ON trains TO e202001;

-- CREATE USER e3001 WITH PASSWORD '132132';
GRANT SELECT, INSERT, UPDATE, DELETE ON posts TO e3001;
GRANT SELECT, INSERT, UPDATE, DELETE ON employees TO e3001;
GRANT SELECT ON rides TO e3001;

-- CREATE USER e4001 WITH PASSWORD '132132';
GRANT SELECT ON stations TO e4001;
GRANT SELECT ON routes TO e4001;
GRANT SELECT ON route_stations TO e4001;
GRANT SELECT ON posts TO e4001;
GRANT SELECT ON employees TO e4001;
GRANT SELECT ON rides TO e4001;
GRANT SELECT ON train_models TO e4001;
GRANT SELECT ON trains TO e4001;

-- CREATE USER e5001 WITH PASSWORD '132132';
GRANT SELECT ON posts TO e5001;
GRANT SELECT ON employees TO e5001;
GRANT SELECT ON rides TO e5001;
GRANT SELECT, INSERT, UPDATE, DELETE ON train_models TO e5001;
GRANT SELECT, INSERT, UPDATE, DELETE ON trains TO e5001;

-- CREATE USER e6001 WITH PASSWORD '132132';
GRANT SELECT, INSERT, UPDATE, DELETE ON stations TO e6001;
GRANT SELECT, INSERT, UPDATE, DELETE ON routes TO e6001;
GRANT SELECT, INSERT, UPDATE, DELETE ON route_stations TO e6001;
GRANT SELECT, INSERT, UPDATE, DELETE ON directions TO e6001;
GRANT SELECT ON tickets TO e6001;
GRANT SELECT, INSERT, UPDATE, DELETE ON tariffs TO e6001;
GRANT SELECT ON posts TO e6001;
GRANT SELECT ON employees TO e6001;
GRANT SELECT, INSERT, UPDATE, DELETE ON rides TO e6001;
GRANT SELECT ON train_models TO e6001;
GRANT SELECT ON trains TO e6001;
 
--VIEW PERMISSIONS========================================================================
GRANT SELECT ON cashiers TO e1001;
GRANT SELECT ON rides_verbose TO e1001;
 
GRANT SELECT ON machinists TO e201001;
GRANT SELECT ON active_machinists TO e201001;
GRANT SELECT, INSERT, UPDATE, DELETE ON manager_routes_verbose TO e201001;
GRANT SELECT ON machinist_workload TO e201001;
GRANT SELECT, INSERT, UPDATE, DELETE ON manager_stations TO e201001;
GRANT SELECT ON active_trains TO e201001;
GRANT SELECT ON tickets_stat TO e201001;
GRANT SELECT ON rides_verbose TO e201001;

GRANT SELECT ON machinists TO e202001;
GRANT SELECT ON active_machinists TO e202001;
GRANT SELECT, INSERT, UPDATE, DELETE ON manager_routes_verbose TO e202001;
GRANT SELECT ON machinist_workload TO e202001;
GRANT SELECT, INSERT, UPDATE, DELETE ON manager_stations TO e202001;
GRANT SELECT ON active_trains TO e202001;
GRANT SELECT ON tickets_stat TO e202001;
GRANT SELECT ON rides_verbose TO e202001;

GRANT SELECT, INSERT, UPDATE, DELETE ON active_staff TO e3001;
GRANT SELECT, INSERT, UPDATE, DELETE ON machinists TO e3001;
GRANT SELECT, INSERT, UPDATE, DELETE ON active_machinists TO e3001;
GRANT SELECT ON machinist_workload TO e3001;
GRANT SELECT ON tickets_stat TO e3001;

GRANT SELECT ON machinist_rides TO e4001;
GRANT SELECT ON active_trains TO e4001;
GRANT SELECT ON rides_verbose TO e4001;

GRANT SELECT ON machinists TO e5001;
GRANT SELECT ON active_machinists TO e5001;
GRANT SELECT ON machinist_workload TO e5001;
GRANT SELECT, INSERT, UPDATE, DELETE ON active_trains TO e5001;

GRANT SELECT ON machinists TO e6001;
GRANT SELECT ON active_machinists TO e6001;
GRANT SELECT ON machinist_workload TO e6001;
GRANT SELECT ON active_trains TO e6001;
GRANT SELECT ON tickets_stat TO e6001;
GRANT SELECT ON route_managers TO e6001;
GRANT SELECT ON rides_verbose TO e6001;
 

--TRIGGERS===================================================================================
CREATE OR REPLACE FUNCTION manage_ticket() RETURNS TRIGGER AS $$ 
DECLARE 
    dzone INTEGER;
    st1 RECORD;
    st2 RECORD;
    coef tariffs.coef%TYPE;
    dcost directions.dcost%TYPE;
    total tickets.cost%TYPE;
BEGIN
    IF new.depart_st = new.arrive_st THEN
        RAISE EXCEPTION 'Не удалось добавить билет: станции отправления и назначения совпадают.';
    END IF;
    SELECT direction, sub_area INTO st1 FROM stations WHERE id = new.depart_st;
    SELECT direction, sub_area INTO st2 FROM stations WHERE id = new.arrive_st;
    IF st1.direction <> st2.direction THEN
        RAISE EXCEPTION 'Не удалось добавить билет: станции разных направлений.';
    END IF;
    IF NOT EXISTS (SELECT * FROM route_stations AS rs1
                       WHERE station = new.arrive_st AND
                           EXISTS (SELECT * FROM route_stations AS rs2 WHERE
                                       rs1.route = rs2.route AND
                                       rs2.station = new.depart_st AND
                                       (rs1.arrive_time > rs2.arrive_time OR
                                           (rs1.arrive_time > '16:00'
                                            AND rs2.arrive_time < '8:00')
                                       )
                                  )
                  ) THEN
        RAISE EXCEPTION 'Не удалось добавить билет: станции не соединены ни одним маршрутом.';                         
    END IF;
    SELECT directions.dcost INTO dcost FROM directions WHERE name = st1.direction;
    SELECT tariffs.coef INTO STRICT coef FROM tariffs WHERE name = new.tariff;

    dzone = ABS(st1.sub_area - st2.sub_area);
    total = dcost * coef * (new.round_trip + 1);
    IF dzone > 1 THEN
        total = total * dzone;
    END IF;
    new.cost = total;
    new.payment_date = current_timestamp;
    new.cashier = user;
    RETURN new;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE EXCEPTION 'Недопустимый тариф: %', new.tariff;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER manage_ticket_tg
    BEFORE INSERT OR UPDATE ON tickets
    FOR EACH ROW 
    EXECUTE PROCEDURE manage_ticket();

CREATE OR REPLACE FUNCTION edit_routes() RETURNS TRIGGER AS $$ 
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO routes VALUES (new.id, new.direction, new.tariff, new.wdays, new.way);
    ELSE
        UPDATE routes SET id = new.id, direction = new.direction, tariff = new.tariff,
            wdays = new.wdays, way = new.way WHERE id = old.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER edit_routes_tg 
    INSTEAD OF INSERT OR UPDATE ON manager_routes_verbose
    FOR EACH ROW 
    EXECUTE PROCEDURE edit_routes();

CREATE OR REPLACE FUNCTION check_route_station() RETURNS TRIGGER AS $$ 
DECLARE
    d1 directions.name%TYPE;
    d2 directions.name%TYPE;
BEGIN
    SELECT direction INTO d1 FROM stations where id = new.station;
    SELECT direction INTO d2 FROM routes where id = new.route;
    IF d1 <> d2 THEN
        RAISE EXCEPTION 'Станция и маршрут должны относиться к одному направлению: % != %', d1, d2;
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_route_station_tr 
    BEFORE INSERT OR UPDATE ON route_stations
    FOR EACH ROW 
    EXECUTE PROCEDURE check_route_station();
 
CREATE OR REPLACE FUNCTION check_route_dir_stations() RETURNS TRIGGER AS $$
BEGIN
    IF new.direction <> old.direction AND
            EXISTS (SELECT * FROM route_stations WHERE route = new.id)THEN
        RAISE EXCEPTION 'Не удалось изменить направление: маршрут все еще содержит станции другого направления.';
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_route_dir_stations_tr
    BEFORE UPDATE ON routes
    FOR EACH ROW 
    EXECUTE PROCEDURE check_route_dir_stations();

CREATE OR REPLACE FUNCTION check_manager() RETURNS TRIGGER AS $$
DECLARE
    m RECORD;
BEGIN
    IF new.manager IS NOT NULL THEN
        SELECT post, emp_date, quit_date INTO m FROM employees WHERE tabno = new.manager;
        IF m.post <> 'Заведующий направлением' OR NOT (m.emp_date <= current_date AND
                (m.quit_date IS NULL OR m.quit_date IS NOT NULL AND current_date <= m.quit_date)) THEN
            RAISE EXCEPTION 'Может быть назначен только активный сотрудник должности "Заведующий направлением".';
        END IF;
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;
 
CREATE TRIGGER check_manager_tr
    BEFORE INSERT OR UPDATE ON directions
    FOR EACH ROW 
    EXECUTE PROCEDURE check_manager();

CREATE OR REPLACE FUNCTION check_manager_emp() RETURNS TRIGGER AS $$ 
BEGIN
    IF old.post = 'Заведующий направлением' AND new.post <> old.post AND
            EXISTS (SELECT * FROM directions WHERE manager = old.tabno) THEN
        RAISE EXCEPTION 'Не удалось поменять должность: сотрудник все еще является заведующим направления.';
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_manager_emp_tr 
    BEFORE UPDATE ON employees
    FOR EACH ROW 
    EXECUTE PROCEDURE check_manager_emp();

CREATE OR REPLACE FUNCTION ride_end(route_in rides.route%TYPE, ddate_in rides.ddate%TYPE)
RETURNS rides.ddate%TYPE AS $$
DECLARE
    r RECORD;
    way routes.way%TYPE;
    dist stations.distance%TYPE;
    t_end route_stations.arrive_time%TYPE;
BEGIN
    SELECT routes.way INTO way FROM routes WHERE id = route_in;
    SELECT CASE way
               WHEN 'в город' THEN MIN(distance)
               ELSE MAX(distance)
           END
        INTO dist
        FROM route_stations AS rs, stations AS st
        WHERE rs.station = st.id AND rs.route = route_in;
    SELECT arrive_time INTO t_end FROM stations AS st, route_stations AS rs
        WHERE rs.station = st.id AND rs.route = route_in AND distance = dist;
    IF EXTRACT(hour from ddate_in) > 16 AND t_end < '8:00' THEN
        RETURN DATE(ddate_in + '1 day') + t_end;
    ELSE
        RETURN DATE(ddate_in) + t_end;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_ride() RETURNS TRIGGER AS $$
DECLARE
    t RECORD;
    m RECORD;
    wdays routes.wdays%TYPE;
BEGIN
    IF new.train IS NOT NULL THEN
        SELECT serv_start_date, serv_end_date INTO STRICT t FROM trains WHERE id = new.train;
        IF NOT (t.serv_start_date <= current_date AND 
                (t.serv_end_date IS NULL OR t.serv_end_date IS NOT NULL AND current_date <= t.serv_end_date)) THEN
            RAISE EXCEPTION 'Может быть назначен только действующий поезд.';
        END IF;
    END IF;
    IF new.machinist IS NOT NULL THEN
        SELECT emp_date, quit_date, post INTO STRICT m FROM employees WHERE tabno = new.machinist;
        IF m.post <> 'Машинист' OR NOT (m.emp_date <= current_date AND
                (m.quit_date IS NULL OR m.quit_date IS NOT NULL
                     AND current_date <= m.quit_date)) THEN
            RAISE EXCEPTION 'Может быть назначен только действующий сотрудник должности "Машинист".';
        END IF;
    END IF;
    IF NOT EXISTS (SELECT * FROM route_stations WHERE route = new.route) THEN
        RAISE EXCEPTION 'Не удалось внести изменения: маршрут не содержит станций';
    END IF;
    SELECT routes.wdays INTO STRICT wdays FROM routes WHERE id = new.route;
    CASE wdays
        WHEN 'по рабочим' THEN
            IF EXTRACT(dow FROM new.ddate) NOT IN (1, 2, 3, 4, 5) THEN
                RAISE EXCEPTION 'День недели не соответствует режиму движения: %', wdays;
            END IF;
        WHEN 'по выходным' THEN
            IF EXTRACT(dow FROM new.ddate) NOT IN (6, 0) THEN
                RAISE EXCEPTION 'День недели не соответствует режиму движения: %', wdays;
            END IF;
    END CASE;
    IF EXISTS (SELECT * FROM rides WHERE id <> new.id AND
                   (machinist = new.machinist OR train = new.train) AND
                   (new.ddate BETWEEN ddate AND ride_end(route, ddate) OR
                    ddate BETWEEN new.ddate AND ride_end(new.route, new.ddate))) THEN
        RAISE EXCEPTION 'Не удалось внести изменения: рейсы машиниста или поезда пересекаются.';
    END IF;
    RETURN new;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        IF t IS NULL THEN
            RAISE EXCEPTION 'Не удалось найти поезд %', new.train;
        ELSIF m IS NULL THEN
            RAISE EXCEPTION 'Не удалось найти сотрудника %', new.machinist;
        ELSIF wdays IS NULL THEN
            RAISE EXCEPTION 'Не удалось найти маршрут %', new.route;
        END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_ride_tr 
    BEFORE INSERT OR UPDATE ON rides
    FOR EACH ROW 
    EXECUTE PROCEDURE check_ride();
 
CREATE OR REPLACE FUNCTION check_machinist_emp() RETURNS TRIGGER AS $$ 
BEGIN
    IF old.post = 'Машинист' AND new.post <> old.post AND
            EXISTS (SELECT * FROM rides WHERE machinist = old.tabno AND ddate >= current_timestamp) THEN
        RAISE EXCEPTION 'Не удалось поменять должность: машинист назначен на будущий рейс.';
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_machinist_emp_tr 
    BEFORE UPDATE ON employees
    FOR EACH ROW 
    EXECUTE PROCEDURE check_machinist_emp();

CREATE OR REPLACE FUNCTION check_train_upd() RETURNS TRIGGER AS $$
BEGIN
    IF (old.serv_end_date IS NULL AND new.serv_end_date IS NOT NULL OR
            old.serv_end_date IS NOT NULL AND old.serv_end_date <> new.serv_end_date) AND
            EXISTS (SELECT * FROM rides WHERE train = new.id AND ddate >= new.serv_end_date) THEN
        RAISE EXCEPTION 'Не удалось изменить дату: поезд все еще назначен на будущий рейс.';
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_train_upd_tr 
    BEFORE UPDATE ON trains
    FOR EACH ROW 
    EXECUTE PROCEDURE check_train_upd();
 
--DEMO DATA================================================================================
 
INSERT INTO tariffs VALUES
    ('экспресс', 2),
    ('стандарт', 1);

INSERT INTO posts VALUES ('Заведующий направлением', 90000),
                         ('Кассир', 40000),
                         ('Менеджер по персоналу', 60000),
                         ('Машинист', 60000),
                         ('Директор депо', 70000),
                         ('Менеджер направлений', 80000);

INSERT INTO employees VALUES
    ('e1001', 'Кассир', 'Данилова', 'Екатерина', 'Дмитриевна', '4571500200', '07.11.1976', 'ж', '37604187288', '321590142255', '15.06.2008', NULL),
    ('e201001', 'Заведующий направлением', 'Черкасов', 'Макар', 'Маратович', '4399425802', '12.12.1972', 'м', '88236665452', '048194724200', '14.06.2015', NULL),
    ('e202001', 'Заведующий направлением', 'Волкова', 'Екатерина', 'Кирилловна', '4358984652', '07.02.1980', 'ж', '49872292154', '315646584298', '11.02.2010', NULL),
    ('e3001', 'Менеджер по персоналу', 'Воронкова', 'София', 'Кирилловна', '4611199485', '24.12.1969', 'ж', '92156685323', '798165959880', '02.03.2016', NULL),
    ('e4001', 'Машинист', 'Логинов', 'Матвей', 'Владиславович', '4612489987', '01.11.1989', 'м', '82448362618', '236306538320', '27.06.2017', NULL),
    ('e5001', 'Директор депо', 'Морозов', 'Владислав', 'Тимофеевич', '4623599311', '15.03.1988', 'м', '86483264447', '116394559160', '30.08.2015', NULL),
    ('e6001', 'Менеджер направлений', 'Виноградов', 'Егор', 'Артёмович', '4610023540', '14.03.1995', 'м', '38596721650', '462794651109', '10.11.2020', NULL);


INSERT INTO directions VALUES ('Павелецкое', 40, NULL),
                              ('Одинцовское', 36, 'e201001'),
                              ('Ярославское', 26, 'e202001');

INSERT INTO stations VALUES (1, 'Москва Ярославская', 0, 0, 'Ярославское'),
                            (3, 'Москва-3', 1, 3, 'Ярославское'),
                            (4, 'Маленковская', 1, 5, 'Ярославское'),
                            (7, 'Ростокино (бывш. Северянин)', 2, 8, 'Ярославское'),
                            (8, 'Лосиноостровская', 2, 10, 'Ярославское'),
                            (13, 'Мытищи', 3, 17, 'Ярославское'),
                            (28, 'Пушкино', 4, 29, 'Ярославское'),
                            (200, 'Москва Павелецкая', 0, 0, 'Павелецкое'),
                            (201, 'ЗИЛ', 1, 4, 'Павелецкое'),
                            (202, 'Чертаново', 2, 10, 'Павелецкое'),
                            (203, 'Булатниково', 3, 20, 'Павелецкое'),
                            (204, 'Ленинская', 4, 29, 'Павелецкое'),
                            (205, 'Домодедово', 5, 37, 'Павелецкое'),
                            (206, 'Белые столбы', 6, 49, 'Павелецкое'),
                            (207, 'Вельяминово', 7, 62, 'Павелецкое');

INSERT INTO routes VALUES (398, 'Ярославское', 'экспресс', 'по рабочим', 'из города');

INSERT INTO route_stations VALUES (1, 398, '8:30'),
                                  (7, 398, '8:37'),
                                  (8, 398, '8:41'),
                                  (13, 398, '8:50'),
                                  (28, 398, '9:01');
INSERT INTO train_models VALUES ('ЭД4М');
INSERT INTO trains VALUES (1, 'ЭД4М', '12.08.2006', NULL);
INSERT INTO rides VALUES (2, '2021-05-17 8:30', 398, 1, 'e4001');

-- now connect as e1001
/*
INSERT INTO tickets VALUES (1, NULL, 'экспресс', '2021-05-17 8:28', 0, 1, 13, NULL),
                           (2, NULL, 'экспресс', '2021-05-17 8:28', 1, 1, 13, NULL),
                           (3, NULL, 'стандарт', '2021-05-17 8:28', 0, 1, 13, NULL),
                           (4, NULL, 'стандарт', '2021-05-17 8:28', 1, 1, 13, NULL);
*/
--INDEXES================================================================================
CREATE INDEX fk_directions_manager ON directions(manager);
CREATE INDEX fk_emp_post ON employees(post);
CREATE INDEX ind_employees_period ON employees(emp_date, quit_date);
CREATE INDEX ind_trains_period ON trains(serv_start_date, serv_end_date);
CREATE INDEX ind_employees_fio ON employees(last_name, first_name, patronymic);
CREATE INDEX ind_rides_ddate ON rides(ddate);

