import React from 'react';

interface TimelineEvent {
  label: string;
  segments: { start: number; end: number }[];
  color: string;
}

interface TripTimelineChartProps {
  duration: number; // total duration in seconds
  events: TimelineEvent[];
}

const TripTimelineChart: React.FC<TripTimelineChartProps> = ({ duration, events }) => {
  return (
    <div className="w-full space-y-4">
      <div className="flex flex-col gap-3">
        {events.map((event, idx) => (
          <div key={idx}>
            <div className="text-sm text-gray-700 mb-1">{event.label}</div>
            <div className="relative w-full h-6 bg-gray-200 rounded overflow-hidden">
              {event.segments.map((seg, sIdx) => {
                const left = (seg.start / duration) * 100;
                const width = ((seg.end - seg.start) / duration) * 100;
                return (
                  <div
                    key={sIdx}
                    className="absolute h-full rounded"
                    style={{
                      left: `${left}%`,
                      width: `${width}%`,
                      backgroundColor: event.color,
                    }}
                  ></div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-between text-xs text-gray-500 pt-2">
        <span>00:00</span>
        <span>{new Date(duration * 1000).toISOString().substr(14, 5)}</span>
      </div>
    </div>
  );
};

export default TripTimelineChart;
