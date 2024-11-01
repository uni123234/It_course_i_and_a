import { Outlet, useNavigate } from "react-router-dom";
import { siteLogo } from "../../assets";
import { isAuthenticated, useAuth } from "../../features";
import CalendarModal from "../CalendarModal"
import NavButton from "./NavButton";
import { useState } from "react";

const NavBar: React.FC = () => {
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);

  const openCalendar = () => setIsCalendarOpen(true);
  const closeCalendar = () => setIsCalendarOpen(false);
  const navigate = useNavigate();

  const handleLogoClick = () => {
    if (isAuthenticated()) {
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
      <nav className="bg-gray-100 shadow-md border-b-2 border-b-purple-950 flex justify-between items-center w-full">
        <button className="ml-1 p-1 pt-2" onClick={handleLogoClick}>
          <img src={siteLogo} className="h-12" />
        </button>

        <ul className="flex space-x-4 m-4">
          {!isAuthenticated() ? (
            <>
              <li>
                <NavButton label="Home" onClick={() => navigate("/")} />
              </li>
              <li>
                <NavButton label="Login" onClick={() => navigate("/login")} />
              </li>
              <li>
                <NavButton
                  label="Register"
                  onClick={() => navigate("/register")}
                />
              </li>
            </>
          ) : (
            <>
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
