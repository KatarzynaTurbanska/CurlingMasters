CREATE TABLE address
(
  person_id  SMALLINT(5) UNSIGNED NOT NULL,
  address_id SMALLINT(5) UNSIGNED NOT NULL,
  PRIMARY KEY (person_id)
);

CREATE TABLE address_book
(
  address_id    SMALLINT(5) UNSIGNED NOT NULL,
  city          VARCHAR(25)          NULL    ,
  street        VARCHAR(40)          NULL    ,
  street_number SMALLINT(5) UNSIGNED NULL    ,
  PRIMARY KEY (address_id)
);

CREATE TABLE equipment
(
  facility_id SMALLINT(5) UNSIGNED NOT NULL,
  brooms      TINYINT(2) UNSIGNED  NULL     COMMENT 'amount of brooms',
  stones      TINYINT(2) UNSIGNED  NULL     COMMENT 'amount of stones',
  shoes       TINYINT(2) UNSIGNED  NULL     COMMENT 'amout of pairs of shoes',
  PRIMARY KEY (facility_id)
);

CREATE TABLE facility
(
  facility_id SMALLINT(5) UNSIGNED NOT NULL,
  address_id  SMALLINT(5) UNSIGNED NOT NULL,
  PRIMARY KEY (facility_id)
);

CREATE TABLE finances
(
  person_id      SMALLINT(5) UNSIGNED NOT NULL,
  date           DATE                 NOT NULL,
  financial_flow FLOAT(7, 2)          NULL    ,
  PRIMARY KEY (date, person_id)
);

CREATE TABLE gender
(
  first_name VARCHAR(15)    NOT NULL,
  gender     ENUM('M', 'F') NULL    ,
  PRIMARY KEY (first_name)
);

CREATE TABLE matches
(
  team_name      VARCHAR(30)          NOT NULL,
  date           DATE                 NOT NULL,
  address_id     SMALLINT(5) UNSIGNED NOT NULL,
  team_score     TINYINT(2) UNSIGNED  NULL    ,
  opponent_score TINYINT(2) UNSIGNED  NULL    ,
  number_of_ends TINYINT UNSIGNED     NULL    ,
  ends_won       TINYINT UNSIGNED     NULL    ,
  PRIMARY KEY (date, team_name)
);

CREATE TABLE opponents
(
  team_name     VARCHAR(30) NOT NULL,
  date          DATE        NOT NULL,
  opponent_name VARCHAR(20) NOT NULL,
  PRIMARY KEY (date, team_name)
);

CREATE TABLE people
(
  person_id  SMALLINT(5) UNSIGNED NOT NULL,
  first_name VARCHAR(15)          NOT NULL,
  last_name  VARCHAR(15)          NULL    ,
  PRIMARY KEY (person_id)
);

CREATE TABLE personal_info
(
  person_id   SMALLINT(5) UNSIGNED                                                                   NOT NULL,
  team_name   VARCHAR(30)                                                                            NULL    ,
  position    ENUM('cleaner', 'director', 'manager', 'medic', 'psychologist', 'accountant', 'coach') NULL    ,
  birthdate   DATE                                                                                   NULL    ,
  join_date   DATE                                                                                   NULL    ,
  retire_date DATE                                                                                   NULL    ,
  PRIMARY KEY (person_id)
);

CREATE TABLE phone_book
(
  person_id SMALLINT(5) UNSIGNED NOT NULL,
  phone     VARCHAR(14)          NULL, 
);

CREATE TABLE positions
(
  person_id SMALLINT(5) UNSIGNED                NOT NULL,
  date      DATE                                NOT NULL,
  position  ENUM('lead','second','vice','skip') NULL    ,
  PRIMARY KEY (date, person_id)
);

CREATE TABLE teams
(
  team_name       VARCHAR(30)                    NOT NULL,
  facility_id     SMALLINT(5) UNSIGNED           NOT NULL,
  age_category    ENUM('junior', 'adult')        NOT NULL,
  gender_category ENUM('mixed',  'men', 'women') NOT NULL,
  PRIMARY KEY (team_name)
);

ALTER TABLE personal_info
  ADD CONSTRAINT FK_teams_TO_personal_info
    FOREIGN KEY (team_name)
    REFERENCES teams(team_name);

ALTER TABLE matches
  ADD CONSTRAINT FK_teams_TO_matches
    FOREIGN KEY (team_name)
    REFERENCES teams(team_name);

ALTER TABLE personal_info
  ADD CONSTRAINT FK_people_TO_personal_info
    FOREIGN KEY (person_id)
    REFERENCES people(person_id);

ALTER TABLE people
  ADD CONSTRAINT FK_gender_TO_people
    FOREIGN KEY (first_name)
    REFERENCES gender(first_name);

ALTER TABLE phone_book
  ADD CONSTRAINT FK_people_TO_phone_book
    FOREIGN KEY (person_id)
    REFERENCES people(person_id);

ALTER TABLE address
  ADD CONSTRAINT FK_address_book_TO_address
    FOREIGN KEY (address_id)
    REFERENCES address_book(address_id);

ALTER TABLE equipment
  ADD CONSTRAINT FK_facility_TO_equipment
    FOREIGN KEY (facility_id)
    REFERENCES facility(facility_id);

ALTER TABLE opponents
  ADD CONSTRAINT FK_matches_TO_opponents
    FOREIGN KEY (team_name, date)
    REFERENCES matches(team_name, date);

ALTER TABLE positions
  ADD CONSTRAINT FK_matches_TO_positions
    FOREIGN KEY (date)
    REFERENCES matches(date);

ALTER TABLE facility
  ADD CONSTRAINT FK_address_book_TO_facility
    FOREIGN KEY (address_id)
    REFERENCES address_book(address_id);

ALTER TABLE matches
  ADD CONSTRAINT FK_address_book_TO_matches
    FOREIGN KEY (address_id)
    REFERENCES address_book(address_id);

ALTER TABLE finances
  ADD CONSTRAINT FK_people_TO_finances
    FOREIGN KEY (person_id)
    REFERENCES people(person_id);

ALTER TABLE address
  ADD CONSTRAINT FK_people_TO_address
    FOREIGN KEY (person_id)
    REFERENCES people(person_id);

ALTER TABLE teams
  ADD CONSTRAINT FK_facility_TO_teams
    FOREIGN KEY (facility_id)
    REFERENCES facility(facility_id);

ALTER TABLE positions
  ADD CONSTRAINT FK_people_TO_positions
    FOREIGN KEY (person_id)
    REFERENCES people(person_id);

ALTER TABLE phone_book
  ADD PRIMARY KEY (person_id);  

ALTER TABLE address_book MODIFY street_number INT(5);

ALTER TABLE opponents MODIFY opponent_name VARCHAR(30);
