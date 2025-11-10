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
  const { documents, isUploading, uploadProgress, activeDocument } = useSelector(
    (state: RootState) => state.documents
  )
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

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
      setSelectedFile(event.target.files[0])
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

  const handleDelete = async (documentId: number) => {
    if (!confirm('Are you sure you want to delete this document?')) {
      return
    }

    try {
      await documentsApi.delete(documentId)
      dispatch(deleteDocumentAction(documentId))
      dispatch(
        showSnackbar({
          message: 'Document deleted',
          severity: 'success',
        })
      )
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
              Supported formats: PDF, Excel, Word, Audio, URLs
            </Typography>
            <Button
              variant="contained"
              component="label"
              sx={{ mt: 2 }}
              disabled={isUploading}
            >
              Select File
              <input type="file" hidden onChange={handleFileSelect} />
            </Button>
            {selectedFile && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2">
                  Selected: {selectedFile.name}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleUpload}
                  sx={{ mt: 1 }}
                  disabled={isUploading}
                >
                  Upload
                </Button>
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
                  border: activeDocument?.id === doc.id ? 2 : 0,
                  borderColor: 'success.main',
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box sx={{ color: 'primary.main', mr: 2 }}>
                      {getDocumentIcon(doc.document_type)}
                    </Box>
                    <Typography variant="h6" sx={{ flex: 1 }} noWrap>
                      {doc.file_name}
                    </Typography>
                    {activeDocument?.id === doc.id && (
                      <CheckCircle color="success" fontSize="small" />
                    )}
                  </Box>
                  <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
                    <Chip
                      label={doc.document_type.toUpperCase()}
                      size="small"
                    />
                    {activeDocument?.id === doc.id && (
                      <Chip
                        label="ACTIVE"
                        size="small"
                        color="success"
                      />
                    )}
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => handleActivate(doc.id)}
                      disabled={activeDocument?.id === doc.id}
                      title="Set as active for chat"
                    >
                      <Visibility />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => handleDelete(doc.id)}
                      title="Delete document"
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
    </Box>
  )
}
