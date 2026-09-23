import { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { preferencesService } from '../services/preferencesService'

const PreferencesContext = createContext(null)

const DEFAULT_PREFERENCES = {
  theme: 'light',
  defaultDateRange: '7d',
  temperatureUnit: 'celsius',
  defaultLandingPage: 'overview',
  emailNotifications: true,
}

export function PreferencesProvider({ children }) {
  const [preferences, setPreferences] = useState(DEFAULT_PREFERENCES)
  const [loading, setLoading] = useState(true)

  // Load saved preferences when the app starts
  useEffect(() => {
    async function loadPreferences() {
      try {
        const saved = await preferencesService.get()

        const loadedPreferences = {
          ...DEFAULT_PREFERENCES,
          ...saved,
        }

        setPreferences(loadedPreferences)
      } catch (error) {
        console.error('Failed to load preferences:', error)
      } finally {
        setLoading(false)
      }
    }

    loadPreferences()
  }, [])

  // Apply theme to the whole website
  useEffect(() => {
    const root = document.documentElement

    if (preferences.theme === 'dark') {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  }, [preferences.theme])

  // Change one preference locally
  const updatePreference = useCallback((key, value) => {
    setPreferences((current) => ({
      ...current,
      [key]: value,
    }))
  }, [])

  // Save all preferences to backend
  const savePreferences = useCallback(async (newPreferences = preferences) => {
    const saved = await preferencesService.update(newPreferences)

    const updatedPreferences = {
      ...DEFAULT_PREFERENCES,
      ...saved,
    }

    setPreferences(updatedPreferences)

    return updatedPreferences
  }, [preferences])

  return (
    <PreferencesContext.Provider
      value={{
        preferences,
        loading,
        updatePreference,
        savePreferences,
      }}
    >
      {children}
    </PreferencesContext.Provider>
  )
}

export function usePreferences() {
  const context = useContext(PreferencesContext)

  if (!context) {
    throw new Error(
      'usePreferences must be used within a PreferencesProvider'
    )
  }

  return context
}