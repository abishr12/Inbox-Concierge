export default function LoginScreen(): React.ReactElement {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Email Concierge</h1>
        <p className="text-gray-600 mb-8">Sign in to categorize your emails</p>
        <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Sign in with Google
        </button>
      </div>
    </div>
  )
}
