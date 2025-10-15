# Creating an ETL Pipeline with Spotify Data

The goal of this project is to build a data pipeline that extracts data on my recently played Spotify songs, cleans it, and loads it into a PostgreSQL database twice a day. This database can then be used to run queries and perform analytics on my listening trends.

## Project Features

- **Spotify API Integration:** Utilizes the "Get Recently Played Tracks" endpoint from the Spotify API to retrieve my recently played songs.
- **Data Cleaning:** Uses Python to clean and transform the retrieved data.
- **Data Storage:** Stores the cleaned data in a PostgreSQL database.
- **Workflow Automation:** Uses Apache Airflow within a Docker container to orchestrate the pipeline and schedule it to run every 12 hours.

<img width="2965" height="1349" alt="image" src="https://github.com/user-attachments/assets/97275a3f-5fc7-4097-ab52-36679a04987e" />

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

## Environment Variables

To run this project, you will need to create a `.env` file in the root of your project folder with the following variables:

- `CLIENT_ID`: Your Spotify client ID  
- `CLIENT_SECRET`: Your Spotify client secret  
- `AUTH_CODE`: Your authentication code provided after running the `authentication_code.py` script  
- `REFRESH_TOKEN`: Your refresh token provided after running the `refresh_token.py` script  
- `HOST`: Hostname for your PostgreSQL database  
- `PORT`: Port number for your PostgreSQL database  
- `DATABASE`: Name of your PostgreSQL database  
- `USERNAME`: Username for accessing your PostgreSQL database  
- `PASSWORD`: Password for your PostgreSQL database  

## Setup / Installation

1. Clone the repository: 
   ```bash
   git clone https://github.com/NathanielMekonen/Spotify_ETL_Pipeline_Project.git
   cd Spotify_ETL_Pipeline_Project

2. Create a `.env` file in the root directory of the project and add your variables as specified in the Environment Variables section above.

3. Run the `authentication_code.py` script to retrieve the authentication code and store it in your `.env` file.

4. Run the `refresh_token.py` script to retrieve the refresh token and store it in your `.env` file.

5. Use Docker Compose to build and run the services:
    ```bash
    docker-compose up --build

6. Open your browser and access the Airflow UI at http://localhost:8080
