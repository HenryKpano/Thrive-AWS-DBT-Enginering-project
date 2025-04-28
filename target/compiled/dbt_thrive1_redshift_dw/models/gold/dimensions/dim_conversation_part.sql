

select
    id as part_id,
    conversation_id,
    conv_dataset_email,
    part_type,
    message,
    created_at,
    get_date_at
from
    "thrivedev"."dev_silver"."stg_dim_conversation_part"



    where get_date_at > (select max(get_date_at) from "thrivedev"."dev_gold"."dim_conversation_part")
