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
                
                ]
   
    - Run the command < docker compose build >
    
    - Run the command < docker compose up >
    
    - Open another terminal and cd into the dbt project folder in this case cd into dbt_thrive1_redshift_dw
    
    - Run the command < docker exec -it dbt_redshift_runner_new bash >
   
    - Test connections by running this command < dbt debug >


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
