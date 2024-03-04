SELECT p.Locatie AS Country,
       SUM(CASE WHEN v.voter = 1 THEN 1 ELSE 0 END) AS Votes_Count
FROM persons p

LEFT JOIN Votes v ON p.ID = v.chosen_person

GROUP BY p.Locatie
ORDER BY Votes_Count;