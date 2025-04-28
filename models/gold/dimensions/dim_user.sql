{{
    config(
        materialized='incremental',
        alias='dim_user',
        schema=var('gold_schema'),
        unique_key='user_id',
        incremental_strategy='delete+insert'
    )
}}

select
    id as user_id,
    name,
    email,
    is_customer,
    get_date_at
from
    {{ ref('stg_dim_user') }}

{% if is_incremental() %}
    where get_date_at > (select max(get_date_at) from {{ this }})
{% endif %}