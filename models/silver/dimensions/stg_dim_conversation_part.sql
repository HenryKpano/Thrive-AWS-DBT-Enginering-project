{{
    config(
        materialized='incremental',
        alias='stg_dim_conversation_part',
        schema=var('silver_schema'),
        unique_key='id',
        incremental_strategy='delete+insert'
    )
}}

select
    id, 
    conversation_id, 
    conv_dataset_email, 
    part_type, 
    message, 
    created_at,
    getdate() as get_date_at
from
    {{ var('bronze_schema') }}.ext_conversation_part