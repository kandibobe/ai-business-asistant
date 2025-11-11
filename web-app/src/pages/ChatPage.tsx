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
  Stack,
  Button,
  Tooltip,
  alpha,
  Fade,
  Divider,
  Card,
  CardContent,
} from '@mui/material'
import {
  Send,
  SmartToy,
  Person,
  Clear,
  ContentCopy,
  Check,
  Description,
  AutoAwesome,
  Lightbulb,
} from '@mui/icons-material'
import ReactMarkdown from 'react-markdown'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/store'
import {
  addMessage,
  sendMessageStart,
  sendMessageSuccess,
  sendMessageFailure,
  clearMessages,
} from '@/store/slices/chatSlice'
import { showSnackbar } from '@/store/slices/uiSlice'
import { chatApi } from '@/api/services'
import { gradients } from '@/theme'

const suggestedPrompts = [
  'Summarize this document',
  'What are the key points?',
  'Extract all important dates and numbers',
  'What are the main recommendations?',
  'Explain this in simple terms',
]

export default function ChatPage() {
  const dispatch = useDispatch()
  const { messages, isLoading } = useSelector((state: RootState) => state.chat)
  const { activeDocument } = useSelector((state: RootState) => state.documents)
  const [input, setInput] = useState('')
  const [copiedId, setCopiedId] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [isTyping, setIsTyping] = useState(false)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  const handleSend = async (text?: string) => {
    const messageText = text || input
    if (!messageText.trim() || isLoading) return

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
      content: messageText,
      timestamp: new Date().toISOString(),
    }

    dispatch(addMessage(userMessage))
    setInput('')
    dispatch(sendMessageStart())
    setIsTyping(true)

    // Simulate typing delay
    setTimeout(async () => {
      try {
        const response = await chatApi.sendMessage(messageText, activeDocument.id)

        const aiMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant' as const,
          content: response.message,
          timestamp: new Date().toISOString(),
          response_time: response.response_time_ms / 1000,
        }

        setIsTyping(false)
        dispatch(sendMessageSuccess(aiMessage))
      } catch (error: any) {
        setIsTyping(false)
        dispatch(sendMessageFailure(error.message))
        dispatch(
          showSnackbar({
            message: `AI error: ${error.message}`,
            severity: 'error',
          })
        )
      }
    }, 500)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleCopy = async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedId(id)
      setTimeout(() => setCopiedId(null), 2000)
    } catch (error) {
      console.error('Failed to copy:', error)
    }
  }

  const handleSuggestedPrompt = (prompt: string) => {
    setInput(prompt)
  }

  return (
    <Box sx={{ height: 'calc(100vh - 140px)', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ mb: 2 }}>
        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          justifyContent="space-between"
          alignItems={{ xs: 'flex-start', sm: 'center' }}
          spacing={2}
        >
          <Box>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              AI Chat Assistant
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Have a conversation with AI about your documents
            </Typography>
          </Box>
          <Stack direction="row" spacing={1} alignItems="center">
            {activeDocument && (
              <Chip
                icon={<Description />}
                label={activeDocument.file_name}
                color="success"
                variant="outlined"
                sx={{ maxWidth: 200 }}
              />
            )}
            <Tooltip title="Clear chat">
              <span>
                <IconButton
                  onClick={() => dispatch(clearMessages())}
                  disabled={messages.length === 0}
                  size="small"
                >
                  <Clear />
                </IconButton>
              </span>
            </Tooltip>
          </Stack>
        </Stack>
      </Box>

      <Paper
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          borderRadius: 3,
        }}
      >
        {/* Messages Area */}
        <Box
          sx={{
            flex: 1,
            overflowY: 'auto',
            p: 3,
            background: `linear-gradient(to bottom, ${alpha('#f8fafc', 0.5)}, #ffffff)`,
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
              <Box
                sx={{
                  width: 120,
                  height: 120,
                  borderRadius: '50%',
                  background: gradients.primary,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mb: 3,
                }}
              >
                <AutoAwesome sx={{ fontSize: 60, color: '#fff' }} />
              </Box>
              <Typography variant="h5" fontWeight={600} gutterBottom>
                Start a Conversation
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4, maxWidth: 400 }}>
                {activeDocument
                  ? `Ask me anything about "${activeDocument.file_name}"`
                  : 'Upload and activate a document to start chatting'}
              </Typography>

              {activeDocument && (
                <Box sx={{ width: '100%', maxWidth: 600 }}>
                  <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                    <Lightbulb sx={{ color: 'warning.main' }} />
                    <Typography variant="subtitle2" fontWeight={600}>
                      Suggested questions:
                    </Typography>
                  </Stack>
                  <Stack spacing={1.5}>
                    {suggestedPrompts.map((prompt, index) => (
                      <Fade in key={index} timeout={300 + index * 100}>
                        <Button
                          variant="outlined"
                          onClick={() => handleSuggestedPrompt(prompt)}
                          sx={{
                            justifyContent: 'flex-start',
                            textAlign: 'left',
                            py: 1.5,
                            px: 2,
                            borderRadius: 2,
                            textTransform: 'none',
                            '&:hover': {
                              borderColor: 'primary.main',
                              bgcolor: alpha('#6366f1', 0.05),
                            },
                          }}
                        >
                          {prompt}
                        </Button>
                      </Fade>
                    ))}
                  </Stack>
                </Box>
              )}
            </Box>
          ) : (
            <>
              {messages.map((message, index) => (
                <Fade in key={message.id} timeout={300}>
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
                        maxWidth: '75%',
                        gap: 2,
                        flexDirection: message.role === 'user' ? 'row-reverse' : 'row',
                      }}
                    >
                      <Avatar
                        sx={{
                          width: 40,
                          height: 40,
                          background:
                            message.role === 'user' ? gradients.primary : gradients.success,
                        }}
                      >
                        {message.role === 'user' ? <Person /> : <SmartToy />}
                      </Avatar>
                      <Box sx={{ flex: 1 }}>
                        <Paper
                          elevation={message.role === 'user' ? 0 : 1}
                          sx={{
                            p: 2.5,
                            background:
                              message.role === 'user'
                                ? gradients.primary
                                : 'background.paper',
                            color: message.role === 'user' ? '#fff' : 'text.primary',
                            borderRadius: 3,
                            position: 'relative',
                          }}
                        >
                          {message.role === 'assistant' ? (
                            <Box
                              sx={{
                                '& p': { my: 1 },
                                '& ul, & ol': { my: 1, pl: 3 },
                                '& li': { my: 0.5 },
                                '& code': {
                                  bgcolor: alpha('#000', 0.05),
                                  px: 1,
                                  py: 0.5,
                                  borderRadius: 1,
                                  fontSize: '0.9em',
                                },
                                '& pre': {
                                  bgcolor: alpha('#000', 0.05),
                                  p: 2,
                                  borderRadius: 2,
                                  overflowX: 'auto',
                                },
                              }}
                            >
                              <ReactMarkdown>{message.content}</ReactMarkdown>
                            </Box>
                          ) : (
                            <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                              {message.content}
                            </Typography>
                          )}

                          {message.role === 'assistant' && (
                            <Tooltip
                              title={copiedId === message.id ? 'Copied!' : 'Copy response'}
                            >
                              <IconButton
                                size="small"
                                onClick={() => handleCopy(message.content, message.id)}
                                sx={{
                                  position: 'absolute',
                                  top: 8,
                                  right: 8,
                                  opacity: 0.6,
                                  '&:hover': { opacity: 1 },
                                }}
                              >
                                {copiedId === message.id ? (
                                  <Check fontSize="small" />
                                ) : (
                                  <ContentCopy fontSize="small" />
                                )}
                              </IconButton>
                            </Tooltip>
                          )}
                        </Paper>
                        <Stack
                          direction="row"
                          spacing={1}
                          alignItems="center"
                          sx={{ mt: 1, px: 1 }}
                        >
                          <Typography variant="caption" color="text.secondary">
                            {new Date(message.timestamp).toLocaleTimeString('en-US', {
                              hour: '2-digit',
                              minute: '2-digit',
                            })}
                          </Typography>
                          {message.response_time && (
                            <Chip
                              label={`${message.response_time.toFixed(1)}s`}
                              size="small"
                              sx={{
                                height: 20,
                                fontSize: '0.7rem',
                                fontWeight: 600,
                              }}
                            />
                          )}
                        </Stack>
                      </Box>
                    </Box>
                  </Box>
                </Fade>
              ))}

              {/* Typing Indicator */}
              {isTyping && (
                <Fade in>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                    <Avatar
                      sx={{
                        width: 40,
                        height: 40,
                        background: gradients.success,
                      }}
                    >
                      <SmartToy />
                    </Avatar>
                    <Paper
                      sx={{
                        p: 2,
                        borderRadius: 3,
                        display: 'flex',
                        alignItems: 'center',
                        gap: 0.5,
                      }}
                    >
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: 'primary.main',
                          animation: 'pulse 1.4s ease-in-out infinite',
                          '@keyframes pulse': {
                            '0%, 100%': { opacity: 0.4 },
                            '50%': { opacity: 1 },
                          },
                        }}
                      />
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: 'primary.main',
                          animation: 'pulse 1.4s ease-in-out 0.2s infinite',
                          '@keyframes pulse': {
                            '0%, 100%': { opacity: 0.4 },
                            '50%': { opacity: 1 },
                          },
                        }}
                      />
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: 'primary.main',
                          animation: 'pulse 1.4s ease-in-out 0.4s infinite',
                          '@keyframes pulse': {
                            '0%, 100%': { opacity: 0.4 },
                            '50%': { opacity: 1 },
                          },
                        }}
                      />
                    </Paper>
                  </Box>
                </Fade>
              )}
            </>
          )}
          <div ref={messagesEndRef} />
        </Box>

        <Divider />

        {/* Input Area */}
        <Box sx={{ p: 2.5, bgcolor: 'background.paper' }}>
          {!activeDocument && (
            <Box sx={{ mb: 2, textAlign: 'center' }}>
              <Typography variant="caption" color="warning.main" fontWeight={600}>
                ⚠ Please activate a document to start chatting
              </Typography>
            </Box>
          )}
          <Stack direction="row" spacing={2} alignItems="flex-end">
            <TextField
              fullWidth
              multiline
              maxRows={4}
              placeholder={
                activeDocument
                  ? 'Ask a question about your document...'
                  : 'Activate a document to start'
              }
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading || !activeDocument}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3,
                },
              }}
            />
            <IconButton
              color="primary"
              onClick={() => handleSend()}
              disabled={!input.trim() || isLoading || !activeDocument}
              sx={{
                width: 48,
                height: 48,
                background: gradients.primary,
                color: '#fff',
                '&:hover': {
                  background: gradients.primary,
                  opacity: 0.9,
                },
                '&.Mui-disabled': {
                  background: alpha('#6366f1', 0.3),
                  color: '#fff',
                },
              }}
            >
              <Send />
            </IconButton>
          </Stack>
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            Press Enter to send, Shift+Enter for new line
          </Typography>
        </Box>
      </Paper>
    </Box>
  )
}
