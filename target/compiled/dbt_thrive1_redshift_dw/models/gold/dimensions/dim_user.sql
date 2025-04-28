

select
    id as user_id,
    name,
    email,
    is_customer,
    get_date_at
from
    "thrivedev"."dev_silver"."stg_dim_user"


    where get_date_at > (select max(get_date_at) from "thrivedev"."dev_gold"."dim_user")
