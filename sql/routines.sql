-- Set the `updated_at` column.
CREATE OR REPLACE FUNCTION django.set_updated_at()
  RETURNS TRIGGER AS
$$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- Prevent changes on the `created_at` column.
CREATE OR REPLACE FUNCTION django.lock_created_at()
  RETURNS TRIGGER AS
$$
BEGIN
  IF NEW.created_at <> OLD.created_at THEN
    RAISE EXCEPTION 'Update the `created_at` field is not allowed.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- Return the difference from two JSONB objects as a JSONB object.
-- Only left values are returned.
CREATE OR REPLACE FUNCTION django.jsonb_diff(left_obj jsonb, right_obj jsonb)
  RETURNS jsonb AS
$$
DECLARE
  diff jsonb;
BEGIN
  SELECT JSONB_OBJECT_AGG(i.key, i.value)
  INTO diff
  FROM (SELECT * FROM JSONB_EACH(left_obj)) i
         LEFT OUTER JOIN
         (SELECT * FROM JSONB_EACH(right_obj)) j ON i.key = j.key
  WHERE i.value != j.value
     OR j.key IS NULL;
  RETURN diff;
END;
$$
  LANGUAGE plpgsql;

-- Log changes.
CREATE OR REPLACE FUNCTION django.log_changes()
  RETURNS TRIGGER AS
$$
BEGIN
  IF (tg_op = 'UPDATE') THEN
    INSERT INTO django.core_actionlog ( db_user
                                      , db_schema
                                      , db_table
                                      , action
                                      , model_id
                                      , old_data
                                      , new_data)
    VALUES ( SESSION_USER
           , tg_table_schema
           , tg_table_name
           , tg_op
           , old.id
           , TO_JSONB(old)
           , django.jsonb_diff(TO_JSONB(new), TO_JSONB(old)));
    RETURN NEW;
  ELSIF (tg_op = 'DELETE') THEN
    INSERT INTO django.core_actionlog ( db_user
                                      , db_schema
                                      , db_table
                                      , action
                                      , model_id
                                      , old_data)
    VALUES ( SESSION_USER
           , tg_table_schema
           , tg_table_name
           , tg_op
           , old.id
           , TO_JSONB(old));
    RETURN OLD;
  ELSIF (tg_op = 'INSERT') THEN
    INSERT INTO django.core_actionlog ( db_user
                                      , db_schema
                                      , db_table
                                      , action
                                      , model_id
                                      , new_data)
    VALUES ( SESSION_USER
           , tg_table_schema
           , tg_table_name
           , tg_op
           , new.id
           , TO_JSONB(new));
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE 'plpgsql';
