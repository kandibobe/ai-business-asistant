import { Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { RootState } from './store'
import MainLayout from './components/layout/MainLayout'
import ErrorBoundary from './components/ErrorBoundary'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import DocumentsPage from './pages/DocumentsPage'
import ChatPage from './pages/ChatPage'
import AnalyticsPage from './pages/AnalyticsPage'
import SettingsPage from './pages/SettingsPage'
import PremiumPage from './pages/PremiumPage'

function App() {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth)

  return (
    <ErrorBoundary>
      <Routes>
      {/* Public routes */}
      <Route
        path="/login"
        element={!isAuthenticated ? <LoginPage /> : <Navigate to="/dashboard" replace />}
      />

      {/* Protected routes */}
      <Route
        path="/"
        element={isAuthenticated ? <MainLayout /> : <Navigate to="/login" replace />}
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="documents" element={<DocumentsPage />} />
        <Route path="chat" element={<ChatPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="settings" element={<SettingsPage />} />
        <Route path="premium" element={<PremiumPage />} />
      </Route>

      {/* Catch all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
    </ErrorBoundary>
  )
}

export default App
