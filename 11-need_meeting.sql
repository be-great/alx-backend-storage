-- list students
--  1- whos grade is below 80
--  2- their last meething more than amonth or no meeting
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
 AND (last_meeting IS NULL OR last_meeting < DATE_SUB(CURDATE(), INTERVAL 1 MONTH));
