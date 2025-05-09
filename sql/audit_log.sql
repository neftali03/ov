
-- CORE ----------------------------------------------------------------
CREATE OR REPLACE TRIGGER log_changes AFTER INSERT OR UPDATE OR DELETE ON django.core_user FOR EACH ROW EXECUTE PROCEDURE django.log_changes();
CREATE OR REPLACE TRIGGER log_changes AFTER INSERT OR UPDATE OR DELETE ON django.core_user_groups FOR EACH ROW EXECUTE PROCEDURE django.log_changes();
