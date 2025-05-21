{{
    config(
        materialized='incremental',
        alias='dim_conversation_part',
        schema=var('gold_schema'),
        unique_key='part_id',
        incremental_strategy='delete+insert'
    )
}}

select
    id as part_id,
    conversation_id,
    conv_dataset_email,
    part_type,
    message,
    created_at,
    get_date_at
from
    {{ ref('stg_dim_conversation_part') }}


{% if is_incremental() %}
    where get_date_at > (select max(get_date_at) from {{ this }})
{% endif %}