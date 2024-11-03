import { Outlet, useNavigate } from "react-router-dom";
import { siteLogo, bellIcon } from "../../assets";
import { useAuth } from "../../features";
import CalendarModal from "../modals/CalendarModal";
import ReminderModal from "../modals/ReminderModal";
import NavButton from "./NavButton";
import { useState } from "react";

const NavBar: React.FC = () => {
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  const [isReminderOpen, setIsReminderOpen] = useState(false);

  const openCalendar = () => setIsCalendarOpen(true);
  const closeCalendar = () => setIsCalendarOpen(false);
  const navigate = useNavigate();

  const toggleReminder = () => {
    setIsReminderOpen(!isReminderOpen);
  };

  const { isAuthenticated } = useAuth();

  const handleLogoClick = () => {
    if (isAuthenticated) {
      navigate("/dashboard");
    } else {
      navigate("/");
    }
  };

  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <>
      <nav className="bg-gradient-to-r from-indigo-50 via-indigo-100 to-purple-50 shadow-lg border-b-2 border-b-purple-400 flex justify-between items-center w-full py-1 px-6 relative">
  <button className="ml-1 p-1 pt-2 hover:scale-105 transform transition-transform" onClick={handleLogoClick}>
    <img src={siteLogo} className="h-12" alt="Logo" />
  </button>

  <ul className="flex space-x-4 items-center">
    {!isAuthenticated ? (
      <>
        <li>
          <NavButton label="Home" onClick={() => navigate("/")} className="text-gray-800 hover:text-purple-600 transition-colors duration-300" />
        </li>
        <li>
          <NavButton label="Login" onClick={() => navigate("/login")} className="text-gray-800 hover:text-purple-600 transition-colors duration-300" />
        </li>
        <li>
          <NavButton label="Register" onClick={() => navigate("/register")} className="text-gray-800 hover:text-purple-600 transition-colors duration-300" />
        </li>
      </>
    ) : (
      <>
        <div className="relative">
          <button onClick={toggleReminder} aria-label="Reminders" className="hover:scale-110 transform transition-transform">
            <img src={bellIcon} className="h-8" alt="Bell Icon" />
          </button>
          <ReminderModal isOpen={isReminderOpen} onClose={toggleReminder} />
        </div>
        <li>
          <NavButton label="Calendar" onClick={openCalendar} className="text-gray-800 hover:text-purple-600 transition-colors duration-300" />
        </li>
        <li>
          <NavButton label="Logout" onClick={handleLogout} className="text-gray-800 hover:text-purple-600 transition-colors duration-300" />
        </li>
      </>
    )}
  </ul>
</nav>
      <CalendarModal isOpen={isCalendarOpen} onClose={closeCalendar} />
      <Outlet />
    </>
  );
};

export default NavBar;
