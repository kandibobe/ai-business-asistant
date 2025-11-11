import { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  IconButton,
  Chip,
  LinearProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material'
import {
  CloudUpload,
  Description,
  PictureAsPdf,
  TableChart,
  Article,
  Link as LinkIcon,
  Delete,
  Visibility,
  CheckCircle,
} from '@mui/icons-material'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '@/store'
import {
  fetchDocumentsStart,
  fetchDocumentsSuccess,
  fetchDocumentsFailure,
  uploadStart,
  uploadProgress as setUploadProgress,
  uploadSuccess,
  uploadFailure,
  setActiveDocument,
  deleteDocument as deleteDocumentAction,
} from '@/store/slices/documentsSlice'
import { showSnackbar } from '@/store/slices/uiSlice'
import { documentsApi } from '@/api/services'

export default function DocumentsPage() {
  const dispatch = useDispatch()
  const { documents, isUploading, uploadProgress, activeDocument, error } = useSelector(
    (state: RootState) => state.documents
  )
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [deleteDialog, setDeleteDialog] = useState<{
    open: boolean
    documentId: number | null
    documentName: string
  }>({
    open: false,
    documentId: null,
    documentName: '',
  })

  // Load documents on mount
  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      dispatch(fetchDocumentsStart())
      const response = await documentsApi.list()
      dispatch(fetchDocumentsSuccess(response.documents))

      // Set active document if exists
      if (response.active_document_id) {
        const activeDoc = response.documents.find(
          (doc) => doc.id === response.active_document_id
        )
        if (activeDoc) {
          dispatch(setActiveDocument(activeDoc))
        }
      }
    } catch (error: any) {
      dispatch(fetchDocumentsFailure(error.message))
    }
  }

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0]

      // Validate file size (50MB max)
      const maxSize = 50 * 1024 * 1024
      if (file.size > maxSize) {
        dispatch(
          showSnackbar({
            message: 'File size exceeds 50MB limit',
            severity: 'error',
          })
        )
        return
      }

      setSelectedFile(file)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    try {
      dispatch(uploadStart())
      const document = await documentsApi.upload(selectedFile, (progress) => {
        dispatch(setUploadProgress(progress))
      })

      dispatch(uploadSuccess(document))
      dispatch(
        showSnackbar({
          message: 'Document uploaded successfully!',
          severity: 'success',
        })
      )
      setSelectedFile(null)

      // Reload documents to get updated list
      loadDocuments()
    } catch (error: any) {
      dispatch(uploadFailure(error.message))
      dispatch(
        showSnackbar({
          message: `Upload failed: ${error.message}`,
          severity: 'error',
        })
      )
    }
  }

  const handleActivate = async (documentId: number) => {
    try {
      await documentsApi.activate(documentId)
      const doc = documents.find((d) => d.id === documentId)
      if (doc) {
        dispatch(setActiveDocument(doc))
        dispatch(
          showSnackbar({
            message: 'Document activated',
            severity: 'success',
          })
        )
      }
    } catch (error: any) {
      dispatch(
        showSnackbar({
          message: `Failed to activate: ${error.message}`,
          severity: 'error',
        })
      )
    }
  }

  const handleDeleteClick = (documentId: number, documentName: string) => {
    setDeleteDialog({
      open: true,
      documentId,
      documentName,
    })
  }

  const handleDeleteConfirm = async () => {
    if (!deleteDialog.documentId) return

    try {
      await documentsApi.delete(deleteDialog.documentId)
      dispatch(deleteDocumentAction(deleteDialog.documentId))
      dispatch(
        showSnackbar({
          message: 'Document deleted',
          severity: 'success',
        })
      )
      setDeleteDialog({ open: false, documentId: null, documentName: '' })
    } catch (error: any) {
      dispatch(
        showSnackbar({
          message: `Failed to delete: ${error.message}`,
          severity: 'error',
        })
      )
    }
  }

  const getDocumentIcon = (type: string) => {
    switch (type) {
      case 'pdf':
        return <PictureAsPdf />
      case 'excel':
        return <TableChart />
      case 'word':
        return <Article />
      case 'url':
        return <LinkIcon />
      default:
        return <Description />
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Documents
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Upload and manage your business documents for AI analysis
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => dispatch(fetchDocumentsFailure(''))}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" fontWeight={600} gutterBottom>
            Upload New Document
          </Typography>
          <Box
            sx={{
              border: '2px dashed',
              borderColor: 'divider',
              borderRadius: 2,
              p: 4,
              textAlign: 'center',
              mt: 2,
            }}
          >
            <CloudUpload sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
            <Typography variant="body1" gutterBottom>
              Drag and drop files here or click to browse
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Supported formats: PDF, Excel, Word, Audio, Text (Max: 50MB)
            </Typography>
            <Button
              variant="contained"
              component="label"
              sx={{ mt: 2 }}
              disabled={isUploading}
            >
              Select File
              <input
                type="file"
                hidden
                onChange={handleFileSelect}
                accept=".pdf,.xlsx,.xls,.csv,.docx,.doc,.mp3,.wav,.txt"
              />
            </Button>
            {selectedFile && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" fontWeight={600}>
                  Selected: {selectedFile.name}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {formatFileSize(selectedFile.size)}
                </Typography>
                <Box sx={{ mt: 1 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleUpload}
                    disabled={isUploading}
                  >
                    Upload
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={() => setSelectedFile(null)}
                    sx={{ ml: 1 }}
                    disabled={isUploading}
                  >
                    Cancel
                  </Button>
                </Box>
              </Box>
            )}
            {isUploading && (
              <Box sx={{ mt: 2 }}>
                <LinearProgress variant="determinate" value={uploadProgress} />
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Uploading... {uploadProgress}%
                </Typography>
              </Box>
            )}
          </Box>
        </CardContent>
      </Card>

      <Typography variant="h6" fontWeight={600} gutterBottom>
        Your Documents ({documents.length})
      </Typography>

      <Grid container spacing={3}>
        {documents.length === 0 ? (
          <Grid item xs={12}>
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 6 }}>
                <Description sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                <Typography variant="body1" color="text.secondary">
                  No documents uploaded yet. Upload your first document to get started!
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ) : (
          documents.map((doc) => (
            <Grid item xs={12} sm={6} md={4} key={doc.id}>
              <Card
                sx={{
                  position: 'relative',
                  border: activeDocument?.id === doc.id ? '2px solid' : 'none',
                  borderColor: 'primary.main',
                }}
              >
                {activeDocument?.id === doc.id && (
                  <Chip
                    label="Active"
                    color="primary"
                    size="small"
                    icon={<CheckCircle />}
                    sx={{ position: 'absolute', top: 8, right: 8 }}
                  />
                )}
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box sx={{ color: 'primary.main', mr: 2 }}>
                      {getDocumentIcon(doc.document_type)}
                    </Box>
                    <Box sx={{ flex: 1, minWidth: 0 }}>
                      <Typography variant="h6" noWrap title={doc.file_name}>
                        {doc.file_name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {formatFileSize(doc.file_size || 0)}
                      </Typography>
                    </Box>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Chip
                      label={doc.document_type.toUpperCase()}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Chip
                      label={doc.status?.toUpperCase() || 'PENDING'}
                      size="small"
                      color={doc.status === 'processed' ? 'success' : 'default'}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    {activeDocument?.id !== doc.id && (
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => handleActivate(doc.id)}
                        fullWidth
                        startIcon={<Visibility />}
                      >
                        Activate
                      </Button>
                    )}
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => handleDeleteClick(doc.id, doc.file_name)}
                    >
                      <Delete />
                    </IconButton>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialog.open}
        onClose={() => setDeleteDialog({ open: false, documentId: null, documentName: '' })}
      >
        <DialogTitle>Delete Document</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete <strong>{deleteDialog.documentName}</strong>?
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialog({ open: false, documentId: null, documentName: '' })}>
            Cancel
          </Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
