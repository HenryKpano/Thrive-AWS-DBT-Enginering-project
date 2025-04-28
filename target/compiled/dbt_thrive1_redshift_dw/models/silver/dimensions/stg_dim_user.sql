

select
    id,
    name,
    email,
    is_customer,
    getdate() as get_date_at
from
    dev_bronze.ext_users