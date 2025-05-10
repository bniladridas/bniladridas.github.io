# SyntharaAI Frontend Architecture

## Overview

The SyntharaAI frontend is built using vanilla HTML, CSS, and JavaScript without any frameworks or libraries. This approach ensures maximum compatibility and performance while keeping the codebase simple and maintainable.

## Core Components

### HTML Structure

The frontend is structured around several HTML files:

- `index.html`: Main landing page with chatbot integration
- `gallery.html`: Gallery of SyntharaAI features and capabilities
- `downloads.html`: Resources and downloads page
- `supply-chain.html`: Information about supply chain features
- `og-editor.html`: Open Graph image editor

### CSS Styling

The styling is implemented using vanilla CSS with:

- CSS variables for theming
- Responsive design using media queries
- Flexbox and Grid for layout
- Minimal animations and transitions

### JavaScript Functionality

The JavaScript functionality is implemented without any frameworks or libraries:

- DOM manipulation for UI updates
- Fetch API for backend communication
- Event listeners for user interactions
- Local storage for persistent settings

## Key Features

### Chatbot Interface

The chatbot interface is a key component of the frontend:

```
┌─────────────────────────────────────┐
│ Chatbot Header                    X │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Bot Message                   │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ User Message                  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Bot Message                   │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│ ┌─────────────────────┐ ┌─────────┐ │
│ │ Message Input       │ │ Send    │ │
│ └─────────────────────┘ └─────────┘ │
└─────────────────────────────────────┘
```

#### Chatbot Features

- **Message History**: Displaying past messages in the conversation
- **Typing Indicators**: Visual feedback when the bot is "typing"
- **User Input**: Text input for user messages
- **Send Button**: Button to send messages
- **Fullscreen Mode**: Expandable interface for better usability
- **File Upload**: Interface for uploading files for analysis

### File Upload and Analysis

The file upload and analysis interface allows users to:

- Upload multiple files
- View file metadata
- See analysis results
- Interact with the chatbot about the files

```
┌─────────────────────────────────────┐
│ File Upload                       X │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Drag and drop files here      │  │
│  │                               │  │
│  │ or click to select files      │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ file1.txt                   X │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ file2.csv                   X │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Analyze Files                 │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

### Responsive Design

The frontend is designed to be responsive and work on various devices:

- **Mobile**: Optimized for small screens with touch interactions
- **Tablet**: Adjusted layout for medium-sized screens
- **Desktop**: Full-featured interface for large screens

```
┌─────────────┐  ┌───────────────────┐  ┌─────────────────────────────┐
│             │  │                   │  │                             │
│  Mobile     │  │  Tablet           │  │  Desktop                    │
│  View       │  │  View             │  │  View                       │
│             │  │                   │  │                             │
│             │  │                   │  │                             │
│             │  │                   │  │                             │
│             │  │                   │  │                             │
│             │  │                   │  │                             │
│             │  │                   │  │                             │
│             │  │                   │  │                             │
│             │  │                   │  │                             │
└─────────────┘  └───────────────────┘  └─────────────────────────────┘
```

## JavaScript Architecture

The JavaScript code follows a modular approach:

### Event-Driven Architecture

The frontend uses an event-driven architecture:

- **Event Listeners**: Attached to DOM elements for user interactions
- **Event Handlers**: Functions that respond to events
- **Custom Events**: For communication between components

### API Communication

Communication with the backend is handled using the Fetch API:

- **GET Requests**: For retrieving data
- **POST Requests**: For sending data (chat messages, file uploads)
- **JSON Parsing**: For handling API responses
- **Error Handling**: For graceful degradation when API calls fail

### State Management

State management is handled using:

- **DOM State**: UI state reflected in the DOM
- **Local Variables**: For component-specific state
- **Local Storage**: For persistent settings

## Performance Considerations

The frontend is optimized for performance:

- **Minimal Dependencies**: No external libraries or frameworks
- **Efficient DOM Manipulation**: Minimizing reflows and repaints
- **Lazy Loading**: Loading resources only when needed
- **Responsive Images**: Using appropriate image sizes for different devices

## Accessibility

The frontend includes several accessibility features:

- **Semantic HTML**: Using appropriate HTML elements
- **ARIA Attributes**: For improved screen reader support
- **Keyboard Navigation**: For users who can't use a mouse
- **Color Contrast**: Ensuring sufficient contrast for readability

## File Structure

```
bniladridas.github.io/
├── index.html           # Main landing page
├── gallery.html         # Gallery page
├── downloads.html       # Downloads page
├── supply-chain.html    # Supply chain page
├── og-editor.html       # Open Graph editor
└── assets/
    ├── css/             # CSS styles
    ├── js/              # JavaScript files
    └── images/          # Image assets
```
