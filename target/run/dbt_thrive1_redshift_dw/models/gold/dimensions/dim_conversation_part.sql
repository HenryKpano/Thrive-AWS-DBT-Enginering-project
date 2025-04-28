
      
        
            
        delete from "thrivedev"."dev_gold"."dim_conversation_part"
    where (part_id) in (
        select distinct part_id
        from "dim_conversation_part__dbt_tmp231915665187" as DBT_INTERNAL_SOURCE
    )
    
    ;
    

    insert into "thrivedev"."dev_gold"."dim_conversation_part" ("part_id", "conversation_id", "conv_dataset_email", "part_type", "message", "created_at", "get_date_at")
        (
            select "part_id", "conversation_id", "conv_dataset_email", "part_type", "message", "created_at", "get_date_at"
            from "dim_conversation_part__dbt_tmp231915665187"
        )
  