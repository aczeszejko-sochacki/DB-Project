DROP TABLE IF EXISTS workers CASCADE;


-- Create tables
CREATE TABLE workers(
  emp int PRIMARY KEY,
  password text NOT NULL,
  parent int,
  data text NOT NULL,
  children int array,
  _in int,
  _out int);


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
CREATE OR REPLACE FUNCTION child(int) RETURNS int[] AS
$$
BEGIN
  RETURN (SELECT children FROM workers WHERE emp = $1);
END;
$$ LANGUAGE plpgsql STABLE;


-- Check if emp2 = $2 is ancestor of emp1 = $1 or $2 = $1
CREATE OR REPLACE FUNCTION ancestor_or_equal(int, int) RETURNS VOID AS
$$
DECLARE
  in_1 int = (SELECT _in FROM workers WHERE emp = $1);
  in_2 int = (SELECT _in FROM workers WHERE emp = $2);
  out_1 int = (SELECT _out FROM workers WHERE emp = $1);
  out_2 int = (SELECT _out FROM workers WHERE emp = $2);
BEGIN
  IF in_1 >= in_2 AND out_1 <= out_2 THEN
    RETURN;
  ELSE
    RAISE EXCEPTION 'Neither ancestor nor equal';
  END IF;
END;
$$ LANGUAGE plpgsql STABLE;


-- Check if emp2 = $2 is ancestor of emp1 = $1
CREATE OR REPLACE FUNCTION ancestor(int, int) RETURNS boolean AS
$$
DECLARE
  in_1 int = (SELECT _in FROM workers WHERE emp = $1);
  in_2 int = (SELECT _in FROM workers WHERE emp = $2);
  out_1 int = (SELECT _out FROM workers WHERE emp = $1);
  out_2 int = (SELECT _out FROM workers WHERE emp = $2);
BEGIN
  IF in_1 > in_2 AND out_1 < out_2 THEN
    RETURN TRUE;
  ELSE
	RETURN FALSE;
  END IF;
END;
$$ LANGUAGE plpgsql STABLE;


-- Return all ancestors of emp = $1
CREATE OR REPLACE FUNCTION ancestors(int) RETURNS SETOF int AS
$$
DECLARE
  in_1 int = (SELECT _in FROM workers WHERE emp = $1);
  out_1 int = (SELECT _out FROM workers WHERE emp = $1);
BEGIN
  RETURN QUERY (SELECT emp FROM workers WHERE _in < in_1 AND out_1 < _out);
END;
$$ LANGUAGE plpgsql STABLE;


-- Return all descendants of emp = $1
CREATE OR REPLACE FUNCTION descendants(int) RETURNS SETOF int AS
$$
DECLARE
  in_1 int = (SELECT _in FROM workers WHERE emp = $1);
  out_1 int = (SELECT _out FROM workers WHERE emp = $1);
BEGIN
  RETURN QUERY (SELECT emp FROM workers WHERE in_1 < _in AND _out < out_1);
END;
$$ LANGUAGE plpgsql STABLE;


-- Read data of emp = $1
CREATE OR REPLACE FUNCTION read(int) RETURNS text AS
$$
BEGIN
  RETURN (SELECT data FROM workers WHERE emp = $1);
END;
$$ LANGUAGE plpgsql STABLE;


-- Update data of emp = $1, set newdata = $2
CREATE OR REPLACE FUNCTION update(int, text) RETURNS VOID AS
$$
BEGIN
	UPDATE workers SET data = $2 WHERE emp = $1;
END;
$$ LANGUAGE plpgsql VOLATILE;

-- Insert root
CREATE OR REPLACE FUNCTION root(int, text, text) RETURNS VOID AS
$$
BEGIN
  INSERT INTO workers(emp, password, data) VALUES($1, $2, $3);
  UPDATE workers SET children = NULL; -- for invoking trigger
END;
$$ LANGUAGE plpgsql VOLATILE;


-- Insert new worker
CREATE OR REPLACE FUNCTION insert_new_worker(int, text, int, text) 
RETURNS VOID AS
$$
BEGIN
  INSERT INTO workers(emp, password, parent, data) VALUES($1, $2, $3, $4);
END;
$$ LANGUAGE plpgsql VOLATILE;

-- Insert new subordinate to subordinates table
CREATE OR REPLACE FUNCTION add_sub() RETURNS TRIGGER AS
$$
BEGIN
  UPDATE workers SET children = children || array[New.emp] 
	WHERE emp = NEW.parent;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql VOLATILE;


-- DFS to set in and out numbers
CREATE OR REPLACE FUNCTION dfs() RETURNS TRIGGER AS
$$
DECLARE
  to_visit int array;
  root int;
  visited int;
  num int = 1;
BEGIN

  UPDATE workers SET _in = NULL;
  UPDATE workers SET _out = NULL;

  SELECT emp INTO root FROM workers WHERE parent IS NULL;
  to_visit = to_visit || root;	-- append

  -- DFS
  WHILE cardinality(to_visit) > 0 LOOP
	root = to_visit[cardinality(to_visit)];

	
	IF (SELECT _in FROM workers WHERE emp = root) IS NULL THEN
		UPDATE workers SET _in = num WHERE emp = root;
		
		to_visit = to_visit ||
		  (SELECT children FROM workers WHERE emp = root);

	ELSE UPDATE workers SET _out = num WHERE emp = root;
    	 to_visit = to_visit[0:(cardinality(to_visit) - 1)];	-- pop last el

	END IF;

	num = num + 1;

  END LOOP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Triggers in PostgreSQL are invoked alphabetically!!!

-- Add subordinate after insert
CREATE TRIGGER add_child AFTER INSERT ON workers FOR EACH ROW
EXECUTE PROCEDURE add_sub();

-- Set new in / out after insert
CREATE TRIGGER in_out AFTER UPDATE OF children ON workers FOR EACH ROW
EXECUTE PROCEDURE dfs();

