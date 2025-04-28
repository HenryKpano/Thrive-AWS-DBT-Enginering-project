select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select is_customer
from "thrivedev"."dev_gold"."dim_user"
where is_customer is null



      
    ) dbt_internal_test