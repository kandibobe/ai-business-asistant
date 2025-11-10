import ErrorPage from '@/components/error/ErrorPage'

export default function ServerErrorPage() {
  return (
    <ErrorPage
      statusCode={500}
      title="Server Error"
      message="We're experiencing technical difficulties. Our team has been notified and is working to fix the issue. Please try again in a few moments."
      showBackButton={false}
      showHomeButton={true}
      showRefreshButton={true}
    />
  )
}
