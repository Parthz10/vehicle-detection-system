export type Role = 'administrator' | 'police_officer' | 'viewer';

export interface Camera {
  id: number;
  name: string;
  source_type: 'webcam' | 'rtsp' | 'upload' | 'smartphone';
  source_url: string | null;
  location_name: string | null;
  latitude: number | null;
  longitude: number | null;
  is_active: boolean;
}

export interface Detection {
  id: number;
  plate_number: string;
  vehicle_type: string;
  timestamp: string;
  camera_name: string;
  latitude: number | null;
  longitude: number | null;
  vehicle_confidence: number;
  plate_confidence: number;
  ocr_confidence: number;
  vehicle_image_path: string | null;
  plate_image_path: string | null;
  is_blacklisted: boolean;
}

export interface Alert {
  id: number;
  detection_id: number;
  plate_number: string;
  message: string;
  created_at: string;
  acknowledged: boolean;
}

export interface StatsSummary {
  total_detections: number;
  today: number;
  blacklisted_hits: number;
  by_vehicle_type: Record<string, number>;
  by_day: Record<string, number>;
}
