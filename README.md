# Data Visualization Project: Analysis of the Connection Between Music and Globalization

## Project Overview

This project explores the impact of **globalization on music** by analyzing how various musical genres, collaborations, and trends have evolved globally. The analysis focuses on how international collaborations have shaped modern music and how different genres have grown or diminished in popularity over time. The project was developed as part of the *Data Visualization* course at **Universidad Politécnica de Madrid**.

The visualizations were created using data fetched from **Spotify** and **MusicBrainz** APIs and include insights into:
- International music collaborations
- Genre evolution over time
- Geographic trends in music

## Data Sources

The data for this project was gathered from:
- **Spotify API**: Used to collect information on artists, albums, and songs.
- **MusicBrainz API**: Used to complement missing data, particularly for artists' country of origin.

### Datasets:
1. **Artists**: Contains artist details like name, country, genre, and popularity.
2. **Albums**: Includes album names, release dates, and main artists.
3. **Songs**: Contains song names, album information, and popularity scores.
4. **Featurings**: Includes collaborations between artists, represented by song and artist IDs.

## Visualization Components

The project is divided into three key interactive visualizations, each providing insights into the relationship between music and globalization:

### 1. International Collaborations Over Time
A **line chart** displays the number of international music collaborations (featurings) over time. Users can filter by regions (North America, Latin America, and Europe) and compare trends. The chart illustrates how cross-border collaborations have significantly increased in recent years, emphasizing the role of globalization in modern music.

### 2. Comparative Network Analysis
An **interactive network graph** shows the collaborations between artists from different continents. The nodes represent artists, and the edges represent collaborations. Users can compare collaboration patterns between different time periods, offering a clear visualization of how musical ties between regions have evolved.

### 3. Genre Evolution Over Time
A **bar chart** visualizes the number of songs released in different genres (e.g., pop, rock, hip-hop, Latin, etc.) across multiple decades. Users can adjust the time range and observe how the popularity of genres has shifted, highlighting the rise of Latin music and the decline of others over specific periods.

## Technologies Used

The project was developed using **RStudio** with the following libraries:
- **Shiny**: To create the interactive web application.
- **ggplot2**: For creating line charts and bar charts.
- **networkD3**: For visualizing the collaboration network.
- **dplyr**: For data manipulation.
- **data.table**, **countrycode**, **lubridate**, **forcats**: For handling data and variables.

## Instructions to Run the Application

### Run Locally
To run the project locally:
1. Install **R** and **RStudio**.
2. Install the required R libraries using the following commands:
   ```r
   install.packages("shiny")
   install.packages("ggplot2")
   install.packages("networkD3")
   install.packages("dplyr")
   install.packages("data.table")
   install.packages("countrycode")
   install.packages("lubridate")
   install.packages("shinyjs")
   install.packages("forcats")
   ```
3. Clone or download the project files and ensure the following CSV files are in the correct path:
   - `artist.csv`
   - `albums.csv`
   - `songs.csv`
   - `featurings.csv`

4. Open the `.R` file in **RStudio** and run the app:
   ```r
   shiny::runApp()
   ```

## Contributions

This project was developed by:
- **Federico Paschetta**
- **Cecilia Peccolo**
- **Karla Gonzalez Romero**
