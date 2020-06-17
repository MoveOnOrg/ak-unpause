SELECT user_id
FROM ak_moveon.core_subscription
WHERE list_id = 17
AND created_at < GETDATE() - INTERVAL '30 days'
