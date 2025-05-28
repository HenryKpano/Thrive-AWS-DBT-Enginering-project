{{
    config(
        materialized='incremental',
        alias='stg_fact_comment_total',
        schema=var('silver_schema'),
        unique_key='name',
        incremental_strategy='delete+insert',
        primary_key='name',
        distribution='even'
    )
}}

select
 u.name,
 count(scp.part_type) as num_com
from
    {{ ref('stg_dim_user') }} u
left join {{ ref('stg_dim_conversation_part') }} scp
	on u.email = scp.conv_dataset_email
group by 1
order by 1 asc

