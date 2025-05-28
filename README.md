Welcome to my dbt CRM Project

### Using the starter project

To run this project follow the steps below:
    
    - Start your Desktop docker app
    
    
    - In your terminal run the commands
        
        
        - Make sure to cd into this folder on your terminal
        
        
        - Create a .env file in the folder
            
            
            - the .env contains your cloud credential as follows replace the credentials with yours
                
                
                [
                    
                    REDSHIFT_HOST=my-cluster.redshift.amazonaws.com
                    
                    REDSHIFT_USER=myuser
                    
                    REDSHIFT_PASSWORD=mypassword
                    
                    REDSHIFT_PORT=5439
                    
                    REDSHIFT_DB=mydatabase
                    
                    REDSHIFT_SCHEMA=analytics

                    FERNET_KEY=eDrO0WTZs0djv9r
                    
                    AIRFLOW__WEBSERVER__SECRET_KEY=oJQhrzE1fUgP8Uf
                
                ]
   
    - docker compose run airflow-webserver airflow db init
    
    - docker compose run airflow-webserver airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin

    - Run the command < docker compose build >
    
    - Run the command < docker compose up >
    
    - After running docker compose up, Docker runs the dbt debug as part of the checks. This will show in the logs if it run successfully. 
    
    - To schedule dbt test or dbt compile, or dbt run to build materialization, write Airflow Dags to perform such task.
   


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
