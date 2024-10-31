import { Outlet, useNavigate } from "react-router-dom";
import { siteLogo } from "../../assets";
import { isAuthenticated } from "../../features";
import NavButton from "./NavButton";

const NavBar: React.FC = () => {
  const navigate = useNavigate();

  const handleLogoClick = () => {
    if (isAuthenticated()) {
      navigate("/dashboard");
    } else {
      navigate("/");
    }
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
            <></>
          )}
        </ul>
      </nav>
      <Outlet />
    </>
  );
};

export default NavBar;
