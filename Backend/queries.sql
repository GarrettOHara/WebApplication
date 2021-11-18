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