{{
    config(
        materialized='incremental',
        alias='stg_dim_user',
        schema=var('silver_schema'),
        unique_key='id',
        incremental_strategy='delete+insert'
    )
}}

select
    id,
    name,
    email,
    is_customer,
    getdate() as get_date_at
from
    {{ var('bronze_schema') }}.ext_users