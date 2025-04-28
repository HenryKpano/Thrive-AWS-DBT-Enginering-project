
      
        
            
        delete from "thrivedev"."dev_silver"."stg_fact_consolidated_messages"
    where (id) in (
        select distinct id
        from "stg_fact_consolidated_messages__dbt_tmp231915669724" as DBT_INTERNAL_SOURCE
    )
    
    ;
    

    insert into "thrivedev"."dev_silver"."stg_fact_consolidated_messages" ("id", "user_id", "email", "conversation_id", "message", "message_type", "created_at")
        (
            select "id", "user_id", "email", "conversation_id", "message", "message_type", "created_at"
            from "stg_fact_consolidated_messages__dbt_tmp231915669724"
        )
  