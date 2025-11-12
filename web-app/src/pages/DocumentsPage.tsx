import { useState, useEffect, useMemo } from 'react'
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  IconButton,
  Chip,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Fade,
} from '@mui/material'
import {
  Description,
  PictureAsPdf,
  TableChart,
  Article,
  Link as LinkIcon,
  Delete,
  Visibility,
  CheckCircle,
  Search,
  FilterList,
  MoreVert,
  Download,
  Info,
  Close,
} from '@mui/icons-material'
import { useDropzone } from 'react-dropzone'
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
import { gradients } from '@/theme'

export default function DocumentsPage() {
  const dispatch = useDispatch()
  const toast = useToast()
  const { documents, activeDocument, error } = useSelector(
    (state: RootState) => state.documents
  )
  const [deleteDialog, setDeleteDialog] = useState<{
    open: boolean
    documentId: number | null
    documentName: string
  }>({
    open: false,
    documentId: null,
    documentName: '',
  })
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [selectedDoc, setSelectedDoc] = useState<number | null>(null)

  // Load documents on mount
  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      dispatch(fetchDocumentsStart())
      const response = await documentsApi.list()
      dispatch(fetchDocumentsSuccess(response.documents))

      if (response.active_document_id) {
        const activeDoc = response.documents.find(
          (doc: any) => doc.id === response.active_document_id
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
    if (selectedFiles.length === 0) return

    try {
      dispatch(uploadStart())

      for (const file of selectedFiles) {
        const document = await documentsApi.upload(file, (progress) => {
          dispatch(setUploadProgress(progress))
        })
        dispatch(uploadSuccess(document))
      }

      dispatch(
        showSnackbar({
          message: `${selectedFiles.length} document(s) uploaded successfully!`,
          severity: 'success',
        })
      )
      setSelectedFiles([])
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
      const doc = documents.find((d: any) => d.id === documentId)
      if (doc) {
        dispatch(setActiveDocument(doc))
        dispatch(
          showSnackbar({
            message: 'Document activated',
            severity: 'success',
          })
        )
      }
      handleMenuClose()
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

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, docId: number) => {
    setAnchorEl(event.currentTarget)
    setSelectedDoc(docId)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
    setSelectedDoc(null)
  }

  const getDocumentIcon = (type: string) => {
    switch (type) {
      case 'pdf':
        return <PictureAsPdf fontSize="large" />
      case 'excel':
        return <TableChart fontSize="large" />
      case 'word':
        return <Article fontSize="large" />
      case 'url':
        return <LinkIcon fontSize="large" />
      default:
        return <Description fontSize="large" />
    }
  }

  const getDocumentColor = (type: string) => {
    switch (type) {
      case 'pdf':
        return gradients.error
      case 'excel':
        return gradients.success
      case 'word':
        return gradients.info
      default:
        return gradients.primary
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  // Filter and search documents
  const filteredDocuments = useMemo(() => {
    return documents.filter((doc: any) => {
      const matchesSearch = doc.file_name.toLowerCase().includes(searchQuery.toLowerCase())
      const matchesFilter = filterType === 'all' || doc.document_type === filterType
      return matchesSearch && matchesFilter
    })
  }, [documents, searchQuery, filterType])

  const documentTypes = useMemo(() => {
    const types = new Set(documents.map((doc: any) => doc.document_type))
    return Array.from(types)
  }, [documents])

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Documents
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Upload and manage your business documents for AI analysis
        </Typography>
      </Box>

      {error && (
        <Alert
          severity="error"
          sx={{ mb: 3 }}
          onClose={() => dispatch(fetchDocumentsFailure(''))}
        >
          {error}
        </Alert>
      )}

      {/* Upload Area */}
      <Card
        sx={{
          mb: 4,
          background: gradients.primary,
          color: '#fff',
        }}
      >
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h6" fontWeight={600} gutterBottom sx={{ color: '#fff' }}>
            Upload Documents
          </Typography>

          <Box
            {...getRootProps()}
            sx={{
              border: '3px dashed',
              borderColor: alpha('#fff', 0.5),
              borderRadius: 3,
              p: 6,
              textAlign: 'center',
              mt: 2,
              bgcolor: alpha('#fff', isDragActive ? 0.2 : 0.1),
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              '&:hover': {
                bgcolor: alpha('#fff', 0.15),
                borderColor: alpha('#fff', 0.8),
              },
            }}
          >
            <input {...getInputProps()} />
            <CloudUpload sx={{ fontSize: 80, color: '#fff', mb: 2, opacity: 0.9 }} />
            <Typography variant="h6" gutterBottom sx={{ color: '#fff' }}>
              {isDragActive ? 'Drop files here' : 'Drag & drop files here'}
            </Typography>
            <Typography variant="body2" sx={{ color: alpha('#fff', 0.8), mb: 2 }}>
              or click to browse files
            </Typography>
            <Chip
              label="PDF • Excel • Word • Audio • Text"
              sx={{
                bgcolor: alpha('#fff', 0.2),
                color: '#fff',
                fontWeight: 500,
              }}
            />
            <Typography variant="caption" display="block" sx={{ color: alpha('#fff', 0.7), mt: 1 }}>
              Maximum file size: 50MB
            </Typography>
          </Box>

          {fileRejections.length > 0 && (
            <Alert severity="error" sx={{ mt: 2 }}>
              Some files were rejected. Please check file types and sizes.
            </Alert>
          )}

          {selectedFiles.length > 0 && (
            <Fade in>
              <Box sx={{ mt: 3 }}>
                <Stack spacing={1}>
                  {selectedFiles.map((file, index) => (
                    <Paper
                      key={index}
                      sx={{
                        p: 2,
                        display: 'flex',
                        alignItems: 'center',
                        bgcolor: alpha('#fff', 0.9),
                      }}
                    >
                      <Description sx={{ mr: 2, color: 'primary.main' }} />
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="body2" fontWeight={600}>
                          {file.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {formatFileSize(file.size)}
                        </Typography>
                      </Box>
                      <IconButton
                        size="small"
                        onClick={() => setSelectedFiles(selectedFiles.filter((_, i) => i !== index))}
                      >
                        <Close />
                      </IconButton>
                    </Paper>
                  ))}
                </Stack>

                <Stack direction="row" spacing={2} mt={2}>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={handleUpload}
                    disabled={isUploading}
                    sx={{
                      bgcolor: '#fff',
                      color: 'primary.main',
                      '&:hover': {
                        bgcolor: alpha('#fff', 0.9),
                      },
                    }}
                  >
                    Upload {selectedFiles.length} File(s)
                  </Button>
                  <Button
                    variant="outlined"
                    size="large"
                    onClick={() => setSelectedFiles([])}
                    disabled={isUploading}
                    sx={{
                      borderColor: '#fff',
                      color: '#fff',
                      '&:hover': {
                        borderColor: '#fff',
                        bgcolor: alpha('#fff', 0.1),
                      },
                    }}
                  >
                    Clear
                  </Button>
                </Stack>
              </Box>
            </Fade>
          )}

          {isUploading && (
            <Box sx={{ mt: 3 }}>
              <LinearProgress
                variant="determinate"
                value={uploadProgress}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  bgcolor: alpha('#fff', 0.2),
                  '& .MuiLinearProgress-bar': {
                    bgcolor: '#fff',
                  },
                }}
              />
              <Typography variant="body2" sx={{ mt: 1, color: '#fff', textAlign: 'center' }}>
                Uploading... {uploadProgress}%
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Search and Filter */}
      <Stack
        direction={{ xs: 'column', sm: 'row' }}
        spacing={2}
        sx={{ mb: 3 }}
      >
        <TextField
          fullWidth
          placeholder="Search documents..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
        <TextField
          select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          sx={{ minWidth: 200 }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <FilterList />
              </InputAdornment>
            ),
          }}
        >
          <MenuItem value="all">All Types</MenuItem>
          {documentTypes.map((type) => (
            <MenuItem key={type} value={type}>
              {type.toUpperCase()}
            </MenuItem>
          ))}
        </TextField>
      </Stack>

      {/* Documents Header */}
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        sx={{ mb: 2 }}
      >
        <Typography variant="h6" fontWeight={600}>
          Your Documents ({filteredDocuments.length})
        </Typography>
        {activeDocument && (
          <Chip
            icon={<CheckCircle />}
            label={`Active: ${activeDocument.file_name}`}
            color="success"
            variant="outlined"
          />
        )}
      </Stack>

      {/* Documents Grid */}
      <Grid container spacing={3}>
        {filteredDocuments.length === 0 ? (
          <Grid item xs={12}>
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 8 }}>
                <Description sx={{ fontSize: 80, color: 'text.secondary', mb: 2, opacity: 0.5 }} />
                <Typography variant="h6" gutterBottom>
                  {searchQuery || filterType !== 'all' ? 'No documents found' : 'No documents uploaded yet'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {searchQuery || filterType !== 'all'
                    ? 'Try adjusting your search or filter'
                    : 'Upload your first document to get started with AI analysis'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ) : (
          filteredDocuments.map((doc: any) => (
            <Grid item xs={12} sm={6} md={4} key={doc.id}>
              <Fade in={true} timeout={1200 + index * 100}>
                <Card
                  sx={{
                    position: 'relative',
                    border: activeDocument?.id === doc.id ? '2px solid' : 'none',
                    borderColor: 'primary.main',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 6,
                    },
                  }}
                >
                  {activeDocument?.id === doc.id && (
                    <Chip
                      label="Active"
                      color="primary"
                      size="small"
                      icon={<CheckCircle />}
                      sx={{ position: 'absolute', top: 8, right: 8, zIndex: 1 }}
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
                          sx={{
                            transition: 'all 0.2s ease',
                            '&:hover': {
                              transform: 'scale(1.05)',
                            },
                          }}
                        >
                          Activate
                        </Button>
                      )}
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleDeleteClick(doc.id, doc.file_name)}
                        sx={{
                          transition: 'all 0.2s ease',
                          '&:hover': {
                            transform: 'scale(1.1)',
                          },
                        }}
                      >
                        <Delete />
                      </IconButton>
                    </Box>
                  </CardContent>
                </Card>
              </Fade>
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
