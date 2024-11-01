import { API_URL } from "../config";
export default API_URL;

export * from "./postRequests"
export * from "./getRequests"


export { registerUser, loginUser } from "./authApi";
