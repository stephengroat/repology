CREATE TABLE IF NOT EXISTS raw_packages(
    repo varchar(255) NOT NULL,
    effname varchar(255) NOT NULL,
    packages jsonb NOT NULL,
    updated timestamp with time zone NOT NULL,
    PRIMARY KEY(repo, effname)
);

CREATE TABLE IF NOT EXISTS metapackages_recalc_queue(
    effname varchar(255) NOT NULL PRIMARY KEY
);

CREATE OR REPLACE FUNCTION raw_metapackages_handle_update() RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            INSERT INTO metapackages_recalc_queue VALUES(NEW.effname) ON CONFLICT(effname) DO NOTHING;
        ELSIF (TG_OP = 'DELETE') THEN
            INSERT INTO metapackages_recalc_queue VALUES(OLD.effname) ON CONFLICT(effname) DO NOTHING;
        ELSIF (TG_OP = 'UPDATE') THEN
            IF (OLD.packages != NEW.packages) THEN
                INSERT INTO metapackages_recalc_queue VALUES(NEW.effname) ON CONFLICT(effname) DO NOTHING;
            END IF;
        END IF;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER raw_metapackages_update_handler
AFTER INSERT OR UPDATE OR DELETE ON raw_packages FOR EACH ROW EXECUTE PROCEDURE raw_metapackages_handle_update();
