
      
        
            
        delete from "thrivedev"."dev_gold"."dim_conversation_start"
    where (id) in (
        select distinct id
        from "dim_conversation_start__dbt_tmp231915415832" as DBT_INTERNAL_SOURCE
    )
    
    ;
    

    insert into "thrivedev"."dev_gold"."dim_conversation_start" ("id", "source_type", "conv_dataset_email", "priority", "message", "created_at", "get_date_at")
        (
            select "id", "source_type", "conv_dataset_email", "priority", "message", "created_at", "get_date_at"
            from "dim_conversation_start__dbt_tmp231915415832"
        )
  