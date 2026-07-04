import { createContext, ReactNode, useContext, useMemo, useState } from 'react';
import { api } from '../api/client';
import { Role } from '../types';

interface AuthState {
  token: string | null;
  role: Role | null;
  fullName: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'));
  const [role, setRole] = useState<Role | null>((localStorage.getItem('role') as Role | null) ?? null);
  const [fullName, setFullName] = useState<string | null>(localStorage.getItem('full_name'));

  async function login(email: string, password: string) {
    const form = new URLSearchParams();
    form.append('username', email);
    form.append('password', password);
    const { data } = await api.post('/auth/login', form);
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('role', data.role);
    localStorage.setItem('full_name', data.full_name);
    setToken(data.access_token);
    setRole(data.role);
    setFullName(data.full_name);
  }

  function logout() {
    localStorage.clear();
    setToken(null);
    setRole(null);
    setFullName(null);
  }

  const value = useMemo(() => ({ token, role, fullName, login, logout }), [token, role, fullName]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error('useAuth must be used inside AuthProvider');
  return value;
}
