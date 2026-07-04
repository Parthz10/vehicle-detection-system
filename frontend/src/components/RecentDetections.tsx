import { Detection } from '../types';
import { mediaUrl } from '../api/client';

export function RecentDetections({ detections }: { detections: Detection[] }) {
  return (
    <div className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
      <div className="border-b border-gray-200 px-4 py-3">
        <h2 className="font-semibold text-gray-950">Recent detections</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-gray-50 text-xs uppercase text-gray-500">
            <tr>
              <th className="px-4 py-3">Plate</th>
              <th className="px-4 py-3">Vehicle</th>
              <th className="px-4 py-3">Camera</th>
              <th className="px-4 py-3">Confidence</th>
              <th className="px-4 py-3">Time</th>
              <th className="px-4 py-3">Preview</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {detections.map((item) => {
              const vehicleUrl = mediaUrl(item.vehicle_image_path);
              return (
                <tr key={item.id} className={item.is_blacklisted ? 'bg-red-50' : 'bg-white'}>
                  <td className="px-4 py-3 font-semibold text-gray-950">{item.plate_number}</td>
                  <td className="px-4 py-3 capitalize text-gray-700">{item.vehicle_type}</td>
                  <td className="px-4 py-3 text-gray-700">{item.camera_name}</td>
                  <td className="px-4 py-3 text-gray-700">{Math.round(item.ocr_confidence * 100)}%</td>
                  <td className="px-4 py-3 text-gray-500">{new Date(item.timestamp).toLocaleString()}</td>
                  <td className="px-4 py-3">
                    {vehicleUrl ? <img src={vehicleUrl} className="h-12 w-20 rounded object-cover" /> : <span className="text-gray-400">None</span>}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
