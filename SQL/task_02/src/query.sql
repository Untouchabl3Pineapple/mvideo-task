-- Задание 2.
-- Используя набор выше показать нарастающий итог продолжительности сессий для игрока в минутах. В
-- данном случае правило 5 минут не учитывается.
-- К примеру строка с id = 1 будет иметь значение 9, строка с id = 2 значение 81 (72 + 9) и т.д.


SELECT 
    session_id,
    player_id,
    country,
    start_time,
    end_time,
    SUM(EXTRACT(EPOCH FROM (end_time - start_time)) / 60) OVER (PARTITION BY player_id ORDER BY start_time) AS player_total_duration
FROM 
    game_sessions
ORDER BY 
    player_id;
