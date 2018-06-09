DROP TABLE IF EXISTS workers CASCADE;
DROP TABLE IF EXISTS children CASCADE;

-- Create tables
CREATE TABLE workers(
  emp int PRIMARY KEY,
  password text NOT NULL,
  parent int,
  data text NOT NULL);


CREATE TABLE children(
  emp int NOT NULL,
  child int REFERENCES workers(emp) NOT NULL);


-- Check if emp = $1 has password $2
CREATE OR REPLACE FUNCTION check_password(int, text) RETURNS VOID AS
$$
BEGIN
  IF ($1, $2) NOT IN (SELECT emp, password FROM workers)
  THEN RAISE EXCEPTION 'Wrong password!';
  END IF;
END;
$$ LANGUAGE plpgsql STABLE;


-- Return parent of emp = $1
CREATE OR REPLACE FUNCTION parent(int) RETURNS int AS
$$
BEGIN
  RETURN (SELECT parent FROM workers WHERE emp = $1);
END;
$$ LANGUAGE plpgsql STABLE;


-- Return children of emp = $1
CREATE OR REPLACE FUNCTION child(int) RETURNS SETOF int AS
$$
BEGIN
  RETURN QUERY (SELECT child FROM children WHERE emp = $1);
END;
$$ LANGUAGE plpgsql STABLE;


-- Check if emp2 = $2 is ancestor of emp1 = $1 or $2 = $1
CREATE OR REPLACE FUNCTION ancestor_or_equal(int, int) RETURNS VOID AS
$$
DECLARE
 worker ALIAS FOR $1;
BEGIN
  WHILE worker IS NOT NULL LOOP
    IF worker = $2 THEN RETURN;
    END IF;

    SELECT parent INTO worker
    FROM workers
    WHERE emp = worker;

  END LOOP;

  RAISE EXCEPTION 'Neither ancestor nor equal';
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
CREATE OR REPLACE FUNCTION insert_new_worker(int, text, int, text) 
RETURNS VOID AS
$$
BEGIN
  INSERT INTO workers VALUES($1, $2, $3, $4);
END;
$$ LANGUAGE plpgsql VOLATILE;


-- Insert new subordinate to subordinates table
CREATE OR REPLACE FUNCTION add_sub() RETURNS TRIGGER AS
$$
BEGIN
  IF (SELECT COUNT(*) 
	  FROM workers) > 1  -- insert after new, not root
  THEN INSERT INTO children VALUES(NEW.parent, NEW.emp);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql VOLATILE;


-- Add subordinate after insert
CREATE TRIGGER add_child AFTER INSERT ON workers FOR EACH ROW
EXECUTE PROCEDURE add_sub();

