{{
    config(
        materialized='incremental',
        alias='dim_conversation_start',
        schema=var('gold_schema'),
        unique_key='id',
        incremental_strategy='delete+insert'
    )
}}

select
    id, 
    source_type, 
    conv_dataset_email, 
    priority, 
    message, 
    created_at,
    get_date_at
from
    {{ ref('stg_dim_conversation_start') }}

{% if is_incremental() %}
    where get_date_at > (select max(get_date_at) from {{ this }})
{% endif %}