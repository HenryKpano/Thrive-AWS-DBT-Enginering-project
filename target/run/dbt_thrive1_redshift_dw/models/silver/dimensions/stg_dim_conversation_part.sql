
      
        
            
        delete from "thrivedev"."dev_silver"."stg_dim_conversation_part"
    where (id) in (
        select distinct id
        from "stg_dim_conversation_part__dbt_tmp231912193688" as DBT_INTERNAL_SOURCE
    )
    
    ;
    

    insert into "thrivedev"."dev_silver"."stg_dim_conversation_part" ("id", "conversation_id", "conv_dataset_email", "part_type", "message", "created_at", "get_date_at")
        (
            select "id", "conversation_id", "conv_dataset_email", "part_type", "message", "created_at", "get_date_at"
            from "stg_dim_conversation_part__dbt_tmp231912193688"
        )
  