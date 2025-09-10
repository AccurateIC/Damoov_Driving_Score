import React, { useState } from "react";
import TripsTable from "./User_TripTable"

const Tabs = () => {
  const [activeTab, setActiveTab] = useState("Safety Parameters");
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
    {
      title: "Phone Usage Speed",
      value: "0.37",
      unit: "%",
      extra: "Last Month",
    },
    { title: "Unique Tags Count", value: "1", unit: "", extra: "Last Month" },
  ];

  return (
    // <div className="flex  flex-col justify-start bg-amber-200 w-full h-full
    //  ">
    //   {/* Tab Buttons */}
    //   <div className="flex bg-amber-500  w-1/3 mb-4">
    //     <button
    //       className={`flex-1 p-2 text-center ${
    //         activeTab === "Safety Parameters" ? "text-blue-600 border-b-2 border-blue-600" : ""
    //       }`}
    //       onClick={() => setActiveTab("Safety Parameters")}
    //     >
    //       Safety Parameters
    //     </button>

    //     <button
    //       className={`flex-1 p-2 text-center ${
    //         activeTab === "Trips" ? "text-blue-600 border-b-2 border-blue-600" : ""
    //       }`}
    //       onClick={() => setActiveTab("Trips")}
    //     >
    //       Trips
    //     </button>
    //   </div>

    //   {/* Tab Content */}
    //   <div className=" h-full">
    //     {activeTab === "Safety Parameters" && <div className="bg-amber-700 h-full" >Safety Paramete</div>}
    //     {activeTab === "Trips" && <div>Trips</div>}
    //   </div>
    // </div>
    <div className="flex flex-col  w-full min-h-[580px]">
      {/* Tab Buttons */}
      <div className="flex  w-1/4 mb-4 text-xl">
        <button
          className={`flex-1  text-center ${
            activeTab === "Safety Parameters"
              ? "text-blue-600 border-b-2 border-blue-600 "
              : ""
          }`}
          onClick={() => setActiveTab("Safety Parameters")}
        >
          Safety Parameters
        </button>

        <button
          className={`flex-1  text-center ${
            activeTab === "Trips"
              ? "text-blue-600 border-b-2 border-blue-600 "
              : ""
          }`}
          onClick={() => setActiveTab("Trips")}
        >
          Trips
        </button>
      </div>

      {/* Tab Content */}
      <div className="flex-grow  p-4  ">
        {activeTab === "Safety Parameters" && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 p-  3xl:max-w-[1415px] 3xl:min-h-[400px] 3xl:grid-cols-6 gap-8">
            {cards.map((card, idx) => (
              <div
                key={idx}
                className="flex flex-col bg-white mb-4 gap-4 2xl:max-w-[209px] 2xl:max-h-[192px] rounded-xl shadow-sm p-8  hover:shadow-md transition-shadow "
              >
                <h3 className="text-md font-md text-gray-700">{card.title}</h3>
                <div className="text-3xl font-bold text-gray-900">
                  {card.value} {card.unit}
                </div>
                {/* <p className="text-sm font-medium text-gray-500">
                  {card.extra}
                </p> */}
                
                 <p className=" font-normal text-sm -2 flex gap-3 ">
                  Last Month{" "}
                  <span className="font-medium text-xs text-green-500 border-1 px-2 border-gray-700 p-1 rounded-xl">
                    {" "}
                    25%
                  </span>
                    </p>
              </div>
            ))}
          </div>
        )}

        {activeTab === "Trips" && (
  <div className=" ">
    <TripsTable />
  </div>
)}
      </div>
    </div>
  );
};

export default Tabs;
