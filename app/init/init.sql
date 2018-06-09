
DROP TABLE IF EXISTS workers CASCADE;
DROP TABLE IF EXISTS subordinates CASCADE;

-- Create tables
CREATE TABLE workers(
  emp int PRIMARY KEY,
  password text NOT NULL,
  supervisor int,
  data text NOT NULL);


CREATE TABLE subordinates(
  emp int NOT NULL,
  subordinate int REFERENCES workers(emp) NOT NULL);


-- Check if emp2 = $2 is ancestor of emp1 = $1
CREATE OR REPLACE FUNCTION ancestor(int, int) RETURNS boolean AS
$$
DECLARE
 worker ALIAS FOR $1;
BEGIN
  WHILE worker IS NOT NULL LOOP
    SELECT supervisor INTO worker
    FROM workers
    WHERE emp = worker;

    IF worker = $2 THEN RETURN TRUE;
    END IF;
  END LOOP;

  RETURN FALSE;
END;
$$ LANGUAGE plpgsql STABLE;


-- Insert root
CREATE OR REPLACE FUNCTION root(int, text, text) RETURNS VOID AS
$$
BEGIN
	INSERT INTO workers(emp, password, data) VALUES($1, $2, $3);
END;
$$ LANGUAGE plpgsql VOLATILE;


-- Insert new worker
CREATE OR REPLACE FUNCTION new(int, text, int, text) RETURNS BOOLEAN AS
$$
BEGIN
  INSERT INTO workers VALUES($1, $2, $3, $4);
  RETURN TRUE;  -- to do
END;
$$ LANGUAGE plpgsql VOLATILE;

