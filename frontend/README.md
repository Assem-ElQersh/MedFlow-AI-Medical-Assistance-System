# MedFlow Frontend

The frontend application for MedFlow, a comprehensive medical assistance system.

## Features

- Modern React application with TypeScript
- Material-UI components for a polished user interface
- Form validation with Zod
- Error handling and logging
- Responsive design
- Real-time updates for emergency cases
- Image upload and analysis
- Specialist matching and scheduling

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

2. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run test` - Run tests
- `npm run test:coverage` - Run tests with coverage
- `npm run format` - Format code with Prettier
- `npm run type-check` - Check TypeScript types

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── services/      # API and utility services
├── hooks/         # Custom React hooks
├── contexts/      # React contexts
├── utils/         # Utility functions
├── types/         # TypeScript type definitions
├── assets/        # Static assets
└── App.tsx        # Root component
```

## Development

### Code Style

- We use ESLint and Prettier for code formatting
- Run `npm run format` to format all files
- Run `npm run lint` to check for linting issues

### TypeScript

- Strict type checking is enabled
- Run `npm run type-check` to check for type errors
- Use proper type definitions for all components and functions

### Testing

- We use Vitest for testing
- Write tests for components and utilities
- Run `npm run test` to execute tests
- Run `npm run test:coverage` for coverage report

## Building for Production

1. Build the application:
   ```bash
   npm run build
   # or
   yarn build
   ```

2. Preview the production build:
   ```bash
   npm run preview
   # or
   yarn preview
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
VITE_API_URL=http://localhost:8000
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and ensure they pass
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 