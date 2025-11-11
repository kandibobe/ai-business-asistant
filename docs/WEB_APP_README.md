# AI Business Assistant - Web Application

## Overview

Modern React web application with TypeScript, Redux Toolkit, and Material-UI for AI Business Intelligence Agent. Full integration with REST API backend.

## Features Implemented

### ✅ Core Pages

- **Dashboard** - Overview with statistics, recent activity, quick actions
- **Documents** - Upload, manage, delete, activate documents with progress tracking
- **Chat** - AI chat with real-time responses using Gemini API
- **Analytics** - Usage statistics and performance metrics
- **Settings** - User preferences and AI configuration
- **Premium** - Upgrade options

### ✅ Authentication

- JWT token-based authentication
- Login/Register forms
- Protected routes
- Token refresh on expiration
- Persistent sessions

### ✅ Features

- Real API integration (no mock data)
- File upload with progress tracking (50MB max)
- Document management (upload, delete, activate)
- AI chat with response time tracking
- Settings persistence
- Notifications/Toast messages
- Error handling
- Loading states
- Responsive design

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Redux Toolkit** - State management
- **Material-UI (MUI)** - Component library
- **Axios** - HTTP client
- **React Router** - Navigation
- **Vite** - Build tool

## Installation

```bash
cd web-app

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at http://localhost:5173

## Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## Project Structure

```
web-app/
├── src/
│   ├── api/
│   │   ├── client.ts              # Axios instance with interceptors
│   │   └── services/              # API service modules
│   │       ├── authService.ts
│   │       ├── documentService.ts
│   │       ├── chatService.ts
│   │       ├── analyticsService.ts
│   │       └── settingsService.ts
│   ├── components/
│   │   └── layout/
│   │       └── MainLayout.tsx     # Main app layout
│   ├── pages/
│   │   ├── LoginPage.tsx          # Login/Register
│   │   ├── DashboardPage.tsx      # Dashboard
│   │   ├── DocumentsPage.tsx      # Document management
│   │   ├── ChatPage.tsx           # AI chat
│   │   ├── AnalyticsPage.tsx      # Analytics
│   │   ├── SettingsPage.tsx       # Settings
│   │   └── PremiumPage.tsx        # Premium upgrade
│   ├── store/
│   │   ├── index.ts               # Redux store
│   │   └── slices/                # Redux slices
│   │       ├── authSlice.ts
│   │       ├── documentsSlice.ts
│   │       ├── chatSlice.ts
│   │       └── settingsSlice.ts
│   ├── types/
│   │   └── index.ts               # TypeScript types
│   ├── App.tsx                    # Main app component
│   └── main.tsx                   # Entry point
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## API Integration

All API calls are made through service modules in `src/api/services/`:

### Authentication

```typescript
import { authService } from '@/api/services'

// Register
const response = await authService.register({
  username: 'user',
  password: 'pass',
  email: 'user@example.com'
})

// Login
const response = await authService.login({
  username: 'user',
  password: 'pass'
})

// Get current user
const user = await authService.me()
```

### Documents

```typescript
import { documentService } from '@/api/services'

// List documents
const response = await documentService.list()

// Upload with progress
await documentService.upload(file, (progress) => {
  console.log(`Upload progress: ${progress}%`)
})

// Delete document
await documentService.delete(documentId)

// Activate document
await documentService.activate(documentId)
```

### Chat

```typescript
import { chatService } from '@/api/services'

// Send message
const response = await chatService.sendMessage({
  message: 'What is this document about?',
  document_id: 1
})

// Get history
const history = await chatService.getHistory(documentId)
```

### Analytics

```typescript
import { analyticsService } from '@/api/services'

// Get user stats
const stats = await analyticsService.getUserStats()

// Get dashboard stats
const dashboard = await analyticsService.getDashboardStats()
```

### Settings

```typescript
import { settingsService } from '@/api/services'

// Get settings
const settings = await settingsService.get()

// Update settings
await settingsService.update({
  language: 'ru',
  ai_role: 'analyst'
})
```

## State Management

Using Redux Toolkit with typed slices:

```typescript
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/store'

const MyComponent = () => {
  const dispatch = useDispatch()
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth)
  const { documents, isLoading } = useSelector((state: RootState) => state.documents)

  // Dispatch actions
  dispatch(someAction())
}
```

## Pages

### 1. LoginPage
- Login form
- Register form
- Tab switching
- Form validation
- Error handling
- Redirect after login

### 2. DashboardPage
- Statistics cards (documents, questions, response time)
- Recent documents list
- Quick actions
- Premium upgrade CTA
- Real-time data from API

### 3. DocumentsPage ✅ Completed
- **File upload** with drag & drop support
- **Progress tracking** during upload
- **File validation** (type, size)
- **Document list** with grid layout
- **Delete confirmation** dialog
- **Activate/Deactivate** documents
- **Refresh** button
- **Loading states**
- **Notifications** for success/error
- **Active document** indicator

**Key Features:**
- Max file size: 50MB
- Supported formats: PDF, Excel, Word, Audio, Text
- Real-time upload progress
- Delete with confirmation
- Active document highlighting
- Format icons (PDF, Excel, Word)
- File size display
- Status badges (processed/pending)

### 4. ChatPage ✅ Completed
- **Real AI responses** from Gemini API
- **Message history** with timestamps
- **Response time** tracking
- **Loading indicator** during AI processing
- **Error handling** with user-friendly messages
- **Smooth scrolling** to new messages
- **Multi-line input** with Shift+Enter
- **Clear history** button

**Key Features:**
- Real-time chat with AI
- Shows response time for each answer
- User/AI message distinction
- Empty state for new chats
- Keyboard shortcut (Enter to send)

### 5. SettingsPage ✅ Completed
- **Profile information** display
- **Language selection** (EN, RU, DE)
- **AI role** configuration (Assistant, Analyst, Consultant, etc.)
- **Response style** (Brief, Standard, Detailed, etc.)
- **AI mode** (Fast, Standard, Advanced)
- **Notifications** toggle
- **Save/Reset** buttons
- **Real API** integration
- **Loading states**
- **Success/Error** notifications
- **Change tracking** (enable Save only when changed)

**Key Features:**
- Loads settings from API on mount
- Only sends changed fields to API
- Premium member badge
- Reset to original values
- Disabled Save button when no changes

### 6. AnalyticsPage
- Usage statistics
- Response time trends
- Document analysis
- Charts and graphs

### 7. PremiumPage
- Pricing plans
- Feature comparison
- Upgrade options

## Components

### MainLayout
- Sidebar navigation
- App bar with user info
- Logout button
- Theme toggle (dark/light)
- Responsive drawer

## Notifications System

Using Material-UI Snackbar with Alert:

```typescript
const [notification, setNotification] = useState({
  open: false,
  message: '',
  severity: 'success' | 'error' | 'info'
})

// Show notification
const showNotification = (message: string, severity: 'success' | 'error' | 'info') => {
  setNotification({ open: true, message, severity })
}

// In JSX
<Snackbar
  open={notification.open}
  autoHideDuration={6000}
  onClose={() => setNotification({ ...notification, open: false })}
>
  <Alert severity={notification.severity}>
    {notification.message}
  </Alert>
</Snackbar>
```

## Error Handling

Global error interceptor in axios client:

```typescript
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
    }
    return Promise.reject(error)
  }
)
```

## Loading States

All async operations show loading indicators:

```typescript
{isLoading ? (
  <CircularProgress />
) : (
  <Content />
)}
```

## Form Validation

Basic validation on all forms:

- Required fields
- Email format
- Password strength
- File size/type

## Responsive Design

Breakpoints:
- **xs**: < 600px (mobile)
- **sm**: 600px - 900px (tablet)
- **md**: 900px - 1200px (small desktop)
- **lg**: 1200px - 1536px (desktop)
- **xl**: > 1536px (large desktop)

## Building for Production

```bash
# Build
npm run build

# Preview build
npm run preview
```

Build output in `dist/` directory.

## Testing

```bash
# Run tests (when implemented)
npm test

# Run tests with coverage
npm run test:coverage
```

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy

# Deploy to production
netlify deploy --prod
```

### Static Hosting

Build and upload `dist/` folder to any static hosting:
- AWS S3 + CloudFront
- GitHub Pages
- Firebase Hosting
- Cloudflare Pages

## Environment Setup

### Development

```bash
# .env.development
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### Production

```bash
# .env.production
VITE_API_URL=https://api.yourdomain.com
VITE_WS_URL=wss://api.yourdomain.com
```

## Troubleshooting

### CORS Errors

If you get CORS errors, ensure the API server has the correct origins in `api/main.py`:

```python
origins = [
    "http://localhost:5173",  # Vite dev server
    "https://yourdomain.com"  # Production domain
]
```

### 401 Unauthorized

If you get 401 errors, check:
1. Token is stored in localStorage
2. Token is not expired
3. Authorization header is set correctly

### File Upload Fails

Check:
1. File size < 50MB
2. File type is supported
3. API endpoint is correct
4. CORS allows file uploads

## Future Enhancements

- [ ] WebSocket real-time chat
- [ ] Error boundaries
- [ ] Skeleton loaders
- [ ] Chart visualizations
- [ ] Export functionality
- [ ] Dark mode persistence
- [ ] i18n (internationalization)
- [ ] PWA support
- [ ] Unit tests
- [ ] E2E tests

## License

MIT

## Support

For issues and questions, create an issue on GitHub.
