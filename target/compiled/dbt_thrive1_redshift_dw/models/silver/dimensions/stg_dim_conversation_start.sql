

select
    id, 
    source_type, 
    conv_dataset_email, 
    priority, 
    message, 
    created_at,
    getdate() as get_date_at
from
    dev_bronze.ext_conversation_start