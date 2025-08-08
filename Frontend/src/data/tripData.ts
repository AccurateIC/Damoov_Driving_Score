export interface TripData {
  trackId: string;
  startTime: string;
  endTime: string;
  hiddenFromApp: boolean;
  tags: string[];
  typeOfTransport: string;
  mileage: number;
  timeDrivenMin: number;
  maxSpeed: number;
  averageSpeed: number;
  safetyScore: number;
  fromAddress: string;
  toAddress: string;
  coordinates: { lat: number; lng: number }[];
}

export const trips: TripData[] = [
  {
    trackId: "TRIP-001",
    startTime: "2025/07/03 9:12 AM+03:00",
    endTime: "2025/07/03 9:21 AM+03:00",
    hiddenFromApp: false,
    tags: ["safe"],
    typeOfTransport: "Driver",
    mileage: 5.03,
    timeDrivenMin: 9,
    maxSpeed: 60.43,
    averageSpeed: 40.47,
    safetyScore: 60,
    fromAddress: "2440 W Highlands Ranch Pkwy, Littleton, CO 80129, USA",
    toAddress: "7790 Gore Creek Ln, Littleton, CO 80125, USA",
    coordinates: [
      { lat: 39.55361, lng: -105.0275 },
      { lat: 39.554, lng: -105.025 },
      { lat: 39.555, lng: -105.020 },
      { lat: 39.556, lng: -105.018 },
    ],
  },
  {
    trackId: "TRIP-002",
    startTime: "2025/07/03 9:27 AM+03:00",
    endTime: "2025/07/03 9:41 AM+03:00",
    hiddenFromApp: false,
    tags: ["alert"],
    typeOfTransport: "Driver",
    mileage: 7.46,
    timeDrivenMin: 20,
    maxSpeed: 51.25,
    averageSpeed: 29.8,
    safetyScore: 62,
    fromAddress: "Chiltern Avenue, Aylesbury, HP19 9DN, United Kingdom",
    toAddress: "Parkwood Close, Aylesbury, HP19 9DG, United Kingdom",
    coordinates: [
      { lat: 51.819, lng: -0.813 },
      { lat: 51.820, lng: -0.812 },
      { lat: 51.821, lng: -0.810 },
    ],
  },
  {
    trackId: "TRIP-003",
    startTime: "2025/07/03 9:42 AM+03:00",
    endTime: "2025/07/03 9:46 AM+03:00",
    hiddenFromApp: false,
    tags: ["unsafe"],
    typeOfTransport: "Driver",
    mileage: 1.12,
    timeDrivenMin: 4,
    maxSpeed: 27.81,
    averageSpeed: 16.99,
    safetyScore: 51,
    fromAddress: "1799 Creek Drive, Orlando, FL, USA",
    toAddress: "1840 Moss View Cir, Orlando, FL, USA",
    coordinates: [
      { lat: 28.5383, lng: -81.3792 },
      { lat: 28.5400, lng: -81.3780 },
    ],
  },
];
