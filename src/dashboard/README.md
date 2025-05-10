# DocuMetrics React Dashboard

A modern React dashboard for visualizing code documentation quality metrics with an immersive aquatic and neon (toggleable) theme.

## Features

- **Interactive Visualizations**
  - Gauge charts for individual metrics
  - Radar chart for comprehensive metric comparison
  - Scatter plot for file-by-file comparison
  
- **Project Management**
  - Folder selection for analyzing entire projects
  - Project overview with aggregate metrics
  
- **Engaging User Interface**
  - Immersive aquatic theme with animated fish, bubbles, and seaweed
  - Toggleable themes (Aquatic and Neon-Futuristic)
  - Responsive design for all device sizes

## Getting Started

### Prerequisites

- Node.js (v14+)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server
npm run dev
```

### Building for Production

```bash
# Create production build
npm run build
```

### API Integration

The dashboard connects to the Flask backend through a REST API. The API adapter is provided in `api_adapter.py`.

## Technologies Used

- React for component-based UI
- Tailwind CSS for styling
- Chart.js for data visualization
- Vite for project bundling

## Project Structure

- `components/` - UI components
  - `common/` - Reusable UI elements and animations
  - `layout/` - Page layouts and navigation
  - `views/` - Main page views (Welcome, Results, Details)
  - `charts/` - Data visualization components
- `contexts/` - React context providers
- `hooks/` - Custom React hooks
- `services/` - API service functions
- `styles/` - CSS and theme files
- `utils/` - Utility functions