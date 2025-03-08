BEGIN TRANSACTION;

-- Apparatus contains information about the entity that responded to the incident
CREATE TABLE [Apparatus] (
   [id] INTEGER PRIMARY KEY NOT NULL,
   [car_id] TEXT,
   [extended_data] TEXT,
   [geohash] TEXT,
   [shift] TEXT,
   [station] TEXT,
   [unit_id] TEXT,
   [unit_type] TEXT
);

-- Create department table
CREATE TABLE [Department] (
   [id] INTEGER PRIMARY KEY NOT NULL,
   [fd_id] TEXT,
   [firecares_id] TEXT,
   [name] TEXT,
   [shift] TEXT,
   [state] TEXT,
   [timezone] TEXT
);

CREATE TABLE "Incident" (
   [id] INTEGER PRIMARY KEY NOT NULL,
   [comments] TEXT,
   [day_of_week] TEXT,
   [event_closed] TEXT,
   [event_id] TEXT,
   [event_opened] TEXT,
   [extended_data] TEXT,
   [first_unit_arrived] TEXT,
   [first_unit_dispatched] TEXT,
   [first_unit_enroute] TEXT,
   [hour_of_day] INTEGER,
   [incident_number] TEXT,
   [loi_search_complete] TEXT,
   [subtype] TEXT,
   [type] TEXT,
   [address_id] INTEGER REFERENCES [address]([id]),
   [department_id] INTEGER REFERENCES [Department]([id])
);


CREATE TABLE [Unit_Status] (
   [id] INTEGER PRIMARY KEY NOT NULL,
   [apparatus_id] INTEGER,
   [status] TEXT,
   [geohash] TEXT,
   [latitude] FLOAT,
   [longitude] FLOAT,
   [timestamp] TEXT
);



CREATE TABLE "address" (
   [id] INTEGER PRIMARY KEY NOT NULL,
   [address_id] TEXT,
   [address_line1] TEXT,
   [city] TEXT,
   [common_place_name] TEXT,
   [cross_street1] TEXT,
   [cross_street2] TEXT,
   [first_due] TEXT,
   [geohash] TEXT,
   [latitude] FLOAT,
   [longitude] FLOAT,
   [name] TEXT,
   [postal_code] TEXT, 
   [prefix_direction] TEXT, 
   [response_zone] TEXT, 
   [state] TEXT, 
   [suffix_direction] TEXT, 
   [type] TEXT);


COMMIT;
