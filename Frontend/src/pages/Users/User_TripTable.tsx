// import React from "react";

// const sampleTrips = Array.from({ length: 10 }, (_, idx) => ({
//   deviceId: "12345",
//   name: "Trip1",
//   startTime: "22.8.25 / 4:53 PM",
//   endTime: "22.8.25 / 4:53 PM",
//   tripDistance: idx % 5 === 0 ? 1 : 45 + (idx % 3) * 5,
//   uniqueId: idx + 1,
// }));

// const TripsTable = () => {
//   return (
//     <div className="  p-6 md:-w-[100px] mb-4">
//       <div >
//         <table className="w-full border-collapse">
//         <thead>
//           <tr className="bg-[#B5B6D5] text-gray-700 ">
//             <th className="p-2 rounded-tl-lg  ">#</th>
//             <th className="p-2  ">Device ID</th>
//             <th className="p-2 ">Name</th>
//             <th className="p-2 ">Start Time</th>
//             <th className="p-2 ">End Time</th>
//             <th className="p-2 ">Trip Distance</th>
//             <th className="p-2 ">Unique ID</th>
//           </tr>
//         </thead>
//         <tbody>
//           {sampleTrips.map((trip, index) => (
//             <tr key={index} className="text-center border-b last:border-none hover:bg-gray-100">
//               <td className="p-2 ">{index + 1}</td>
//               <td className="p-2 ">{trip.deviceId}</td>
//               <td className="p-2 ">{trip.name}</td>
//               <td className="p-2 ">{trip.startTime}</td>
//               <td className="p-2 ">{trip.endTime}</td>
//               <td className="p-2 ">{trip.tripDistance}</td>
//               <td className="p-2 ">{trip.uniqueId}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//       </div>
//     </div>
//   );
// };

// export default TripsTable;


import React from "react";

const sampleTrips = Array.from({ length: 10 }, (_, idx) => ({
  deviceId: "12345",
  name: "Trip1",
  startTime: "22.8.25 / 4:53 PM",
  endTime: "22.8.25 / 4:53 PM",
  tripDistance: idx % 5 === 0 ? 1 : 45 + (idx % 3) * 5,
  uniqueId: idx + 1,
}));

const TripsTable = () => {
  return (
    <div className="m-2 md:w-full mb-4 ">
      {/* Scroll container */}
      <div className="max-h-[450px] overflow-auto bg-white rounded-lg">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-[#B5B6D5] text-gray-700 sticky top-0">
              <th className="p-2 rounded-tl-lg">#</th>
              <th className="p-2">Device ID</th>
              <th className="p-2">Name</th>
              <th className="p-2">Start Time</th>
              <th className="p-2">End Time</th>
              <th className="p-2">Trip Distance</th>
              <th className="p-2">Unique ID</th>
            </tr>
          </thead>
          <tbody>
            {sampleTrips.map((trip, index) => (
              <tr
                key={index}
                className="text-center border-b last:border-none font-md text-[14px] hover:bg-gray-100 "
              >
                <td className="px-4 py-3">{index + 1}</td>
                <td className="px-4 py-3">{trip.deviceId}</td>
                <td className="px-4 py-3">{trip.name}</td>
                <td className="px-4 py-3">{trip.startTime}</td>
                <td className="px-4 py-3">{trip.endTime}</td>
                <td className="px-4 py-3">{trip.tripDistance}</td>
                <td className="px-4 py-3">{trip.uniqueId}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TripsTable;
