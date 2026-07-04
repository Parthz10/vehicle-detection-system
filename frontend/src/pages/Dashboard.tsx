import { useEffect, useMemo, useState } from 'react';
import { Car, LogOut, RadioTower, Siren, Smartphone } from 'lucide-react';
import { QRCodeSVG } from 'qrcode.react';
import { api, API_BASE } from '../api/client';
import { AlertPanel } from '../components/AlertPanel';
import { Filters } from '../components/Filters';
import { RecentDetections } from '../components/RecentDetections';
import { StatCard } from '../components/StatCard';
import { useAuth } from '../contexts/AuthContext';
import { Alert, Camera, Detection, StatsSummary } from '../types';

export function Dashboard() {
  const { fullName, logout } = useAuth();
  const [detections, setDetections] = useState<Detection[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [stats, setStats] = useState<StatsSummary | null>(null);
  const [plate, setPlate] = useState('');
  const [vehicleType, setVehicleType] = useState('');
  const [date, setDate] = useState('');
  const [selectedCamera, setSelectedCamera] = useState<number | null>(null);

  const phoneUrl = `${window.location.origin}/phone-camera`;

  async function load() {
    const params: Record<string, string> = {};
    if (plate) params.plate_number = plate;
    if (vehicleType) params.vehicle_type = vehicleType;
    if (date) {
      params.start_date = `${date}T00:00:00`;
      params.end_date = `${date}T23:59:59`;
    }
    const [detectionRes, statsRes, alertsRes, camerasRes] = await Promise.all([
      api.get('/detections', { params }),
      api.get('/detections/stats'),
      api.get('/alerts'),
      api.get('/cameras'),
    ]);
    setDetections(detectionRes.data);
    setStats(statsRes.data);
    setAlerts(alertsRes.data);
    setCameras(camerasRes.data);
    if (!selectedCamera && camerasRes.data[0]) setSelectedCamera(camerasRes.data[0].id);
  }

  useEffect(() => {
    load();
    const timer = window.setInterval(load, 7000);
    return () => window.clearInterval(timer);
  }, [plate, vehicleType, date]);

  useEffect(() => {
    if (!alerts.some((alert) => !alert.acknowledged)) return;
    const audio = new AudioContext();
    const oscillator = audio.createOscillator();
    const gain = audio.createGain();
    oscillator.frequency.value = 880;
    gain.gain.value = 0.08;
    oscillator.connect(gain);
    gain.connect(audio.destination);
    oscillator.start();
    window.setTimeout(() => {
      oscillator.stop();
      audio.close();
    }, 220);
  }, [alerts]);

  const streamUrl = useMemo(() => (selectedCamera ? `${API_BASE}/api/streams/${selectedCamera}/mjpeg` : null), [selectedCamera]);

  return (
    <main className="min-h-screen">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
          <div>
            <h1 className="text-xl font-semibold text-gray-950">AI Vehicle Detection & ANPR</h1>
            <p className="text-sm text-gray-500">{fullName}</p>
          </div>
          <button onClick={logout} className="inline-flex items-center gap-2 rounded-md border border-gray-300 px-3 py-2 text-sm hover:bg-gray-50">
            <LogOut size={16} /> Logout
          </button>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-5 px-4 py-5">
        <div className="grid gap-4 md:grid-cols-3">
          <StatCard label="Total detections" value={stats?.total_detections ?? 0} icon={<Car size={22} />} />
          <StatCard label="Today" value={stats?.today ?? 0} icon={<RadioTower size={22} />} />
          <StatCard label="Blacklist hits" value={stats?.blacklisted_hits ?? 0} icon={<Siren size={22} />} />
        </div>

        <div className="grid gap-5 lg:grid-cols-[1fr_360px]">
          <section className="rounded-lg border border-gray-200 bg-white shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-gray-200 px-4 py-3">
              <h2 className="font-semibold text-gray-950">Live camera feed</h2>
              <select className="rounded-md border border-gray-300 px-3 py-2 text-sm" value={selectedCamera ?? ''} onChange={(e) => setSelectedCamera(Number(e.target.value))}>
                {cameras.map((camera) => <option key={camera.id} value={camera.id}>{camera.name}</option>)}
              </select>
            </div>
            <div className="aspect-video bg-gray-950">
              {streamUrl ? <img src={streamUrl} className="h-full w-full object-contain" /> : <div className="grid h-full place-items-center text-gray-400">No camera configured</div>}
            </div>
          </section>

          <div className="grid gap-5">
            <AlertPanel alerts={alerts} />
            <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
              <div className="mb-3 flex items-center gap-2">
                <Smartphone size={18} className="text-patrol" />
                <h2 className="font-semibold text-gray-950">Phone camera</h2>
              </div>
              <div className="grid place-items-center rounded-md bg-gray-50 p-4">
                <QRCodeSVG value={phoneUrl} size={160} />
              </div>
            </div>
          </div>
        </div>

        <Filters plate={plate} setPlate={setPlate} vehicleType={vehicleType} setVehicleType={setVehicleType} date={date} setDate={setDate} />
        <RecentDetections detections={detections} />
      </div>
    </main>
  );
}
