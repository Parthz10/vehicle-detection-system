import { Dashboard } from './pages/Dashboard';
import { Login } from './components/Login';
import { PhoneCamera } from './pages/PhoneCamera';
import { useAuth } from './contexts/AuthContext';

export function App() {
  const { token } = useAuth();
  if (window.location.pathname === '/phone-camera') return <PhoneCamera />;
  return token ? <Dashboard /> : <Login />;
}
