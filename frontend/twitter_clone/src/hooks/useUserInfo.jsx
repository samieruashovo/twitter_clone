import { useEffect } from "react";
import { checkAuthenticated, load_user } from "../redux/asyncActions/UserAsync";
import { useDispatch, useSelector } from "react-redux";

const useUserInfo = () => {
  const userInfo = useSelector((state) => state.userReducer);
  console.log("userinfo" + userInfo);
  const user = userInfo.user;
  console.log("user" + user);
  const isAuthenticated = userInfo.isAuthenticated;
  console.log("isauthenticated" + isAuthenticated);
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(load_user());
    dispatch(checkAuthenticated());
  }, [dispatch]);
  return { user, isAuthenticated };
};
export default useUserInfo;
