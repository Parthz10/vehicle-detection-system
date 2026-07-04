import { BellRing } from 'lucide-react';
import { Alert } from '../types';

export function AlertPanel({ alerts }: { alerts: Alert[] }) {
  const active = alerts.filter((alert) => !alert.acknowledged);
  return (
    <div className={`rounded-lg border p-4 shadow-sm ${active.length ? 'border-red-300 bg-red-50' : 'border-gray-200 bg-white'}`}>
      <div className="mb-3 flex items-center gap-2">
        <BellRing size={18} className={active.length ? 'text-red-700' : 'text-gray-500'} />
        <h2 className="font-semibold text-gray-950">Blacklist alerts</h2>
      </div>
      <div className="space-y-2">
        {alerts.slice(0, 5).map((alert) => (
          <div key={alert.id} className="rounded-md bg-white px-3 py-2 text-sm text-gray-700">
            <span className="font-semibold text-red-700">{alert.plate_number}</span> {alert.message}
          </div>
        ))}
        {!alerts.length && <p className="text-sm text-gray-500">No alerts recorded.</p>}
      </div>
    </div>
  );
}
