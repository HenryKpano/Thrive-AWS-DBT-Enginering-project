{{
    config(
        materialized='view',
        alias='fact_comment_total',
        schema=var('gold_schema'),
        unique_key='id',
        incremental_strategy='delete+insert',
        primary_key='id',
        distribution='even'
    )
}}


select
 u.name,
 count(scp.part_type) as num_com
from
    {{ ref('dim_user') }} u
left join {{ ref('dim_conversation_part') }} scp
	on u.email = scp.conv_dataset_email
group by 1
order by 1 asc
