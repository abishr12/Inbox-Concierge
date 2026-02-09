export default function LoginScreen(): React.ReactElement {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center max-w-2xl px-6">
        <h1 className="text-6xl font-light text-gray-900 mb-8 tracking-tight">
          AI-powered email categorization
        </h1>
        <p className="text-xl text-gray-600 mb-6 font-light leading-relaxed">
          Streamline your inbox with intelligent automation
        </p>
        <p className="text-xl text-gray-600 mb-12 font-light leading-relaxed">
          for every email thread, categorized instantly.
        </p>
        <button className="px-12 py-4 bg-gray-800 text-white text-lg rounded-full hover:bg-gray-700 transition-colors font-medium">
          Sign in with Google
        </button>
      </div>
    </div>
  )
}
