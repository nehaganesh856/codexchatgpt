import { useNavigate, useLocation } from 'react-router-dom';
import { Code2, Grid, Plus, Settings, LogOut, Home } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { useState } from 'react';

function Sidebar({ onClose }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const isActive = (path) => location.pathname === path;

  const menuItems = [
    { label: 'Home', icon: Home, path: '/' },
    { label: 'Dashboard', icon: Grid, path: '/dashboard' },
    { label: 'Generator', icon: Plus, path: '/generator' },
    { label: 'Settings', icon: Settings, path: '/settings' },
  ];

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await logout();
      navigate('/');
      onClose?.();
    } finally {
      setIsLoggingOut(false);
    }
  };

  return (
    <div className="w-full h-screen bg-slate-800 border-r border-slate-700 flex flex-col p-6">
      {/* Logo */}
      <div className="flex items-center gap-2 mb-8">
        <Code2 className="w-6 h-6 text-blue-500" />
        <span className="text-lg font-bold text-white">AppBuilder</span>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.path}
              onClick={() => {
                navigate(item.path);
                onClose?.();
              }}
              className={`w-full flex items-center gap-3 px-4 py-2 rounded-lg transition ${
                isActive(item.path)
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-300 hover:bg-slate-700'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Logout Button */}
      <button
        onClick={handleLogout}
        disabled={isLoggingOut}
        className="w-full flex items-center gap-3 px-4 py-2 text-slate-300 hover:bg-slate-700 hover:text-white rounded-lg transition disabled:opacity-50"
      >
        <LogOut className="w-5 h-5" />
        <span>{isLoggingOut ? 'Signing out...' : 'Sign Out'}</span>
      </button>
    </div>
  );
}

export default Sidebar;