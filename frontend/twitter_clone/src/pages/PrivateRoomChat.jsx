import React, { useEffect, useState, useRef } from "react";
import Message from "./Message";
import { useParams } from "react-router";
import { BiSend, BiUpArrowCircle } from "react-icons/bi";
import TweetHeader from "../components/TweetComponents/tweetHeader";
import Pop from "../pop.mp3";
import { useSelector, useDispatch } from "react-redux";
import {
  getChatMessage,
  loadMoreMessage,
} from "../redux/asyncActions/ChatAsync";
import { addMsg } from "../redux/slices/ChatSlice";
import ReconnectingWebSocket from "reconnecting-websocket";
import AddPicker from "../components/SmallComponent/AddPicker";
import { Link } from "react-router-dom";
import { setMsgNoti } from "../redux/slices/NotificationSlice";
// import { axiosInstance } from "..";
import axios from "axios";



const PrivateRoomChat = () => {
  const [msgInput, setMsgInput] = useState("");
  const [istyping, setIstyping] = useState(null);
  const [typingUser, setTypingUser] = useState(null);
  const { username } = useParams();
  const userIn = useSelector((state) => state.userReducer);
  const [noScroll, setNoScroll] = useState(true);
  const dispatch = useDispatch();
  let endpoint = "ws://localhost:3000/";
  let endp = "http://127.0.0.1:8000/";
  const me = userIn.user?.username;
  const chatState = useSelector((state) => state.chatReducer);
  const chats = chatState.chatMessage;
  const meta = chatState.meta;
  const [onlineStatus, setOnlineStatus] = useState(null);
  const audioRef = useRef(null);
  const msgDivRef = useRef(null);

  const client = new ReconnectingWebSocket(
    endpoint + "ws/chat/" + username + "/" + "?token=" + userIn.access
  );
  const axiosInstance = axios.create({
    baseURL: "http://127.0.0.1:8000/",
    timeout: 5000,
    headers: {
      "Content-Type": "application/json",
      accept: "application/json",
    },
  });
  useEffect(() => {
    if (localStorage.getItem("access")) {
      client.onopen = function () {
        console.log("Chat Websoket Connected");
        dispatch(setMsgNoti());
      };

      client.onmessage = function (event) {
        const data = JSON.parse(event.data);

        if (data.command === "private_chat") {
          dispatch(addMsg(data));
          if (audioRef.current) {
            audioRef.current.play();
          }
          // msgDivRef.current.scrollTop = msgDivRef.current.scrollHeight;
          // console.log(data);
        }
        // if (data.command === "is_typing") {
        //   setTypingUser(data.user);
        //   setIstyping(data.text);
        //   timer = setTimeout(() => {
        //     setIstyping(null);
        //   }, 500);
        // }
      };
      // client.onclose = function () {
      //   console.log("WebSocket Client disconnected");
      // };
    }
  }, [dispatch]);

  useEffect(() => {
    if (noScroll) {
      msgDivRef.current.scrollTop = msgDivRef.current.scrollHeight;
    }
  }, [chats]);

  const EnterKey = (e) => {
    //hit enter key in input
    if (e.key === "Enter" || e.keyCode === 13) {
      if (msgInput.length !== 0) {
        sendChat(e);
      }
    }
  };

  useEffect(() => {
    dispatch(getChatMessage(username));
  }, [dispatch, username]);

  // export const reTweet = (tweetId) => async (dispatch) => {
  //   try {
  //     const res = await axiosInstance.post(`tweets/post/retweet/`, {
  //       tweetId: tweetId,
  //     });
  
  //     dispatch(tweetAdded(res.data));
  //     dispatch(setMessage(`Re Tweeted !`));
  //   } catch (err) {
  //     dispatch(tweetFail());
  //     console.log(err.response.data);
  //     dispatch(setMessage(err.response.data.detail));
  //   }
  // };
  const sendChat = async (e) => {
    e.preventDefault();
    if (!msgInput) {
      alert("cannot be blank !");
    } else {
        const res = await axiosInstance.post(`chats/send_msg/`, {
    
            "id": 1,
            "sender":me,
            "text": msgInput

      });
      // client.send(
      //   JSON.stringify({
      //     command: "private_chat",
      //     message: msgInput,
      //     username: me,
      //   })
      // );
    }
    setMsgInput("");
  };
  const getChat = async (e) => {

        const res = await axiosInstance.get(`chats/send_msg/`);
        const data = res.data;
        if (data && data.length > 0) {
          const conversation = data[0]; // Assuming you have only one conversation in the array
        
          // Iterate through the messages in the conversation
          for (const message of conversation.messages) {
            const sender = message.sender;
            const username = sender.username;
            const text = message.text;
            const profilePic = sender.profile_pic;
        
            // Now you can use the username, text, and profilePic as needed
            console.log(`Username: ${username}`);
            console.log(`Text: ${text}`);
            console.log(`Profile Picture: ${profilePic}`);
          }
        }


  };
  let timer;
  // const isTyping = (e) => {
  //   window.clearTimeout(timer);
  //   client.send(
  //     JSON.stringify({
  //       command: "is_typing",
  //       text: `${me} is typing ...`,
  //       user: me,
  //     })
  //   );
  // };

  function loadMore() {
    if (meta?.next) {
      setNoScroll(false);
      dispatch(loadMoreMessage(meta.next));
    }
  }
  // if (meta?.next && msgDivRef.current && msgDivRef.current.scrollTop < 40) {
  //   loadMore();
  // }
  return (
    <Message>
      <TweetHeader headerName={username} />

      <div className="main-div">
        <audio ref={audioRef} src={Pop}></audio>
        <div ref={msgDivRef} id="msg-scoll" className="msg-div">
          {meta?.next && (
            <i
              onClick={loadMore}
              className="largeicon center"
              title="load more"
            >
              <BiUpArrowCircle />
            </i>
          )}

<div ref={msgDivRef} id="msg-scoll" className="msg-div">
          {meta?.next && (
            <i onClick={loadMore} className="largeicon center" title="load more">
              <BiUpArrowCircle />
            </i>
          )}
          {chats &&
            chats
              .slice()
              .reverse() // reversing array
              .map((msg) => (
                <div
                  key={msg.id}
                  className={
                    msg?.sender?.username === me ? "rightby" : "msg-chat"
                  }
                >
                  {msg?.sender?.username !== me && (
                    <Link to={`/${msg?.sender.username}`}>
                      <img
                        src={msg?.sender.profile_pic}
                        alt="profile"
                        className="authorImage"
                      />
                    </Link>
                  )}
                  <div
                    className={
                      msg.sender?.username === me ? "msg-txt right" : "msg-txt"
                    }
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
        </div>
Hello
          {/* {chats &&
            chats
              .slice()
              .reverse() //revrsing array
              .map((msg) => (
                <div
                  key={msg.id}
                  className={
                    msg?.sender?.username === username ? "msg-chat" : "rightby"
                  }
                >
                  {msg?.sender?.username === username && (
                    <Link to={`/${msg?.sender.username}`}>
                      <img
                        src={msg?.sender.profile_pic}
                        alt="profile"
                        className="authorImage"
                      />
                    </Link>
                  )}

                  <div
                    className={
                      msg.sender?.username === username
                        ? "msg-txt"
                        : "msg-txt right"
                    }
                  >
                    {msg.text}
                  </div>
                </div>
              ))} */}
        </div>

        <div className="bottom-input">
          {typingUser !== me && (
            <span
              style={{ position: "absolute", left: 10, bottom: 50 }}
              className="ml-4"
            >
              {istyping}
            </span>
          )}
          <input
            type="text"
            value={msgInput}
            onChange={(e) => setMsgInput(e.target.value)}
            placeholder="Start a new message"
            onKeyDown={EnterKey}
            // onKeyPress={isTyping}
            className="chat-input"
          />

          <span className="d-flex">
            <AddPicker
              classNem="chatEmoji"
              position="up"
              setInput={setMsgInput}
            />
            <BiSend onClick={getChat} className="largeicon mx-2" />
          </span>
        </div>
      </div>
    </Message>
  );
};

export default PrivateRoomChat;
