# Travel Recommendation and Itinerary Planner (India)

This project is a full-stack web application that recommends travel destinations in India based on user preferences and generates a customized itinerary with a map view of tourist attractions.

---

## Features

### Travel Planning Workflow
- Multi-step guided process:
  - Select preferences
  - View destination recommendations
  - Customize trip details
  - Generate itinerary and explore map

### Recommendation Criteria
- Region (North, South, East, West, Northeast India)
- Climate preference
- Interests (Spiritual, Wildlife, Beaches, Hill Stations, etc.)
- Budget level (Budget, Mid-range, Premium)

### Trip Customization
- Number of days
- Daily budget
- Additional preferred interests

### Output
- Day-wise itinerary generation
- Interactive map visualization of attractions
- Suggested nearby places if time/budget allow
- Fully responsive design with light/dark mode support

---

## Tech Stack

### Frontend
- React + Vite
- Tailwind CSS
- React Router DOM
- Leaflet (map rendering)

### Backend
- FastAPI (Python)
- Deployments: Render (Backend), Vercel (Frontend)

---

## Application Workflow

1. User selects preferences (budget, climate, interests, region)
2. Application recommends matching Indian destinations
3. User selects a destination and customizes days and budget
4. A day-wise itinerary is generated
5. Map view and nearby attractions are displayed

---

## API Endpoints

| Functionality | Method | Endpoint |
|--------------|:------:|----------|
| Health check | GET | `/api/health` |
| Metadata | GET | `/api/meta` |
| Destination recommendation | POST | `/api/recommend-destinations` |
| Itinerary generation | POST | `/api/generate-itinerary` |
| Nearby attractions | POST | `/api/nearby` |

---

## Screenshots

Screenshots of each workflow step are included:
- Preferences page
  <img width="1530" height="901" alt="image" src="https://github.com/user-attachments/assets/d6c1f7c2-1a0b-46d2-9dfb-14b2b9987904" />

- Destination recommendations page
  <img width="1710" height="597" alt="image" src="https://github.com/user-attachments/assets/48d3c02c-a514-4632-84ce-c89482cd7aa0" />

- Customization page
  <img width="1545" height="608" alt="image" src="https://github.com/user-attachments/assets/4425c1ad-41fc-44b0-a75d-bd491b1a43ce" />

- Itinerary and map view
  <img width="1646" height="944" alt="image" src="https://github.com/user-attachments/assets/93d9050b-e708-410b-aaaf-fa4a7a8d390e" />





