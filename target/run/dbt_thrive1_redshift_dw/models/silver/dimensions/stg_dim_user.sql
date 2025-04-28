
      
        
            
        delete from "thrivedev"."dev_silver"."stg_dim_user"
    where (id) in (
        select distinct id
        from "stg_dim_user__dbt_tmp231912214000" as DBT_INTERNAL_SOURCE
    )
    
    ;
    

    insert into "thrivedev"."dev_silver"."stg_dim_user" ("id", "name", "email", "is_customer", "get_date_at")
        (
            select "id", "name", "email", "is_customer", "get_date_at"
            from "stg_dim_user__dbt_tmp231912214000"
        )
  