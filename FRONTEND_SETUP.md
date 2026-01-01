# Modern Frontend Setup Guide

This guide will help you set up the modern Next.js frontend with dark/light theme support.

## Architecture

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python) REST API
- **Communication**: REST API via HTTP

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.8+ (for backend)
- All existing Python dependencies installed

## Setup Instructions

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
# or
yarn install
```

### 2. Install Backend Dependencies

```bash
cd ../backend
pip install -r requirements.txt
```

### 3. Start the Backend API Server

```bash
# From the backend directory
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. Start the Frontend Development Server

```bash
# From the frontend directory
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`

## Quick Start (Windows)

Use the batch files:

```bash
# Start both servers
run_full_stack.bat

# Or start separately:
run_backend.bat    # Terminal 1
run_frontend.bat   # Terminal 2
```

## Features

### 🎨 Modern UI
- Beautiful, responsive design
- Smooth animations and transitions
- Professional color scheme
- Custom fonts (Inter & Poppins)

### 🌓 Dark/Light Theme
- Automatic theme detection based on system preferences
- Manual theme toggle button in header
- Theme preference saved in localStorage
- Smooth theme transitions

### 📊 Real-time Updates
- Live lead discovery updates
- Real-time statistics dashboard
- Status polling every 2 seconds

### 🔍 Advanced Features
- Search and filter leads
- Category selection with search
- Export leads to CSV
- Detailed lead cards with expandable sections
- Score-based filtering

## Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── layout.tsx         # Root layout with theme provider
│   ├── page.tsx           # Main page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── Header.tsx         # App header with theme toggle
│   ├── ThemeProvider.tsx  # Theme context provider
│   ├── ThemeToggle.tsx    # Theme toggle button
│   ├── DiscoveryPanel.tsx # Discovery configuration panel
│   ├── LeadsList.tsx      # Leads display component
│   └── StatsDashboard.tsx # Statistics dashboard
├── lib/                   # Utility functions
│   ├── api.ts            # API client
│   └── utils.ts          # Utility functions
└── public/               # Static assets

backend/
└── main.py               # FastAPI backend server
```

## API Endpoints

The backend provides these endpoints:

- `GET /status` - Get discovery status
- `POST /start` - Start discovery
- `POST /stop` - Stop discovery
- `GET /leads` - Get discovered leads
- `GET /countries` - Get list of countries
- `GET /categories` - Get list of categories
- `GET /stats` - Get statistics

## Development

### Frontend Development

```bash
cd frontend
npm run dev
```

### Backend Development

```bash
cd backend
python main.py
# or
uvicorn main:app --reload
```

### Build for Production

#### Frontend

```bash
cd frontend
npm run build
npm start
```

#### Backend

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Configuration

Make sure your `.env` file in the root directory is configured with:
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SHEETS_CREDENTIALS_PATH`
- `GOOGLE_MAPS_API_KEY` (optional but recommended)

## Troubleshooting

### Frontend won't start
- Make sure Node.js 18+ is installed
- Run `npm install` to install dependencies
- Check for port 3000 conflicts

### Backend API errors
- Make sure Python dependencies are installed
- Check that credentials.json exists
- Verify Google Sheets API is enabled
- Check that the spreadsheet is shared with the service account

### CORS errors
- Make sure backend is running on port 8000
- Check that CORS middleware is configured in backend/main.py
- Verify frontend is accessing the correct API URL

## Styling Customization

The app uses Tailwind CSS with custom configuration in `tailwind.config.js`.

Key colors:
- Primary: Blue shades (configurable)
- Success: Green
- Warning: Yellow
- Error: Red

To customize colors, edit `tailwind.config.js` and update the `colors` section.

## Theme Customization

Themes are defined in `app/globals.css` using CSS variables. You can customize:
- Background colors
- Text colors
- Border colors
- Card colors
- Muted colors

Edit the `:root` and `.dark` sections in `globals.css`.

## Deployment

### Frontend (Vercel/Netlify)

```bash
cd frontend
npm run build
# Deploy the .next folder
```

### Backend (Any Python hosting)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Make sure to:
- Set environment variables
- Install all dependencies
- Configure CORS for your frontend domain
- Use a production ASGI server like Gunicorn with Uvicorn workers

