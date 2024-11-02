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
      <nav className="bg-gray-100 shadow-md border-b-2 border-b-purple-950 flex justify-between items-center w-full relative">
        <button className="ml-1 p-1 pt-2" onClick={handleLogoClick}>
          <img src={siteLogo} className="h-12" alt="Logo" />
        </button>

        <ul className="flex space-x-4 m-4 items-center">
          {!isAuthenticated ? (
            <>
              <li>
                <NavButton label="Home" onClick={() => navigate("/")} />
              </li>
              <li>
                <NavButton label="Login" onClick={() => navigate("/login")} />
              </li>
              <li>
                <NavButton label="Register" onClick={() => navigate("/register")} />
              </li>
            </>
          ) : (
            <>
              <div className="relative">
                <button onClick={toggleReminder} aria-label="Reminders">
                  <img src={bellIcon} className="h-8" alt="Bell Icon" />
                </button>
                <ReminderModal isOpen={isReminderOpen} onClose={toggleReminder} />
              </div>
              <li>
                <NavButton label="Calendar" onClick={openCalendar} />
              </li>
              <li>
                <NavButton label="Logout" onClick={handleLogout} />
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
