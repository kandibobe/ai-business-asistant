import ErrorPage from '@/components/error/ErrorPage'

export default function NotFoundPage() {
  return (
    <ErrorPage
      statusCode={404}
      title="Page Not Found"
      message="The page you're looking for doesn't exist or has been moved. Please check the URL or go back to the homepage."
      showBackButton={true}
      showHomeButton={true}
      showRefreshButton={false}
    />
  )
}
