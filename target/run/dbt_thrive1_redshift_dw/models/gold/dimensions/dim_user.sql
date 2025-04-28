
      
        
            
        delete from "thrivedev"."dev_gold"."dim_user"
    where (user_id) in (
        select distinct user_id
        from "dim_user__dbt_tmp231915660164" as DBT_INTERNAL_SOURCE
    )
    
    ;
    

    insert into "thrivedev"."dev_gold"."dim_user" ("user_id", "name", "email", "is_customer", "get_date_at")
        (
            select "user_id", "name", "email", "is_customer", "get_date_at"
            from "dim_user__dbt_tmp231915660164"
        )
  