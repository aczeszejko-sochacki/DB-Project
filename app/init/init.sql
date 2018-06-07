BEGIN;

  DROP TABLE IF EXISTS workers CASCADE;
  DROP TABLE IF EXISTS subordinates CASCADE;

  CREATE TABLE workers(
    emp int PRIMARY KEY,
    password text NOT NULL,
	supervisor int NOT NULL);
  CREATE TABLE subordinates(
    emp int NOT NULL,
    subordinate int REFERENCES workers(emp) NOT NULL);

COMMIT;
