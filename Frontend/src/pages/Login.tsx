import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // ✅ For navigation
import logo from "../assets/logo.png";
import tempo from "../assets/tempo.png";
import gradientBox from "../assets/rectangle.svg";

const baseURL = import.meta.env.VITE_BASE_URL;

export default function LoginPage() {
  const [activeTab, setActiveTab] = useState("signin");
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    remember: false,
  });
  const [showForgotModal, setShowForgotModal] = useState(false);
  const [resetEmail, setResetEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const savedEmail = localStorage.getItem("rememberedEmail");
    if (savedEmail) {
      setFormData((prev) => ({ ...prev, email: savedEmail, remember: true }));
    }
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // const API_BASE = "http://127.0.0.1:5000";
    setLoading(true);

    try {
      let response;
      if (activeTab === "signup") {
        if (formData.password.length < 8) {
          alert("Password must be at least 8 characters long.");
          setLoading(false);
          return;
        }
        if (formData.password !== formData.confirmPassword) {
          alert("Passwords do not match!");
          setLoading(false);
          return;
        }

        response = await fetch(`${baseURL}/signup`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: formData.name,
            email: formData.email,
            password: formData.password,
            confirm_password: formData.confirmPassword,
          }),
        });
      } else {
        response = await fetch(`${baseURL}/signin`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
          }),
        });
      }

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || "Something went wrong!");
      }

      // ✅ Save token and user in localStorage
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data));

      // ✅ Remember email if checked
      if (formData.remember) {
        localStorage.setItem("rememberedEmail", formData.email);
      } else {
        localStorage.removeItem("rememberedEmail");
      }

      // alert(data.message);
  navigate("/dashboard/summary_New"); // ✅ Redirect after success
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = (e) => {
    e.preventDefault();
    if (!resetEmail) {
      alert("Please enter your email!");
      return;
    }
    alert(`📧 Password reset link sent to ${resetEmail}`);
    setResetEmail("");
    setShowForgotModal(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="w-full h-screen bg-white grid grid-cols-1 md:grid-cols-2">
        {/* Left Section */}
        <div className="flex flex-col justify-center items-center px-4 sm:px-8 md:px-10">
          <div className="mb-2 flex flex-col items-center">
            <img
              src={logo}
              alt="logo"
              className="h-12 sm:h-14 md:h-16 lg:h-20 mb-2 object-contain"
            />
          </div>

          <h1 className="text-lg sm:text-xl md:text-2xl font-medium mb-2 text-center">
            Welcome to Accurate!
          </h1>
          <p className="text-gray-400 mb-6 text-center text-sm sm:text-base">
            We are ready to serve you anytime
          </p>

          <div className="flex mb-6 w-full max-w-xs sm:max-w-sm rounded-full border border-gray-200 overflow-hidden">
            <button
              onClick={() => setActiveTab("signin")}
              className={`flex-1 py-2 sm:py-3 font-medium transition ${
                activeTab === "signin"
                  ? "bg-indigo-600 text-white"
                  : "bg-white text-gray-500"
              }`}
            >
              Sign In
            </button>
            <button
              onClick={() => setActiveTab("signup")}
              className={`flex-1 py-2 sm:py-3 font-medium transition ${
                activeTab === "signup"
                  ? "bg-indigo-600 text-white"
                  : "bg-white text-gray-600"
              }`}
            >
              Sign Up
            </button>
          </div>

          <form
            className="w-full max-w-xs sm:max-w-sm space-y-4"
            onSubmit={handleSubmit}
          >
            {activeTab === "signup" && (
              <input
                type="text"
                name="name"
                placeholder="Enter Your Name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 rounded-full border border-gray-300 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            )}

            <input
              type="email"
              name="email"
              placeholder="Enter Your Email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 rounded-full border border-gray-300 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <input
              type="password"
              name="password"
              placeholder="Enter Your Password"
              value={formData.password}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 rounded-full border border-gray-300 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            {activeTab === "signup" && (
              <>
                <input
                  type="password"
                  name="confirmPassword"
                  placeholder="Confirm Your Password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 rounded-full border border-gray-300 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <p className="text-xs sm:text-sm text-gray-500">
                  The password must be at least 8 characters long and include
                  special characters such as (*, @, etc.)
                </p>
              </>
            )}

            {activeTab === "signin" && (
              <div className="flex items-center justify-between text-xs sm:text-sm">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    name="remember"
                    checked={formData.remember}
                    onChange={handleChange}
                    className="text-indigo-600 focus:ring-indigo-500"
                  />
                  Remember Me
                </label>
                <button
                  type="button"
                  onClick={() => setShowForgotModal(true)}
                  className="text-indigo-600 font-medium"
                >
                  Forgot Password?
                </button>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 text-white py-3 rounded-full font-medium hover:bg-indigo-700 transition text-sm sm:text-base"
            >
              {loading
                ? "Please wait..."
                : activeTab === "signin"
                ? "Sign In"
                : "Sign Up"}
            </button>
          </form>
        </div>

        {/* Right Section */}
        <div className="flex flex-col justify-center items-center bg-gray-100 p-6">
          <div className="relative w-full flex justify-center">
            <img
              src={gradientBox}
              alt="Gradient Background"
              className="w-3/4 sm:w-2/3 md:w-1/2 lg:w-2/5 max-w-md rounded-3xl"
            />
            <img
              src={tempo}
              alt="Tempo"
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 
              w-4/5 sm:w-3/4 md:w-2/3 lg:w-1/2 max-w-sm object-contain"
            />
          </div>

          <p className="mt-6 text-gray-500 text-sm text-center px-4">
            “Track your fleet is easy with Damoov”
          </p>
        </div>
      </div>

      {/* Forgot Password Modal */}
      {showForgotModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 px-4">
          <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-sm">
            <h2 className="text-lg sm:text-xl font-semibold mb-4">
              Forgot Password
            </h2>
            <form onSubmit={handleForgotPassword} className="space-y-4">
              <input
                type="email"
                placeholder="Enter your registered email"
                value={resetEmail}
                onChange={(e) => setResetEmail(e.target.value)}
                required
                className="w-full px-4 py-3 rounded-full border border-gray-300 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <button
                type="submit"
                className="w-full bg-indigo-600 text-white py-2 rounded-full hover:bg-indigo-700 transition text-sm sm:text-base"
              >
                Send Reset Link
              </button>
              <button
                type="button"
                onClick={() => setShowForgotModal(false)}
                className="w-full bg-gray-300 text-gray-700 py-2 rounded-full hover:bg-gray-400 transition text-sm sm:text-base"
              >
                Cancel
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}


// import React, { useState, useEffect } from "react";
// import logo from "../assets/logo.png";
// import tempo from "../assets/tempo.png";
// import gradientBox from "../assets/rectangle.svg";

// export default function LoginPage() {
//   const [activeTab, setActiveTab] = useState("signin");
//   const [formData, setFormData] = useState({
//     email: "",
//     password: "",
//     confirmPassword: "",
//     remember: false,
//   });
//   const [showForgotModal, setShowForgotModal] = useState(false);
//   const [resetEmail, setResetEmail] = useState("");

//   useEffect(() => {
//     const savedEmail = localStorage.getItem("rememberedEmail");
//     if (savedEmail) {
//       setFormData((prev) => ({ ...prev, email: savedEmail, remember: true }));
//     }
//   }, []);

//   const handleChange = (e) => {
//     const { name, value, type, checked } = e.target;
//     setFormData((prev) => ({
//       ...prev,
//       [name]: type === "checkbox" ? checked : value,
//     }));
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();

//     if (activeTab === "signup") {
//       if (formData.password.length < 8) {
//         alert("Password must be at least 8 characters long.");
//         return;
//       }
//       if (formData.password !== formData.confirmPassword) {
//         alert("Passwords do not match!");
//         return;
//       }
//       alert("✅ Sign Up Successful!");
//     } else {
//       if (formData.remember) {
//         localStorage.setItem("rememberedEmail", formData.email);
//       } else {
//         localStorage.removeItem("rememberedEmail");
//       }
//       alert("✅ Sign In Successful!");
//     }
//   };

//   const handleForgotPassword = (e) => {
//     e.preventDefault();
//     if (!resetEmail) {
//       alert("Please enter your email!");
//       return;
//     }
//     alert(`📧 Password reset link sent to ${resetEmail}`);
//     setResetEmail("");
//     setShowForgotModal(false);
//   };

//   return (
//     <div className="min-h-screen bg-gray-100 flex items-center justify-center">
//       <div className="w-full h-screen bg-white grid grid-cols-1 md:grid-cols-2">
//         <div className="flex flex-col justify-center items-center px-4 sm:px-8 md:px-10">
//           <div className="mb-2 flex flex-col items-center">
//             <img
//               src={logo}
//               alt="logo"
//               className="h-12 sm:h-14 md:h-16 lg:h-20 mb-2 object-contain"
//             />
//           </div>

//           <h1 className="text-lg sm:text-xl md:text-2xl font-medium mb-2 text-center">
//             Welcome to Accurate!
//           </h1>
//           <p className="text-gray-400 mb-6 text-center text-sm sm:text-base">
//             We are ready to serve you anytime
//           </p>

//           <div className="flex mb-6 w-full max-w-xs sm:max-w-sm rounded-full border border-gray-200 overflow-hidden">
//             <button
//               onClick={() => setActiveTab("signin")}
//               className={`flex-1 py-2 sm:py-3 font-medium transition ${
//                 activeTab === "signin"
//                   ? "bg-indigo-600 text-white"
//                   : "bg-white text-gray-500"
//               }`}
//             >
//               Sign In
//             </button>
//             <button
//               onClick={() => setActiveTab("signup")}
//               className={`flex-1 py-2 sm:py-3 font-medium transition ${
//                 activeTab === "signup"
//                   ? "bg-indigo-600 text-white"
//                   : "bg-white text-gray-600"
//               }`}
//             >
//               Sign Up
//             </button>
//           </div>

//           <form
//             className="w-full max-w-xs sm:max-w-sm space-y-4"
//             onSubmit={handleSubmit}
//           >
//             <input
//               type="email"
//               name="email"
//               placeholder="Enter Your Email"
//               value={formData.email}
//               onChange={handleChange}
//               required
//               className="w-full px-4 py-3 rounded-full border border-gray-300 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
//             />

//             <input
//               type="password"
//               name="password"
//               placeholder="Enter Your Password"
//               value={formData.password}
//               onChange={handleChange}
//               required
//               className="w-full px-4 py-3 rounded-full border border-gray-300 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
//             />

//             {activeTab === "signup" && (
//               <>
//                 <input
//                   type="password"
//                   name="confirmPassword"
//                   placeholder="Confirm Your Password"
//                   value={formData.confirmPassword}
//                   onChange={handleChange}
//                   required
//                   className="w-full px-4 py-3 rounded-full border border-gray-300 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
//                 />
//                 <p className="text-xs sm:text-sm text-gray-500">
//                   The password must be at least 8 characters long and include
//                   special characters such as (*, @, etc.)
//                 </p>
//               </>
//             )}

//             {activeTab === "signin" && (
//               <div className="flex items-center justify-between text-xs sm:text-sm">
//                 <label className="flex items-center gap-2">
//                   <input
//                     type="checkbox"
//                     name="remember"
//                     checked={formData.remember}
//                     onChange={handleChange}
//                     className="text-indigo-600 focus:ring-indigo-500"
//                   />
//                   Remember Me
//                 </label>
//                 <button
//                   type="button"
//                   onClick={() => setShowForgotModal(true)}
//                   className="text-indigo-600 font-medium"
//                 >
//                   Forgot Password?
//                 </button>
//               </div>
//             )}

//             <button
//               type="submit"
//               className="w-full bg-indigo-600 text-white py-3 rounded-full font-medium hover:bg-indigo-700 transition text-sm sm:text-base"
//             >
//               {activeTab === "signin" ? "Sign In" : "Sign Up"}
//             </button>
//           </form>
//         </div>

//         <div className="flex flex-col justify-center items-center bg-gray-100 p-6">
//           <div className="relative w-full flex justify-center">
//             <img
//               src={gradientBox}
//               alt="Gradient Background"
//               className="w-3/4 sm:w-2/3 md:w-1/2 lg:w-2/5 max-w-md rounded-3xl"
//             />
//             <img
//               src={tempo}
//               alt="Tempo"
//               className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 
//               w-4/5 sm:w-3/4 md:w-2/3 lg:w-1/2 max-w-sm object-contain"
//             />
//           </div>

//           <p className="mt-6 text-gray-500 text-sm text-center px-4">
//             “Track your fleet is easy with Damoov”
//           </p>
//         </div>
//       </div>

//       {showForgotModal && (
//         <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 px-4">
//           <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-sm">
//             <h2 className="text-lg sm:text-xl font-semibold mb-4">
//               Forgot Password
//             </h2>
//             <form onSubmit={handleForgotPassword} className="space-y-4">
//               <input
//                 type="email"
//                 placeholder="Enter your registered email"
//                 value={resetEmail}
//                 onChange={(e) => setResetEmail(e.target.value)}
//                 required
//                 className="w-full px-4 py-3 rounded-full border border-gray-300 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
//               />
//               <button
//                 type="submit"
//                 className="w-full bg-indigo-600 text-white py-2 rounded-full hover:bg-indigo-700 transition text-sm sm:text-base"
//               >
//                 Send Reset Link
//               </button>
//               <button
//                 type="button"
//                 onClick={() => setShowForgotModal(false)}
//                 className="w-full bg-gray-300 text-gray-700 py-2 rounded-full hover:bg-gray-400 transition text-sm sm:text-base"
//               >
//                 Cancel
//               </button>
//             </form>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }
