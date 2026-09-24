import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Mail, Lock, AlertCircle } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import Button from '../components/ui/Button'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      await login(email, password)

      const redirectTo = location.state?.from?.pathname || '/'

      navigate(redirectTo, { replace: true })
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface-bg px-4">
      <div className="w-full max-w-sm">

        {/* Logo and title */}
        <div className="flex flex-col items-center mb-8">

          <div className="flex items-center justify-center mb-3">
          <img
              src="/logo.png"
              alt="Manufacturing Intelligence"
              className="h-20 w-20 object-contain"
          />
          </div>

          <h1 className="text-lg font-semibold text-ink">
            Manufacturing Intelligence
          </h1>

          <p className="text-sm text-ink-muted mt-1">
            Sign in to your account
          </p>
        </div>

        {/* Login form */}
        <form
          onSubmit={handleSubmit}
          className="bg-surface-card border border-surface-border rounded-card shadow-card p-6 space-y-4"
        >

          {/* Error message */}
          {error && (
            <div className="flex items-start gap-2 rounded-lg bg-status-criticalBg text-status-critical text-sm px-3 py-2.5">
              <AlertCircle size={16} className="shrink-0 mt-0.5" />
              {error}
            </div>
          )}

          {/* Email */}
          <div>
            <label className="block text-xs font-medium text-ink-muted mb-1.5">
              Email
            </label>

            <div className="flex items-center gap-2 h-10 rounded-lg border border-surface-border px-3 focus-within:border-primary transition-colors">
              <Mail size={15} className="text-ink-muted" />

              <input
                type="email"
                required
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                className="flex-1 bg-transparent outline-none text-sm placeholder:text-ink-muted"
              />
            </div>
          </div>

          {/* Password */}
          <div>
            <label className="block text-xs font-medium text-ink-muted mb-1.5">
              Password
            </label>

            <div className="flex items-center gap-2 h-10 rounded-lg border border-surface-border px-3 focus-within:border-primary transition-colors">
              <Lock size={15} className="text-ink-muted" />

              <input
                type="password"
                required
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="flex-1 bg-transparent outline-none text-sm placeholder:text-ink-muted"
              />
            </div>
          </div>

          {/* Sign in button */}
          <Button
            type="submit"
            className="w-full"
            disabled={submitting}
          >
            {submitting ? 'Signing in...' : 'Sign in'}
          </Button>

        </form>

        {/* Register link */}
        <p className="text-center text-sm text-ink-muted mt-5">
          Don't have an account?{' '}

          <Link
            to="/register"
            className="text-primary font-medium hover:underline"
          >
            Create one
          </Link>
        </p>

      </div>
    </div>
  )
}