import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest): Promise<NextResponse> {
  const searchParams = request.nextUrl.searchParams
  const code = searchParams.get('code')

  if (!code) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  try {
    // Call the server's callback endpoint with the OAuth code
    const response = await fetch(`http://localhost:8000/auth/callback?code=${code}`)
    
    if (!response.ok) {
      throw new Error('Failed to authenticate')
    }

    // Redirect to emails page on success
    return NextResponse.redirect(new URL('/emails', request.url))
  } catch (error) {
    console.error('OAuth callback error:', error)
    return NextResponse.redirect(new URL('/', request.url))
  }
}
