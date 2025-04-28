

select
    id, 
    source_type, 
    conv_dataset_email, 
    priority, 
    message, 
    created_at,
    get_date_at
from
    "thrivedev"."dev_silver"."stg_dim_conversation_start"


    where get_date_at > (select max(get_date_at) from "thrivedev"."dev_gold"."dim_conversation_start")
