import { FormEvent, useState } from 'react';
import { ShieldCheck } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export function Login() {
  const { login } = useAuth();
  const [email, setEmail] = useState('admin@example.com');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError('');
    try {
      await login(email, password);
    } catch {
      setError('Invalid email or password');
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-gray-100 px-4">
      <form onSubmit={submit} className="w-full max-w-sm rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <div className="mb-6 flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-md bg-ink text-white">
            <ShieldCheck size={24} />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-gray-950">ANPR Control</h1>
            <p className="text-sm text-gray-500">Secure dashboard access</p>
          </div>
        </div>
        <label className="mb-4 block">
          <span className="mb-1 block text-sm font-medium text-gray-700">Email</span>
          <input className="w-full rounded-md border border-gray-300 px-3 py-2 outline-none focus:border-patrol" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label className="mb-4 block">
          <span className="mb-1 block text-sm font-medium text-gray-700">Password</span>
          <input className="w-full rounded-md border border-gray-300 px-3 py-2 outline-none focus:border-patrol" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        {error && <p className="mb-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
        <button className="w-full rounded-md bg-ink px-4 py-2 font-medium text-white hover:bg-gray-800">Login</button>
      </form>
    </main>
  );
}
