{{
    config(
        materialized='incremental',
        alias='stg_dim_conversation_start',
        schema=var('silver_schema'),
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
    getdate() as get_date_at
from
    {{ var('bronze_schema') }}.ext_conversation_start