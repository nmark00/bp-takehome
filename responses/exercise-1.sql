SELECT 
    oi.locationId,
    MONTH(STR_TO_DATE(t.datetime, '%Y-%m-%d %H:%i:%s')) AS refund_month,
    SUM(JSON_EXTRACT(t.details, '$.items[0].amount')) AS total_refunded
FROM 
    transactions t
JOIN 
    order_items oi ON JSON_EXTRACT(t.details, '$.items[0].id') = oi.id
WHERE 
    t.type = 'refund'
GROUP BY 
    oi.locationId,
    MONTH(STR_TO_DATE(t.datetime, '%Y-%m-%d %H:%i:%s'))
ORDER BY 
    oi.locationId,
    refund_month;