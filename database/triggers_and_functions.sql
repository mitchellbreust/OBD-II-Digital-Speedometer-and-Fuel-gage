
-- this will be executed as a cron job at 12am every day
CREATE OR REPLACE FUNCTION delete_old_data()
RETURNS void LANGUAGE plpgsql AS $$
DECLARE
    cutoff_date DATE;
    max_date_in_table DATE;
    start_of_month DATE;
BEGIN
    -- Calculate the cutoff date, 3 months ago from today
    cutoff_date := date_trunc('month', current_date) - interval '3 months';

    -- Find the maximum date in the timestamps table
    SELECT max(timestamp)::date INTO max_date_in_table FROM timestamps;

    -- Loop through each month and delete data if the entire month is older than 3 months
    FOR start_of_month IN
        SELECT date_trunc('month', timestamp)::date
        FROM timestamps
        WHERE timestamp < cutoff_date
        GROUP BY date_trunc('month', timestamp)::date
    LOOP
        -- Ensure the month is fully older than 3 months
        IF start_of_month < cutoff_date AND max_date_in_table < (start_of_month + interval '1 month') THEN
            -- Delete from the metric tables
            DELETE FROM Fuel_level WHERE timestamp_id IN (
                SELECT id FROM timestamps WHERE timestamp >= start_of_month AND timestamp < start_of_month + interval '1 month'
            );
            DELETE FROM Mass_air_flow WHERE timestamp_id IN (
                SELECT id FROM timestamps WHERE timestamp >= start_of_month AND timestamp < start_of_month + interval '1 month'
            );
            DELETE FROM Oxygen WHERE timestamp_id IN (
                SELECT id FROM timestamps WHERE timestamp >= start_of_month AND timestamp < start_of_month + interval '1 month'
            );
            DELETE FROM Speed_kph WHERE timestamp_id IN (
                SELECT id FROM timestamps WHERE timestamp >= start_of_month AND timestamp < start_of_month + interval '1 month'
            );
            DELETE FROM Throttle WHERE timestamp_id IN (
                SELECT id FROM timestamps WHERE timestamp >= start_of_month AND timestamp < start_of_month + interval '1 month'
            );
            DELETE FROM Coolant WHERE timestamp_id IN (
                SELECT id FROM timestamps WHERE timestamp >= start_of_month AND timestamp < start_of_month + interval '1 month'
            );
            DELETE FROM Intake_manifold WHERE timestamp_id IN (
                SELECT id FROM timestamps WHERE timestamp >= start_of_month AND timestamp < start_of_month + interval '1 month'
            );
            DELETE FROM RPM WHERE timestamp_id IN (
                SELECT id FROM timestamps WHERE timestamp >= start_of_month AND timestamp < start_of_month + interval '1 month'
            );

            -- Finally, delete from the timestamps table
            DELETE FROM timestamps WHERE timestamp >= start_of_month AND timestamp < start_of_month + interval '1 month';
        END IF;
    END LOOP;
END;
$$;
