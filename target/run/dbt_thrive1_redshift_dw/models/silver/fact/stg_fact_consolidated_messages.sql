
      
  
    

  create  table
    "thrivedev"."dev_bronze_dev_silver"."stg_fact_consolidated_messages"
    
    
    
  as (
    


WITH
  start_msgs AS (
    SELECT
      id           AS msg_id,
      conv_dataset_email AS email,
      id           AS conversation_id,
      message,
      'open'       AS message_type,
      created_at
    FROM 
        "thrivedev"."dev_bronze_dev_silver"."stg_dim_conversation_start"
  ),
  part_msgs AS (
    SELECT
      id           AS msg_id,
      conv_dataset_email AS email,
      conversation_id,
      message,
      part_type    AS message_type,
      created_at
    FROM 
        "thrivedev"."dev_bronze_dev_silver"."stg_dim_conversation_part"
  ),
  all_msgs AS (
    SELECT * FROM start_msgs
    UNION ALL
    SELECT * FROM part_msgs
  ),
  conv_customer AS (
    SELECT
      am.conversation_id,
      u.id AS user_id
    FROM all_msgs am
    INNER JOIN "thrivedev"."dev_bronze_dev_silver"."stg_dim_user" u
      ON am.email = u.email
    WHERE u.is_customer = 1
    GROUP BY user_id, am.conversation_id
  )
SELECT
  am.msg_id      AS id,
  cc.user_id     AS user_id,
  am.email       AS email,
  am.conversation_id,
  am.message,
  am.message_type,
  am.created_at
FROM all_msgs am
INNER JOIN conv_customer cc
  ON am.conversation_id = cc.conversation_id
ORDER BY
  am.conversation_id,
  am.created_at
  );
  
  