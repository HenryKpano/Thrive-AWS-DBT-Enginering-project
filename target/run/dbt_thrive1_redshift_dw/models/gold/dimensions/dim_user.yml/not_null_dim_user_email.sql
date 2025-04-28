select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select email
from "thrivedev"."dev_gold"."dim_user"
where email is null



      
    ) dbt_internal_test