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
