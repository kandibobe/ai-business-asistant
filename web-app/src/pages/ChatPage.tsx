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
} from '@mui/material'
import {
  Send,
  SmartToy,
  Person,
  Clear,
} from '@mui/icons-material'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/store'
import { addMessage, sendMessageStart, sendMessageSuccess, sendMessageFailure, clearMessages } from '@/store/slices/chatSlice'
import { showSnackbar } from '@/store/slices/uiSlice'
import { chatApi } from '@/api/services'

export default function ChatPage() {
  const dispatch = useDispatch()
  const { messages, isLoading } = useSelector((state: RootState) => state.chat)
  const { user } = useSelector((state: RootState) => state.auth)
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
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            AI Chat
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Ask anything about your business or uploaded documents
          </Typography>
        </Box>
        <IconButton
          onClick={() => dispatch(clearMessages())}
          disabled={messages.length === 0}
        >
          <Clear />
        </IconButton>
      </Box>

      <Paper
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
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
              <SmartToy sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Start a conversation
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Ask me anything about your business, documents, or analytics
              </Typography>
            </Box>
          ) : (
            messages.map((message) => (
              <Box
                key={message.id}
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
                      bgcolor: message.role === 'user' ? 'primary.main' : 'secondary.main',
                    }}
                  >
                    {message.role === 'user' ? <Person /> : <SmartToy />}
                  </Avatar>
                  <Box>
                    <Paper
                      sx={{
                        p: 2,
                        backgroundColor:
                          message.role === 'user' ? 'primary.main' : 'background.paper',
                        color: message.role === 'user' ? 'white' : 'text.primary',
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
                          label={`${message.response_time}s`}
                          size="small"
                          sx={{ height: 20 }}
                        />
                      )}
                    </Box>
                  </Box>
                </Box>
              </Box>
            ))
          )}
          {isLoading && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Avatar sx={{ bgcolor: 'secondary.main' }}>
                <SmartToy />
              </Avatar>
              <CircularProgress size={24} />
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>

        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
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
            />
            <IconButton
              color="primary"
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              sx={{ alignSelf: 'flex-end' }}
            >
              <Send />
            </IconButton>
          </Box>
        </Box>
      </Paper>
    </Box>
  )
}
