import { useState, useRef, useEffect } from 'react'
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Avatar,
  CircularProgress,
  Chip,
  Fade,
  Zoom,
  Grow,
} from '@mui/material'
import {
  Send,
  SmartToy,
  Person,
  Clear,
  AutoAwesome,
} from '@mui/icons-material'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/store'
import { addMessage, sendMessageStart, sendMessageSuccess, sendMessageFailure, clearMessages } from '@/store/slices/chatSlice'
import { showSnackbar } from '@/store/slices/uiSlice'
import { chatApi } from '@/api/services'

export default function ChatPage() {
  const dispatch = useDispatch()
  const { messages, isLoading } = useSelector((state: RootState) => state.chat)
  const { activeDocument } = useSelector((state: RootState) => state.documents)
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    // Check if there's an active document
    if (!activeDocument) {
      dispatch(
        showSnackbar({
          message: 'Please upload and activate a document first',
          severity: 'warning',
        })
      )
      return
    }

    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: input,
      timestamp: new Date().toISOString(),
    }

    dispatch(addMessage(userMessage))
    setInput('')
    dispatch(sendMessageStart())

    try {
      const response = await chatApi.sendMessage(input, activeDocument.id)

      const aiMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: response.message,
        timestamp: new Date().toISOString(),
        response_time: response.response_time_ms / 1000, // Convert to seconds
      }

      dispatch(sendMessageSuccess(aiMessage))
    } catch (error: any) {
      dispatch(sendMessageFailure(error.message))
      dispatch(
        showSnackbar({
          message: `AI error: ${error.message}`,
          severity: 'error',
        })
      )
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <Box sx={{ height: 'calc(100vh - 140px)', display: 'flex', flexDirection: 'column' }}>
      <Fade in={true} timeout={600}>
        <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              💬 AI Chat
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Ask anything about your business or uploaded documents
            </Typography>
          </Box>
          <IconButton
            onClick={() => dispatch(clearMessages())}
            disabled={messages.length === 0}
            sx={{
              transition: 'all 0.2s ease',
              '&:hover': {
                transform: 'rotate(90deg) scale(1.1)',
              },
            }}
          >
            <Clear />
          </IconButton>
        </Box>
      </Fade>

      <Fade in={true} timeout={800}>
        <Paper
          sx={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            boxShadow: 4,
            transition: 'box-shadow 0.3s ease',
            '&:hover': {
              boxShadow: 6,
            },
          }}
        >
          <Box
            sx={{
              flex: 1,
              overflowY: 'auto',
              p: 3,
              backgroundColor: 'background.default',
            }}
          >
            {messages.length === 0 ? (
              <Zoom in={true} timeout={600}>
                <Box
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    textAlign: 'center',
                  }}
                >
                  <Box
                    sx={{
                      position: 'relative',
                      mb: 3,
                    }}
                  >
                    <SmartToy sx={{ fontSize: 80, color: 'primary.main', opacity: 0.8 }} />
                    <AutoAwesome
                      sx={{
                        position: 'absolute',
                        top: -10,
                        right: -10,
                        fontSize: 28,
                        color: 'warning.main',
                        animation: 'pulse 2s ease-in-out infinite',
                        '@keyframes pulse': {
                          '0%, 100%': { opacity: 1, transform: 'scale(1)' },
                          '50%': { opacity: 0.5, transform: 'scale(1.2)' },
                        },
                      }}
                    />
                  </Box>
                  <Typography variant="h5" fontWeight={600} gutterBottom>
                    Start a conversation
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    Ask me anything about your business, documents, or analytics
                  </Typography>
                </Box>
              </Zoom>
            ) : (
              messages.map((message, index) => (
                <Grow key={message.id} in={true} timeout={400 + index * 100}>
                  <Box
                    sx={{
                      display: 'flex',
                      mb: 3,
                      justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                    }}
                  >
                    <Box
                      sx={{
                        display: 'flex',
                        maxWidth: '70%',
                        gap: 2,
                        flexDirection: message.role === 'user' ? 'row-reverse' : 'row',
                      }}
                    >
                      <Avatar
                        sx={{
                          bgcolor: message.role === 'user'
                            ? 'primary.main'
                            : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          background: message.role === 'assistant'
                            ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                            : undefined,
                        }}
                      >
                        {message.role === 'user' ? <Person /> : <SmartToy />}
                      </Avatar>
                      <Box>
                        <Paper
                          elevation={2}
                          sx={{
                            p: 2,
                            backgroundColor:
                              message.role === 'user' ? 'primary.main' : 'background.paper',
                            color: message.role === 'user' ? 'white' : 'text.primary',
                            borderRadius: 2,
                            transition: 'all 0.2s ease',
                            '&:hover': {
                              transform: 'translateY(-2px)',
                              boxShadow: 4,
                            },
                          }}
                        >
                          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                            {message.content}
                          </Typography>
                        </Paper>
                        <Box sx={{ mt: 1, display: 'flex', gap: 1, alignItems: 'center' }}>
                          <Typography variant="caption" color="text.secondary">
                            {new Date(message.timestamp).toLocaleTimeString()}
                          </Typography>
                          {message.response_time && (
                            <Chip
                              label={`⚡ ${message.response_time}s`}
                              size="small"
                              sx={{
                                height: 20,
                                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                color: 'white',
                              }}
                            />
                          )}
                        </Box>
                      </Box>
                    </Box>
                  </Box>
                </Grow>
              ))
            )}
            {isLoading && (
              <Fade in={true} timeout={300}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Avatar
                    sx={{
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    }}
                  >
                    <SmartToy />
                  </Avatar>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Box
                      sx={{
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        bgcolor: 'primary.main',
                        animation: 'bounce 1s ease-in-out infinite',
                        '@keyframes bounce': {
                          '0%, 80%, 100%': { transform: 'scale(0)' },
                          '40%': { transform: 'scale(1)' },
                        },
                      }}
                    />
                    <Box
                      sx={{
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        bgcolor: 'primary.main',
                        animation: 'bounce 1s ease-in-out 0.2s infinite',
                      }}
                    />
                    <Box
                      sx={{
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        bgcolor: 'primary.main',
                        animation: 'bounce 1s ease-in-out 0.4s infinite',
                      }}
                    />
                  </Box>
                </Box>
              </Fade>
            )}
            <div ref={messagesEndRef} />
          </Box>

          <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider', bgcolor: 'background.paper' }}>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                fullWidth
                multiline
                maxRows={4}
                placeholder="Type your message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                  },
                }}
              />
              <IconButton
                color="primary"
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                sx={{
                  alignSelf: 'flex-end',
                  background: input.trim() ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : undefined,
                  color: input.trim() ? 'white' : undefined,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'scale(1.1) rotate(15deg)',
                    background: input.trim() ? 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)' : undefined,
                  },
                  '&:disabled': {
                    background: 'transparent',
                  },
                }}
              >
                <Send />
              </IconButton>
            </Box>
          </Box>
        </Paper>
      </Fade>
    </Box>
  )
}
