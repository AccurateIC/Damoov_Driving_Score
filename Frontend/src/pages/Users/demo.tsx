
import React, { useState } from "react";

const Tabs = () => {
  const [activeTab, setActiveTab] = useState("Safety Parameters");

  // Example card data
  const cards = [
    { title: "Safety Score", value: "79.81", unit: "mh", extra: "Last Month" },
    { title: "Trust Level", value: "100", unit: "", extra: "Last Month" },
    { title: "Trips", value: "19", unit: "", extra: "Last Month" },
    { title: "Mileage", value: "1", unit: "", extra: "Last Month" },
    { title: "Time Drive", value: "7.36", unit: "h", extra: "Last Month" },
    { title: "Average speed", value: "12.78", unit: "mh", extra: "Last Month" },
    { title: "Max Speed", value: "66.74", unit: "mh", extra: "Last Month" },
    { title: "Phone Usage", value: "0.00", unit: "%", extra: "Last Month" },
    { title: "Speeding", value: "0.74", unit: "%", extra: "Last Month" },
    { title: "Phone Usage Speed", value: "0.37", unit: "%", extra: "Last Month" },
    // { title: "Unique Tags Count", value: "1", unit: "", extra: "Last Month" },
  ];

  return (
    <div className="flex flex-col bg-amber-100 w-full min-h-[580px]">
      {/* Tab Buttons */}
      <div className="flex w-1/3 mb-4">
        <button
          className={`flex-1 p-2 text-center ${
            activeTab === "Safety Parameters"
              ? "text-blue-600 border-b-2 border-blue-600"
              : ""
          }`}
          onClick={() => setActiveTab("Safety Parameters")}
        >
          Safety Parameters
        </button>

        <button
          className={`flex-1 p-2 text-center ${
            activeTab === "Trips"
              ? "text-blue-600 border-b-2 border-blue-600"
              : ""
          }`}
          onClick={() => setActiveTab("Trips")}
        >
          Trips
        </button>
      </div>

      {/* Tab Content */}
      <div className="flex-grow p-4">
        {activeTab === "Safety Parameters" && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
            {cards.map((card, idx) => (
              <div
                key={idx}
                className="bg-white p-4 rounded-lg shadow flex flex-col justify-between"
              >
                <h3 className="text-lg font-semibold text-gray-700">
                  {card.title}
                </h3>
                <div className="text-3xl font-bold text-gray-900">
                  {card.value} {card.unit}
                </div>
                <p className="text-sm text-gray-500">{card.extra}</p>
              </div>
            ))}
          </div>
        )}

        {activeTab === "Trips" && (
          <div className="text-gray-700">Trips content goes here...</div>
        )}
      </div>
    </div>
  );
};

export default Tabs;
