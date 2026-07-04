import { Search } from 'lucide-react';

interface Props {
  plate: string;
  setPlate: (value: string) => void;
  vehicleType: string;
  setVehicleType: (value: string) => void;
  date: string;
  setDate: (value: string) => void;
}

export function Filters({ plate, setPlate, vehicleType, setVehicleType, date, setDate }: Props) {
  return (
    <div className="grid gap-3 rounded-lg border border-gray-200 bg-white p-4 shadow-sm md:grid-cols-[1fr_180px_180px]">
      <label className="relative">
        <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
        <input className="w-full rounded-md border border-gray-300 py-2 pl-10 pr-3 outline-none focus:border-patrol" placeholder="Search plate number" value={plate} onChange={(e) => setPlate(e.target.value)} />
      </label>
      <select className="rounded-md border border-gray-300 px-3 py-2 outline-none focus:border-patrol" value={vehicleType} onChange={(e) => setVehicleType(e.target.value)}>
        <option value="">All vehicles</option>
        <option value="car">Car</option>
        <option value="motorcycle">Motorcycle</option>
        <option value="bus">Bus</option>
        <option value="truck">Truck</option>
        <option value="van">Van</option>
        <option value="bicycle">Bicycle</option>
      </select>
      <input className="rounded-md border border-gray-300 px-3 py-2 outline-none focus:border-patrol" type="date" value={date} onChange={(e) => setDate(e.target.value)} />
    </div>
  );
}
