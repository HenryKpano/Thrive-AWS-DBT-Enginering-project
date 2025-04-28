select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select name
from "thrivedev"."dev_gold"."dim_user"
where name is null



      
    ) dbt_internal_test