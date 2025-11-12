import { createContext, useContext, useState, useMemo, ReactNode } from 'react';
import { ThemeProvider, createTheme, CssBaseline, PaletteMode } from '@mui/material';

interface ThemeContextType {
  mode: PaletteMode;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType>({
  mode: 'light',
  toggleTheme: () => {},
});

export const useThemeMode = () => useContext(ThemeContext);

interface CustomThemeProviderProps {
  children: ReactNode;
}

export default function CustomThemeProvider({ children }: CustomThemeProviderProps) {
  const [mode, setMode] = useState<PaletteMode>(() => {
    // Load from localStorage or default to light
    const savedMode = localStorage.getItem('themeMode');
    return (savedMode === 'dark' ? 'dark' : 'light') as PaletteMode;
  });

  const toggleTheme = () => {
    setMode((prevMode) => {
      const newMode = prevMode === 'light' ? 'dark' : 'light';
      localStorage.setItem('themeMode', newMode);
      return newMode;
    });
  };

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          ...(mode === 'light'
            ? {
                // Light mode colors
                primary: {
                  main: '#667eea',
                  light: '#818cf8',
                  dark: '#5568d3',
                },
                secondary: {
                  main: '#764ba2',
                  light: '#9d6bc3',
                  dark: '#5e3c81',
                },
                background: {
                  default: '#f8fafc',
                  paper: '#ffffff',
                },
                success: {
                  main: '#10b981',
                  light: '#34d399',
                  dark: '#059669',
                },
                info: {
                  main: '#3b82f6',
                  light: '#60a5fa',
                  dark: '#2563eb',
                },
                warning: {
                  main: '#f59e0b',
                  light: '#fbbf24',
                  dark: '#d97706',
                },
                error: {
                  main: '#ef4444',
                  light: '#f87171',
                  dark: '#dc2626',
                },
              }
            : {
                // Dark mode colors
                primary: {
                  main: '#818cf8',
                  light: '#a5b4fc',
                  dark: '#667eea',
                },
                secondary: {
                  main: '#9d6bc3',
                  light: '#b794d6',
                  dark: '#764ba2',
                },
                background: {
                  default: '#0f172a',
                  paper: '#1e293b',
                },
                success: {
                  main: '#34d399',
                  light: '#6ee7b7',
                  dark: '#10b981',
                },
                info: {
                  main: '#60a5fa',
                  light: '#93c5fd',
                  dark: '#3b82f6',
                },
                warning: {
                  main: '#fbbf24',
                  light: '#fcd34d',
                  dark: '#f59e0b',
                },
                error: {
                  main: '#f87171',
                  light: '#fca5a5',
                  dark: '#ef4444',
                },
              }),
        },
        typography: {
          fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
          h1: {
            fontWeight: 700,
          },
          h2: {
            fontWeight: 700,
          },
          h3: {
            fontWeight: 600,
          },
          h4: {
            fontWeight: 600,
          },
          h5: {
            fontWeight: 600,
          },
          h6: {
            fontWeight: 600,
          },
          button: {
            textTransform: 'none',
            fontWeight: 600,
          },
        },
        shape: {
          borderRadius: 12,
        },
        shadows: [
          'none',
          '0px 2px 4px rgba(0,0,0,0.05)',
          '0px 4px 8px rgba(0,0,0,0.05)',
          '0px 8px 16px rgba(0,0,0,0.05)',
          '0px 12px 24px rgba(0,0,0,0.05)',
          '0px 16px 32px rgba(0,0,0,0.05)',
          '0px 20px 40px rgba(0,0,0,0.05)',
          '0px 24px 48px rgba(0,0,0,0.05)',
          '0px 32px 64px rgba(0,0,0,0.05)',
          ...Array(16).fill('none'),
        ] as any,
        components: {
          MuiButton: {
            styleOverrides: {
              root: {
                borderRadius: 10,
                padding: '10px 24px',
                fontSize: '0.95rem',
                boxShadow: 'none',
                '&:hover': {
                  boxShadow: '0px 4px 12px rgba(0,0,0,0.15)',
                },
              },
              contained: {
                background: mode === 'light'
                  ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  : 'linear-gradient(135deg, #818cf8 0%, #9d6bc3 100%)',
                '&:hover': {
                  background: mode === 'light'
                    ? 'linear-gradient(135deg, #5568d3 0%, #5e3c81 100%)'
                    : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                },
              },
            },
          },
          MuiPaper: {
            styleOverrides: {
              root: {
                backgroundImage: 'none',
              },
              elevation1: {
                boxShadow: '0px 2px 8px rgba(0,0,0,0.05)',
              },
              elevation2: {
                boxShadow: '0px 4px 12px rgba(0,0,0,0.05)',
              },
            },
          },
          MuiCard: {
            styleOverrides: {
              root: {
                borderRadius: 16,
                boxShadow: '0px 4px 12px rgba(0,0,0,0.05)',
              },
            },
          },
          MuiChip: {
            styleOverrides: {
              root: {
                fontWeight: 600,
              },
            },
          },
        },
      }),
    [mode]
  );

  return (
    <ThemeContext.Provider value={{ mode, toggleTheme }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
}
