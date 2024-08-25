
CREATE TABLE User (
    id SERIAL PRIMARY KEY
);

CREATE TABLE timestamps (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Fuel_level (
    id SERIAL PRIMARY KEY,
    User_Id INT REFERENCES User(id),
    fuel FLOAT NOT NULL,
    timestamp_id INT REFERENCES timestamps(id)
);

CREATE TABLE Fuel_cons (
    id SERIAL PRIMARY KEY,
    User_Id INT REFERENCES User(id),
    consumption FLOAT NOT NULL,
    timestamp_id INT REFERENCES timestamps(id)
);

CREATE TABLE Mass_air_flow (
    id SERIAL PRIMARY KEY,
    User_Id INT REFERENCES User(id),
    air_flow FLOAT NOT NULL,
    timestamp_id INT REFERENCES timestamps(id)
);

CREATE TABLE Oxygen (
    id SERIAL PRIMARY KEY,
    User_Id INT REFERENCES User(id),
    oxygen_level FLOAT NOT NULL,
    timestamp_id INT REFERENCES timestamps(id)
);

CREATE TABLE Speed_kph (
    id SERIAL PRIMARY KEY,
    User_Id INT REFERENCES User(id),
    speed FLOAT NOT NULL,
    timestamp_id INT REFERENCES timestamps(id)
);

CREATE TABLE Throttle (
    id SERIAL PRIMARY KEY,
    User_Id INT REFERENCES User(id),
    position FLOAT NOT NULL,
    timestamp_id INT REFERENCES timestamps(id)
);

CREATE TABLE Coolant (
    id SERIAL PRIMARY KEY,
    User_Id INT REFERENCES User(id),
    temp FLOAT NOT NULL,
    timestamp_id INT REFERENCES timestamps(id)
);

CREATE TABLE Intake_manifold (
    id SERIAL PRIMARY KEY,
    User_Id INT REFERENCES User(id),
    level FLOAT NOT NULL,
    timestamp_id INT REFERENCES timestamps(id)
);

CREATE TABLE RPM (
    id SERIAL PRIMARY KEY,
    User_Id INT REFERENCES User(id),
    amount FLOAT NOT NULL,
    timestamp_id INT REFERENCES timestamps(id)
);
