import { ReactNode } from 'react';

export function StatCard({ label, value, icon }: { label: string; value: ReactNode; icon: ReactNode }) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className="mt-1 text-2xl font-semibold text-gray-950">{value}</p>
        </div>
        <div className="grid h-10 w-10 place-items-center rounded-md bg-teal-50 text-patrol">{icon}</div>
      </div>
    </div>
  );
}
