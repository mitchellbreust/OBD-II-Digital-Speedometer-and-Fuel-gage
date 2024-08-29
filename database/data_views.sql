
CREATE VIEW UserFuelLevel AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    fl.fuel
FROM 
    Users u
JOIN 
    Fuel_level fl ON u.id = fl.User_Id
JOIN 
    timestamps t ON fl.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;

CREATE VIEW UserFuelConsumption AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    fc.consumption AS fuel_consumption
FROM 
    Users u
JOIN 
    Fuel_cons fc ON u.id = fc.User_Id
JOIN 
    timestamps t ON fc.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;

CREATE VIEW UserMassAirFlow AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    maf.air_flow
FROM 
    Users u
JOIN 
    Mass_air_flow maf ON u.id = maf.User_Id
JOIN 
    timestamps t ON maf.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;

CREATE VIEW UserOxygenLevel AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    o.oxygen_level
FROM 
    Users u
JOIN 
    Oxygen o ON u.id = o.User_Id
JOIN 
    timestamps t ON o.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;


CREATE VIEW UserSpeed AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    s.speed
FROM 
    Users u
JOIN 
    Speed_kph s ON u.id = s.User_Id
JOIN 
    timestamps t ON s.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;

CREATE VIEW UserThrottlePosition AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    th.position AS throttle_position
FROM 
    Users u
JOIN 
    Throttle th ON u.id = th.User_Id
JOIN 
    timestamps t ON th.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;

CREATE VIEW UserCoolantTemperature AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    c.temp AS coolant_temperature
FROM 
    Users u
JOIN 
    Coolant c ON u.id = c.User_Id
JOIN 
    timestamps t ON c.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;

CREATE VIEW UserIntakeManifoldLevel AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    im.level AS intake_manifold_level
FROM 
    Users u
JOIN 
    Intake_manifold im ON u.id = im.User_Id
JOIN 
    timestamps t ON im.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;

CREATE VIEW UserRPM AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    r.amount AS rpm
FROM 
    Users u
JOIN 
    RPM r ON u.id = r.User_Id
JOIN 
    timestamps t ON r.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;

CREATE VIEW UserDiagnosticCodes AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    dc.code AS diagnostic_code
FROM 
    Users u
JOIN 
    DC dc ON u.id = dc.User_Id
JOIN 
    timestamps t ON dc.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;

CREATE VIEW UserVoltage AS
SELECT 
    u.id AS user_id,
    t.timestamp,
    v.volt AS voltage_value
FROM 
    Users u
JOIN 
    voltage v ON u.id = v.User_Id
JOIN 
    timestamps t ON v.timestamp_id = t.id
ORDER BY 
    u.id, t.timestamp;
