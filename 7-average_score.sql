-- compute the average score for user
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE id = user_id

    -- update the user average score
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id
END $$
DELIMITER;