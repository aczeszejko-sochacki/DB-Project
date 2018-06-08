BEGIN;

  DROP TABLE IF EXISTS workers CASCADE;
  DROP TABLE IF EXISTS subordinates CASCADE;

  CREATE TABLE workers(
    emp int PRIMARY KEY,
    password text NOT NULL,
	supervisor int,
    data text NOT NULL);

  CREATE TABLE subordinates(
    emp int NOT NULL,
    subordinate int REFERENCES workers(emp) NOT NULL);

  CREATE OR REPLACE FUNCTION insert_sub() RETURNS TRIGGER AS 
  $X$
  BEGIN
    RETURN NULL;
  END
  $X$ LANGUAGE plpgsql;

  CREATE TRIGGER insert_subordinate AFTER INSERT ON workers
  EXECUTE PROCEDURE insert_sub();

COMMIT;
