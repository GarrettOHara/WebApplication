SELECT COUNT(a.choice_id), c.text  
FROM answer AS a, question AS q, choice AS C 
WHERE a.question_id = q.question_id 
GROUP BY c.choice_id;

SELECT COUNT(a.choice_id)
FROM answer AS a, question AS q 
WHERE a.question_id = q.question_id
GROUP BY a.choice_id;

SELECT COUNT(a.choice_id), c.text
FROM answer AS a, question AS q, choice AS c
WHERE a.question_id = q.question_id AND a.question_id = c.question_id
GROUP BY a.choice_id;

SELECT *
FROM choice AS c 
WHERE c.question_id in (
  SELECT COUNT(a.choice_id)
  FROM answer AS a, question AS q 
  WHERE a.question_id = 12 --VARIABLE DATA FOR QUESTION
  GROUP BY a.choice_id
);

SELECT c.text
FROM answer AS a, question AS q, choice AS c 
WHERE a.question_id = 12;


SELECT choice.text, COUNT(answer.choice_id) 
FROM choice, answer 
WHERE choice.question_id and answer.question_id = 12 
GROUP BY answer.choice_id;

SELECT choice.text, COUNT(answer.choice_id) 
FROM choice, answer 
GROUP BY answer.choice_id
HAVING answer.question_id and choice.question_id = 12;

SELECT choice.text, COUNT(answer.choice_id)
FROM choice, answer 
WHERE choice.question_id = 12 
GROUP BY answer.choice_id;

---------

SELECT count(*) 
FROM answer 
WHERE question_id = 12 
GROUP BY choice_id;

SELECT choice.text
FROM choice
WHERE question_id = 12;


SELECT q.text as Question, c.text AS Choice, COUNT(c.choice_id) AS Responses
FROM question AS q, choice AS c, answer as a
WHERE a.question_id = q.question_id and a.choice_id = c.choice_id and q.question_id = 13
GROUP BY a.choice_id;


+-------------------------------------+-----------------+-----------+
| Question                            | Chocie          | Responses |
+-------------------------------------+-----------------+-----------+
| How awesome is this web application | Its great       |         3 |
| How awesome is this web application | Its teadious... |         1 |
+-------------------------------------+-----------------+-----------+ 

('Testing creating polls', 'Option B', 3)
('Testing creating polls', 'Option A', 1)


SELECT * FROM (
  SELECT COUNT(answer.question_id)
  FROM answer
  GROUP BY answer.question_id
) AS Responses ORDER BY answer.question_id ASC;

SELECT COUNT(answer.question_id) AS Responses
FROM answer
ORDER BY answer.question_id DESC
GROUP BY answer.question_id
;


SELECT *
FROM answer, question
WHERE question.question_id = answer.question_id
GROUP BY question.question_id;

SELECT * as Repsonses
FROM answer
ORDER BY(
  SELECT COUNT(*) as Repsonses
  FROM answer
  GROUP BY answer.question_id 
  ORDER BY Repsonses DESC
) ASC;

-- HISTORY QUERY
-- RETURN QUESTION DATA AND RESPONSE DATA
-- ORDERS RESPONSES OF QUESTIOSN DESCENDING
SELECT *,COUNT(*) as Repsonses
FROM answer, question
WHERE answer.question_id = question.question_id
GROUP BY answer.question_id 
ORDER BY Repsonses DESC;
------------------------------------------------

-- SEARCH QUERY
-- RETURN STRING MATCH ON DATA WITH LIKE OPERATOR
-- USE PYTHON STRING FORMATTING TO INPUT USER SEARCH
SELECT *
FROM question
WHERE question.text LIKE '{}%';
-------------------------------------------------