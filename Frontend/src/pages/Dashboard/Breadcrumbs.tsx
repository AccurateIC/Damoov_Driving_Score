import React from "react";
import { Link, useLocation } from "react-router-dom";

const Breadcrumbs: React.FC = () => {
  const location = useLocation();

  // Split path into segments
  const pathnames = location.pathname.split("/").filter((x) => x);

  // Format function: clean names
  const formatName = (str: string) => {
    return str
      .replace(/_/g, " ")
      .replace(/-/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

 return (
  <div className="font-medium text-gray-400 mb-[23px]">
    {/* Always show Dashboard as the root */}
    {/* <Link to="/dashboard" className="hover:text-indigo-500">
      Dashboard
    </Link> */}

    {pathnames.map((name, index) => {
      const routeTo = `/${pathnames.slice(0, index + 1).join("/")}`;
      const isLast = index === pathnames.length - 1;

      return (
      <span key={routeTo}>
  {index > 0 && " > "}
  {isLast ? (
    <span className="font-bold text-xl text-gray-800">
      {formatName(name)}
    </span>
  ) : (
    <Link to={routeTo} className="hover:text-indigo-500">
      {formatName(name)}
    </Link>
  )}
</span>

      );
    })}
  </div>
);

};

export default Breadcrumbs;

// import React from "react";
// import { Link, useLocation } from "react-router-dom";

// const Breadcrumbs: React.FC = () => {
//   const location = useLocation();

//   // Split path into segments
//   const pathnames = location.pathname.split("/").filter((x) => x);

//   return (
//     <div className="md:w-[204px] md:h-[30px] font-medium text-gray-400 mb-[23px]">
//       {pathnames.length === 0 ? (
//         <span className="font-bold text-xl text-gray-800">Dashboard</span>
//       ) : (
//         <>
//           <Link to="/dashboard" className="hover:text-indigo-500">
//             Dashboard
//           </Link>
//           {pathnames.map((name, index) => {
//             const routeTo = `/${pathnames.slice(0, index + 1).join("/")}`;
//             const isLast = index === pathnames.length - 1;

//             return (
//               <span key={routeTo}>
//                 {" > "}
//                 {isLast ? (
//                   <span className="font-bold text-xl text-gray-800 capitalize">
//                     {name.replace("-", " ")}
//                   </span>
//                 ) : (
//                   <Link
//                     to={routeTo}
//                     className="hover:text-indigo-500 capitalize"
//                   >
//                     {name.replace("-", " ")}
//                   </Link>
//                 )}
//               </span>
//             );
//           })}
//         </>
//       )}
//     </div>
//   );
// };

// export default Breadcrumbs;
