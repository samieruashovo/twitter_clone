import React, { useEffect } from "react";
import "./App.css";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import Activate from "./pages/Activate";
import Profile from "./pages/Profile";
import TweetDetail from "./pages/TweetDetail";
import NotFound from "./components/NotFound";
import { load_user, recommendMeUser } from "./redux/asyncActions/UserAsync";
import { useDispatch, useSelector } from "react-redux";
import BookmarkList from "./pages/BookmarkList";
import ReconnectingWebSocket from "reconnecting-websocket";
import Notifications from "./pages/Notifications";
import { removeNotice, tweetNotice } from "./redux/slices/NotificationSlice";
import Explore from "./pages/Explore";
import ChatMessage from "./pages/ChatMessage";
import PrivateRoomChat from "./pages/PrivateRoomChat";
import FollowUser from "./pages/FollowUser";
import { getNotifications } from "./redux/asyncActions/NotificationAsync";
import Sidebar from "./components/Sidebar";

function App() {
  const userIn = useSelector((state) => state.userReducer);
  const isAuthenticated = userIn.isAuthenticated;
  const dispatch = useDispatch();
  const noticeInfo = useSelector((state) => state.notificationReducer);
  const message = noticeInfo.message;
  let endpoint = `ws://127.0.0.1:3000/ws/home/`;
  let client;

  function websocketCon() {
    client = new ReconnectingWebSocket(endpoint + "?token=" + userIn.access);
    client.onopen = function () {
      console.log("WebSocket Client Connected");
    };

    client.onmessage = function (event) {
      const data = JSON.parse(event.data);
      console.log(data);

      dispatch(tweetNotice(data.payload));
    };

    client.onclose = function () {
      console.log("WebSocket Client disconnected");
    };
  }
  message &&
    setTimeout(() => {
      dispatch(removeNotice());
    }, 3000);

  useEffect(() => {
    if (localStorage.getItem("access")) {
      websocketCon();
    }
  }, [dispatch, websocketCon]);

  useEffect(() => {
    dispatch(load_user());
    if (isAuthenticated) {
      dispatch(recommendMeUser());
      dispatch(getNotifications());
    }

    !isAuthenticated && <Navigate to="/login"></Navigate>;
  }, [dispatch, isAuthenticated]);

  return (
    <BrowserRouter>
      <Routes>
        
        <Route path="/" element={<Home/>} />
        {/* <Route path="/" exact component={Home} /> */}
        <Route path="/activate/:uid/:token" element={<Activate />} />
        {/* <Route path="/activate/:uid/:token" exact component={Activate} /> */}
        <Route path="/login" element={<Login />} />

        {/* <Route path="/login" component={Login} /> */}
        <Route path="/messages/w/:username" element={<PrivateRoomChat />} />

        {/* <Route path="/messages/w/:username" component={PrivateRoomChat} /> */}
        <Route path="/messages" element={<ChatMessage />} />

        {/* <Route path="/messages" component={ChatMessage} /> */}
        {/* <Route path="/register" component={Register} /> */}
        <Route path="/register" element={<Register />} />
        <Route path="/notifications" element={<Notifications />} />

        {/* <Route path="/notifications" component={Notifications} /> */}
        <Route path="/bookmark" element={<BookmarkList />} />

        {/* <Route path="/bookmark" component={BookmarkList} /> */}
        <Route path="/follow-users" element={<FollowUser />} />

        {/* <Route path="/follow-users" component={FollowUser} /> */}
        <Route path="/explore" element={<Explore />} />

        {/* <Route path="/explore" component={Explore} /> */}
        <Route path="user/:username" element={<Profile />} />

        {/* <Route path="/:username" exact component={Profile} /> */}
        <Route path="/:username/tweet/:id" element={<TweetDetail />} />

        {/* <Route path="/:username/tweet/:id" component={TweetDetail} /> */}
        <Route path="" element={<NotFound />} />

        <Route path="" component={NotFound} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
