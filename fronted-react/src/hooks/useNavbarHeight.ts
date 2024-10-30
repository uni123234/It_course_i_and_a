import { useState, useEffect } from "react";

export const useNavbarHeight = () => {
  const [navbarHeight, setNavbarHeight] = useState<number>(0);

  useEffect(() => {
    const navbar = document.querySelector("nav") as HTMLElement;
    if (navbar) {
      setNavbarHeight(navbar.offsetHeight);
      console.log("Navbar height: ", navbar.offsetHeight);
    }
  }, []);

  return navbarHeight;
};

export default useNavbarHeight;
