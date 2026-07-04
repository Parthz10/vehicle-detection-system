import { useEffect, useRef, useState } from 'react';
import { Camera, LocateFixed, Upload } from 'lucide-react';
import { api } from '../api/client';

export function PhoneCamera() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [coords, setCoords] = useState<{ latitude: number; longitude: number } | null>(null);
  const [status, setStatus] = useState('Ready');
  const location = coords ? `${coords.latitude.toFixed(5)}, ${coords.longitude.toFixed(5)}` : 'Location not shared';

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false }).then((stream) => {
      if (videoRef.current) videoRef.current.srcObject = stream;
    });
    navigator.geolocation?.getCurrentPosition((pos) => {
      setCoords({ latitude: pos.coords.latitude, longitude: pos.coords.longitude });
    });
  }, []);

  async function captureAndSend() {
    const video = videoRef.current;
    if (!video) return;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d')?.drawImage(video, 0, 0);
    canvas.toBlob(async (blob) => {
      if (!blob) return;
      const form = new FormData();
      form.append('camera_name', 'Smartphone camera');
      if (coords) {
        form.append('latitude', String(coords.latitude));
        form.append('longitude', String(coords.longitude));
      }
      form.append('file', blob, 'phone-frame.jpg');
      setStatus('Uploading frame');
      try {
        const { data } = await api.post('/streams/upload-frame', form);
        setStatus(`${data.length} detection${data.length === 1 ? '' : 's'} saved`);
      } catch {
        setStatus('Upload failed. Login on this device first.');
      }
    }, 'image/jpeg', 0.92);
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white">
      <div className="mx-auto max-w-3xl px-4 py-4">
        <div className="mb-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Camera size={20} />
            <h1 className="font-semibold">Smartphone camera</h1>
          </div>
          <div className="flex items-center gap-1 text-sm text-gray-300">
            <LocateFixed size={16} /> {location}
          </div>
        </div>
        <video ref={videoRef} autoPlay playsInline muted className="aspect-video w-full rounded-lg bg-black object-contain" />
        <div className="mt-4 flex items-center justify-between gap-3">
          <p className="text-sm text-gray-300">{status}</p>
          <button onClick={captureAndSend} className="inline-flex items-center gap-2 rounded-md bg-patrol px-4 py-2 font-medium text-white">
            <Upload size={18} /> Send frame
          </button>
        </div>
      </div>
    </main>
  );
}
