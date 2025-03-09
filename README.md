# Emergency Incident Project

This project allows users to upload emergency incident data and view a timeline of dispatch events with interactive maps. The application displays incident locations, unit responses, and weather conditions during the incident.

A demo is hosted at [incidents.jsnellis.net](https://incidents.jsnellis.net)

## Installation

### Prerequisites
- Docker
- An API key for a weather service (this project uses [Meteostat](https://dev.meteostat.net/))

### Installation Steps (OSX/Linux)

**Note:** I don't have access to an osx machine, but as far as I can tell the setup for docker is roughly identical. These instructions were tested on my linux machine.

1. Clone the repository
   ```bash
   git clone git@github.com:jnellis3/Emergency-Incidents-Project.git
   cd Emergency-Incidents-Project
   ```

2. Create a `.env` file in the project root with your weather API credentials:
   ```
   WEATHER_URL=https://meteostat.p.rapidapi.com/point/hourly
   WEATHER_API_KEY=your_api_key_here
   WEATHER_API_HOST=meteostat.p.rapidapi.com
   ```

3. Build and start the Docker container:
   ```bash
   docker-compose up -d --build
   ```

4. Access the application at http://localhost:8001

### Usage

1. Use the drop zone at the top of the page to upload incident JSON files
2. Select incidents from the table that you would like included in the timeline
3. Click the "Play Timeline" button to see the incident response unfold on the map
4. View weather conditions and unit status updates in the information windows

Sample data is included in ./sample_data

## Future Improvements

There are many improvements to be made, but the current state at the very least provides a functional prototype.

1. **Better Error Handling**: I ran out of time to fully implement error handling in all functions. For example, if the weather API went down, my entire timeline functionality goes down with it.
2. **Better Design**: I would like to have added better markers and dashboard layouts. I would also want to add routes to connect dispatch events together. 
3. **Testing**: Add unit and integration tests for the backend and frontend components
4. **Advanced Filtering**: Add filtering options for incidents by type, date, etc. This is why I originally transformed the json data into sqlite as opposed to storing as is. If this scaled to 1000's of incidents, it would be cool to see what kind of filters could be applied.
5. **Caching**: Implement caching for weather data to reduce API calls. There's no reason we need to call the API every time a timeline starts.
6. **Enhanced Timeline**: Create a more interactive timeline with play/pause controls and speed adjustments
7. **Frontend Refactor**: The frontend really needs to be separated into multiple files to seperate concerns. Currently everything is in a single file.

## Time Spent

I spent probably 7 or 8 hours on this project, mostly from implementing the timeline functionality on the front end.
- 1 hour on initial setup and database design
- 1.5 hours on backend development (API endpoints, weather integration)
- 1.5 hours on frontend development (map integration, drop area, and table)
- 3 hours building timeline
- 1 hour documentation and deploying demo server

## Screenshots

### Dashboard Overview
![image](https://github.com/user-attachments/assets/3d0191a5-4b27-4688-b709-1747947ffefd)

### Incident Timeline
![image](https://github.com/user-attachments/assets/abf0530c-a0f8-437d-8b12-10fe4cb85924)

### Timeline Info Widget
![image](https://github.com/user-attachments/assets/df98b276-b5fd-4f84-bc8d-8541954dddae)


