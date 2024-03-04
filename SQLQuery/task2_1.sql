SELECT p.ID AS Person_ID, p.First_Name, p.Last_Name, p.Locatie AS Location,
       COUNT(v.ID) AS Votes_Received,
       SUM(CASE WHEN v.valid = 1 THEN 1 ELSE 0 END) AS Valid_Votes,
       SUM(CASE WHEN v.valid = 0 THEN 1 ELSE 0 END) AS Invalid_Votes,
       v.quality AS Quality
FROM persons p
LEFT JOIN Votes v ON p.ID = v.chosen_person
GROUP BY p.ID, p.First_Name, p.Last_Name, p.Locatie
ORDER BY Votes_Received DESC;