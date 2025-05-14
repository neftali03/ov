
-- CORE ----------------------------------------------------------------
CREATE OR REPLACE TRIGGER lock_created_at
  BEFORE UPDATE
  ON django.core_requestlog
  FOR EACH ROW
EXECUTE PROCEDURE django.lock_created_at();
CREATE OR REPLACE TRIGGER lock_created_at
  BEFORE UPDATE
  ON django.core_actionlog
  FOR EACH ROW
EXECUTE PROCEDURE django.lock_created_at();

ALTER TABLE core_actionlog ALTER COLUMN created_at SET DEFAULT NOW();
