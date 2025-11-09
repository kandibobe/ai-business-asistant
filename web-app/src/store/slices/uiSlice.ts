import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface UiState {
  isSidebarOpen: boolean
  isDrawerOpen: boolean
  currentPage: string
  snackbar: {
    open: boolean
    message: string
    severity: 'success' | 'error' | 'warning' | 'info'
  }
}

const initialState: UiState = {
  isSidebarOpen: true,
  isDrawerOpen: false,
  currentPage: 'dashboard',
  snackbar: {
    open: false,
    message: '',
    severity: 'info',
  },
}

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.isSidebarOpen = !state.isSidebarOpen
    },
    toggleDrawer: (state) => {
      state.isDrawerOpen = !state.isDrawerOpen
    },
    setCurrentPage: (state, action: PayloadAction<string>) => {
      state.currentPage = action.payload
    },
    showSnackbar: (
      state,
      action: PayloadAction<{
        message: string
        severity?: 'success' | 'error' | 'warning' | 'info'
      }>
    ) => {
      state.snackbar = {
        open: true,
        message: action.payload.message,
        severity: action.payload.severity || 'info',
      }
    },
    hideSnackbar: (state) => {
      state.snackbar.open = false
    },
  },
})

export const {
  toggleSidebar,
  toggleDrawer,
  setCurrentPage,
  showSnackbar,
  hideSnackbar,
} = uiSlice.actions

export default uiSlice.reducer
