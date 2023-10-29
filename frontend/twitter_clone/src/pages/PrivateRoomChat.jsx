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
  const [chatData, setChatData] = useState([]); 
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

        }

      };

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

    }
    setMsgInput("");
    window.location.reload();
  };
// let chatData =[];
let convo;
  const getChat = async (e) => {

        const res = await axiosInstance.get(`chats/send_msg/`);
        const data = res.data;

        if (data && data.length > 0) {
          const conversation = data[0];
          const convo =data[0]; // Assuming you have only one conversation in the array
          // chatData=conversation;
          // Iterate through the messages in the conversation
          setChatData(conversation.messages);
          
          // for (const message of conversation.messages) {
            
          //   const sender = message.sender;
          //   const username = sender.username;
          //   const text = message.text;
          //   const profilePic = sender.profile_pic;

          // }
        }
       


  };
  useEffect(() => {
    getChat();
    
  }, []);


  function loadMore() {
    if (meta?.next) {
      setNoScroll(false);
      dispatch(loadMoreMessage(meta.next));
    }
  }


  console.log(chatData)

         
  const chatMessages = chatData.chatMessages || [];
  console.log(chatMessages + 'ssss')
  return (
    <Message>
      <TweetHeader headerName={username} />

      <div className="main-div">
       
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
          
        <div>
          {console.log()}
        {chatData.map(chatMessage => (

          <div key={chatMessage.id}>

 <div
                  key={chatMessage.id}
                  className={
                    chatMessage?.sender?.username === me ? "msg-chat" : "rightby"
                  }
                >
                
                  {chatMessage?.sender?.username === username && (
                    <Link to={`/${chatMessage?.sender.username}`}>
                      <img
                        src={"http://127.0.0.1:8000/"+chatMessage?.sender.profile_pic}
                        alt="profile"
                        className="authorImage"
                      />
                    </Link>
                  )}

                  <div
                    className={
                      chatMessage.sender?.username === username
                        ? "msg-txt"
                        : "msg-txt right"
                    }
                  >
                    {chatMessage.text}
                  </div>
                </div>

          </div>
        ))}
      </div>

             
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
            <BiSend onClick={sendChat} className="largeicon mx-2" />
          </span>
        </div>
      </div>
    </Message>
  );
};

export default PrivateRoomChat;
