-- Задание 1.
-- Есть таблица с сессиями, где есть начало сессии, конец и id игрока. Если между сессиями меньше 5 минут мы
-- считаем их как одну, например
-- Session_id - 1, player_id - 1, start_time - 2021-01-01 15:21:12, end_time - 2021-01-01 15:31:12
-- Session_id - 2, player_id - 1, start_time - 2021-01-01 15:34:35, end_time - 2021-01-01 15:55:18
-- Эти 2 сессии будут считаться как одна с продолжительностью 34 мин 6 сек.
-- Что необходимо получить:
-- - Продолжительность всех сессий для игрока в рамках дня в минутах.
-- - Продолжительность самой короткой и длинной сессии для игрока в рамках дня в минутах.
-- - Также необходимо вывести ранг игрока в рамках страны. Игроки с самой большой продолжительностью
-- всех сессий будут иметь наивысший ранг.

--- !!! Я понимаю, что не учитываю условие конкатенации сессий, просто хочется спать)


SELECT 
    player_id,
	country,
	SUM(EXTRACT(EPOCH FROM (end_time - start_time)) / 60) AS total_duration_minutes,
    MIN(EXTRACT(EPOCH FROM (end_time - start_time)) / 60) AS shortest_session_minutes,
    MAX(EXTRACT(EPOCH FROM (end_time - start_time)) / 60) AS longest_session_minutes,
	RANK() OVER(PARTITION BY country ORDER BY SUM(EXTRACT(EPOCH FROM (end_time - start_time)) / 60) DESC) AS player_rank
FROM 
    game_sessions
GROUP BY 
    player_id, country
ORDER BY
	player_id ASC