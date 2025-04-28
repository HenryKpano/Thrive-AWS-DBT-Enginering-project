

select
    id, 
    conversation_id, 
    conv_dataset_email, 
    part_type, 
    message, 
    created_at,
    getdate() as get_date_at
from
    dev_bronze.ext_conversation_part