import { useState } from 'react'
import { Check } from 'lucide-react'
import DashboardLayout from '../components/layout/DashboardLayout'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { LoadingSkeleton, ErrorState } from '../components/ui/States'
import { usePreferences } from '../context/PreferencesContext'

const THEME_OPTIONS = [
  { value: 'light', label: 'Light' },
  { value: 'dark', label: 'Dark' }
]

const RANGE_OPTIONS = [
  { value: 'today', label: 'Today' },
  { value: '7d', label: 'Last 7 Days' },
  { value: '30d', label: 'Last 30 Days' },
  { value: '90d', label: 'Last 90 Days' }
]

const UNIT_OPTIONS = [
  { value: 'celsius', label: 'Celsius (°C)' },
  { value: 'fahrenheit', label: 'Fahrenheit (°F)' }
]

const LANDING_OPTIONS = [
  { value: 'overview', label: 'Overview' },
  { value: 'equipment', label: 'Equipment' },
  { value: 'production', label: 'Production' },
  { value: 'ai-insights', label: 'AI Insights' }
]

function SegmentedControl({ options, value, onChange }) {
  return (
    <div className="inline-flex flex-wrap rounded-lg border border-surface-border bg-surface-bg p-1 gap-1">
      {options.map((opt) => (
        <button
          key={opt.value}
          type="button"
          onClick={() => onChange(opt.value)}
          className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
            value === opt.value
              ? 'bg-white text-primary shadow-card font-medium'
              : 'text-ink-muted hover:text-ink'
          }`}
        >
          {opt.label}
        </button>
      ))}
    </div>
  )
}

function Toggle({ checked, onChange }) {
  return (
    <button
      type="button"
      aria-pressed={checked}
      onClick={() => onChange(!checked)}
      className={`relative h-6 w-11 rounded-full transition-colors ${
        checked ? 'bg-primary' : 'bg-slate-200'
      }`}
    >
      <span
        className={`absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform ${
          checked ? 'translate-x-[22px]' : 'translate-x-0.5'
        }`}
      />
    </button>
  )
}

function Row({ label, description, children }) {
  return (
    <div className="flex items-center justify-between gap-6 py-4 border-b border-surface-border last:border-0">
      <div>
        <p className="text-sm font-medium text-ink">
          {label}
        </p>

        {description && (
          <p className="text-xs text-ink-muted mt-0.5">
            {description}
          </p>
        )}
      </div>

      {children}
    </div>
  )
}

export default function Preferences() {
  const {
    preferences,
    loading,
    updatePreference,
    savePreferences,
  } = usePreferences()

  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState(null)

  function update(key, value) {
    updatePreference(key, value)
    setSaved(false)
    setError(null)
  }

  async function handleSave() {
    setSaving(true)
    setSaved(false)
    setError(null)

    try {
      await savePreferences()
      setSaved(true)
    } catch (err) {
      console.error(err)
      setError(err)
    } finally {
      setSaving(false)
    }
  }

  return (
    <DashboardLayout
      title="Preferences"
      breadcrumb="Manufacturing / Preferences"
    >
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-ink">
          Preferences
        </h2>

        <p className="text-sm text-ink-muted mt-1">
          Personalize how the dashboard looks and behaves for your account.
        </p>
      </div>

      <Card className="max-w-2xl">
        {loading && <LoadingSkeleton rows={4} />}

        {!loading && error && (
          <ErrorState
            onRetry={() => window.location.reload()}
          />
        )}

        {!loading && preferences && (
          <>
            {/* Theme */}
            <Row
              label="Theme"
              description="Choose a light or dark interface."
            >
              <SegmentedControl
                options={THEME_OPTIONS}
                value={preferences.theme}
                onChange={(value) => update('theme', value)}
              />
            </Row>

            {/* Default Date Range */}
            <Row
              label="Default date range"
              description="Applied to the Overview dashboard on load."
            >
              <SegmentedControl
                options={RANGE_OPTIONS}
                value={preferences.defaultDateRange}
                onChange={(value) =>
                  update('defaultDateRange', value)
                }
              />
            </Row>

            {/* Temperature Unit */}
            <Row
              label="Temperature unit"
              description="Used across equipment temperature readings."
            >
              <SegmentedControl
                options={UNIT_OPTIONS}
                value={preferences.temperatureUnit}
                onChange={(value) =>
                  update('temperatureUnit', value)
                }
              />
            </Row>

            {/* Default Landing Page */}
            <Row
              label="Default landing page"
              description="The page you see right after signing in."
            >
              <select
                value={preferences.defaultLandingPage}
                onChange={(e) =>
                  update(
                    'defaultLandingPage',
                    e.target.value
                  )
                }
                className="h-9 rounded-lg border border-surface-border bg-white px-3 text-sm outline-none focus:border-primary"
              >
                {LANDING_OPTIONS.map((option) => (
                  <option
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </option>
                ))}
              </select>
            </Row>

            {/* Email Notifications */}
            <Row
              label="Email notifications"
              description="Receive email alerts for critical equipment and quality events."
            >
              <Toggle
                checked={preferences.emailNotifications}
                onChange={(value) =>
                  update('emailNotifications', value)
                }
              />
            </Row>

            {/* Save */}
            <div className="flex items-center gap-3 pt-5">
              <Button
                onClick={handleSave}
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save preferences'}
              </Button>

              {saved && (
                <span className="flex items-center gap-1.5 text-sm text-status-success">
                  <Check size={15} />
                  Saved
                </span>
              )}
            </div>
          </>
        )}
      </Card>
    </DashboardLayout>
  )
}