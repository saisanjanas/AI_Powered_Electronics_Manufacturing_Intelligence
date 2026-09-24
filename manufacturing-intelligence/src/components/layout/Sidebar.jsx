import { NavLink, useNavigate } from 'react-router-dom'
import {
  LayoutGrid,
  Cpu,
  Factory,
  ShieldCheck,
  Wrench,
  Sparkles,
  BarChart3,
  Settings,
  HelpCircle,
  ChevronsLeft,
  ChevronsRight,
  Activity,
  LogOut
} from 'lucide-react'
import clsx from 'clsx'
import { useAuth } from '../../context/AuthContext'

const PRIMARY_NAV = [
  { to: '/', label: 'Overview', icon: LayoutGrid, end: true },
  { to: '/equipment', label: 'Equipment', icon: Cpu },
  { to: '/production', label: 'Production', icon: Factory },
  { to: '/quality', label: 'Quality', icon: ShieldCheck },
  { to: '/maintenance', label: 'Maintenance', icon: Wrench },
  { to: '/ai-insights', label: 'AI Insights', icon: Sparkles }
]

const ANALYTICS_NAV = [
  { to: '/analytics/production', label: 'Production Analytics', icon: BarChart3 },
  { to: '/analytics/equipment', label: 'Equipment Analytics', icon: BarChart3 },
  { to: '/analytics/quality', label: 'Quality Analytics', icon: BarChart3 },
  { to: '/analytics/downtime', label: 'Downtime Analytics', icon: BarChart3 }
]

function NavItem({ item, collapsed }) {
  return (
    <NavLink
      to={item.to}
      end={item.end}
      className={({ isActive }) =>
        clsx(
          'group relative flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors duration-150',
          isActive
            ? 'bg-primary text-white shadow-sm'
            : 'text-slate-300 hover:bg-white/10 hover:text-white'
        )
      }
    >
      <item.icon
        size={17}
        strokeWidth={2}
        className="shrink-0"
      />

      {!collapsed && (
        <span className="truncate">
          {item.label}
        </span>
      )}

      {collapsed && (
        <span
          className="
            pointer-events-none
            absolute left-full ml-2
            whitespace-nowrap
            rounded-md
            bg-navy-secondary
            px-2 py-1
            text-xs text-white
            opacity-0
            shadow-raised
            transition-opacity duration-150
            group-hover:opacity-100
            z-30
          "
        >
          {item.label}
        </span>
      )}
    </NavLink>
  )
}

export default function Sidebar({ collapsed, onToggle }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login', { replace: true })
  }

  const initials = user?.name
    ? user.name
        .split(' ')
        .map((p) => p[0])
        .slice(0, 2)
        .join('')
        .toUpperCase()
    : '—'

  return (
    <aside
      className={clsx(
        `
          sticky top-0 h-screen shrink-0
          bg-navy text-white
          flex flex-col
          border-r border-white/5
          transition-all duration-200
        `,
        collapsed ? 'w-[72px]' : 'w-64'
      )}
    >
      {/* Logo */}
      <div
        className={clsx(
          'flex items-center gap-2.5 px-4 h-16 border-b border-white/10',
          collapsed && 'justify-center px-0'
        )}
      >
       <div className="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden">
      <img
            src="/logo.png"
            alt="Manufacturing Intelligence"
            className="h-10 w-10 object-contain"
      />
      </div>

        {!collapsed && (
          <span className="text-sm font-semibold tracking-tight truncate">
            Manufacturing Intelligence
          </span>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto scrollbar-thin px-3 py-4 space-y-6">

        {/* Main navigation */}
        <div className="space-y-1">
          {PRIMARY_NAV.map((item) => (
            <NavItem
              key={item.to}
              item={item}
              collapsed={collapsed}
            />
          ))}
        </div>

        {/* Analytics */}
        <div>
          {!collapsed && (
            <p
              className="
                px-3 mb-2
                text-[11px]
                font-semibold
                text-slate-400
                tracking-wide
                uppercase
              "
            >
              Analytics
            </p>
          )}

          <div className="space-y-1">
            {ANALYTICS_NAV.map((item) => (
              <NavItem
                key={item.to}
                item={item}
                collapsed={collapsed}
              />
            ))}
          </div>
        </div>
      </nav>

      {/* Bottom section */}
      <div className="border-t border-white/10 px-3 py-4 space-y-1">

        {/* Preferences */}
        <NavItem
          item={{
            to: '/preferences',
            label: 'Preferences',
            icon: Settings
          }}
          collapsed={collapsed}
        />

        {/* Help */}
        <NavItem
          item={{
            to: '/help',
            label: 'Help',
            icon: HelpCircle
          }}
          collapsed={collapsed}
        />

        {/* User */}
        <div
          className={clsx(
            `
              flex items-center gap-2.5
              px-3 pt-3 mt-2
              border-t border-white/10
            `,
            collapsed && 'justify-center px-0'
          )}
        >
          <div
            className="
              h-7 w-7 shrink-0
              rounded-full
              bg-primary-light
              flex items-center justify-center
              text-[11px]
              font-semibold
              text-primary-dark
            "
          >
            {initials}
          </div>

          {!collapsed && (
            <div className="min-w-0 flex-1">
              <p className="text-xs font-medium text-white truncate">
                {user?.name || 'Guest'}
              </p>

              <p className="text-[11px] text-slate-400 truncate capitalize">
                {user?.role || ''}
              </p>
            </div>
          )}

          {!collapsed && (
            <button
              type="button"
              onClick={handleLogout}
              title="Sign out"
              className="
                text-slate-400
                hover:text-white
                transition-colors
              "
            >
              <LogOut size={15} />
            </button>
          )}
        </div>

        {/* Collapse */}
        <button
          type="button"
          onClick={onToggle}
          className={clsx(
            `
              mt-3
              flex w-full items-center gap-2
              rounded-lg
              px-3 py-2
              text-xs font-medium
              text-slate-400
              hover:bg-white/10
              hover:text-white
              transition-colors
            `,
            collapsed && 'justify-center px-0'
          )}
        >
          {collapsed ? (
            <ChevronsRight size={16} />
          ) : (
            <ChevronsLeft size={16} />
          )}

          {!collapsed && (
            <span>
              Collapse
            </span>
          )}
        </button>
      </div>
    </aside>
  )
}