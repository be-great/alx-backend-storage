-- create two stored procedures
--- 1- compute the average weighted score of user based on project score and stores in users table
--- 2- compute the average score of all user stores it in users
--- weighted_sum=(project1×weight1)+(project2×weight2)
--- average_score = weighted_sum / (weight1 + weight2)
DELIMITER //;
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT;
    DECLARE weighted_sum FLOAT;
    -- calculate the total weighted for the user
    SELECT SUM(p.weight)
    INTO total_weight
    FROM projects p
    JOIN corrections c ON p.id = c.project_id
    WHERE c.user_id = user_id;

    -- calculate the weighted sum of score of user
    SELECT SUM(c.socre* p.weight)
    INTO weighted_sum
    FROM projects p
    JOIN corrections c ON p.id = c.project_id
    WHERE c.user_id = user_id;
    -- update the average weighted score
    IF total_weight > 0 THEN
        UPDATE users
        SET average_score = weighted_sum / total_weight
        WHERE id = user_id;
    ELSE
        UPDATE users
        SET average_score = 0
        WHERE id = user_id;
    END IF;
END //
DELIMITER ;