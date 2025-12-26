*Travel Recommendation and Itinerary Planner (India)*
This project is a full-stack web application that recommends travel destinations in India based on user preferences and generates a customized itinerary with a map view of tourist attractions.

Features:
Multi-step travel planning workflow
Destination recommendations based on:
Region
Climate
Interests
Budget level

Trip customization:
Number of days
Daily budget
Interest refinement
Day-wise itinerary generation
Map visualization of key attractions
Suggestions for nearby tourist spots for extra time/budget
Fully responsive and supports light/dark mode

Tech Stack:
Frontend:
React + Vite
Tailwind CSS
React Router DOM
Leaflet (Map rendering)

Backend:
FastAPI (Python)
Render for deployment

Deployment:
Frontend: Vercel
Backend: Render

Application Workflow:
User selects preferences (budget, climate, interests, region)
App recommends suitable destinations in India
User selects a destination and customizes trip details
App generates a day-wise itinerary with attraction recommendations and map view
Suggestions for nearby places if time/budget allow

API Endpoints:
Functionality	Method	Endpoint
Health check	GET	/api/health
Metadata	GET	/api/meta
Destination recommendation	POST	/api/recommend-destinations
Itinerary generation	POST	/api/generate-itinerary
Nearby attractions	POST	/api/nearby

Screenshots of each part of the workflow are included in the repository for reference:
Preferences page
<img width="1530" height="901" alt="image" src="https://github.com/user-attachments/assets/d6c1f7c2-1a0b-46d2-9dfb-14b2b9987904" />

Destination recommendations page
<img width="1710" height="597" alt="image" src="https://github.com/user-attachments/assets/48d3c02c-a514-4632-84ce-c89482cd7aa0" />

Customization page
<img width="1545" height="608" alt="image" src="https://github.com/user-attachments/assets/4425c1ad-41fc-44b0-a75d-bd491b1a43ce" />

Itinerary and map view
<img width="1646" height="944" alt="image" src="https://github.com/user-attachments/assets/93d9050b-e708-410b-aaaf-fa4a7a8d390e" />


