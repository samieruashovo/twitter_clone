import React from "react";
import { Link } from "react-router-dom";
import { FiMoreHorizontal } from "react-icons/fi";
import DropDown from "./DropDown";
import { TweetOperation } from "../TweetOperation";
import Moment from "moment";
import { likeTweet } from "../../redux/asyncActions/TweetAsync";
import { BiGlobe } from "react-icons/bi";
import { FaLock } from "react-icons/fa";
import { useEffect, useState } from "react";
import axios from "axios";
import { axiosInstance } from "../..";



const TweetPostCard = ({ tweet, dispatch, user }) => {
 


  console.log(tweet)
  var uid = tweet.uuid
  const likeTweetD = () => {
    dispatch(likeTweet(uid));
  };
  
  return (
    <div className="tweetCard">
      <div className="actual-tweet">
        <div>
          <FiMoreHorizontal
            data-toggle="dropdown"
            className="dropdownIcon"
            uuid={`#${tweet.uuid}dropdown`}
            aria-haspopup="true"
            aria-expanded="false"
          />
          {/* this is delete button */}
          {/* <DropDown
            target={`${tweet.id}dropdown`}
            tweet={tweet}
            user={user}
            tweetId={tweet.id}
          /> */}
        </div>
        {tweet.parent ? (
          <div style={{ display: "flex", flexDirection: "column" }}>
            <strong>
              <Link
                to={`${tweet.username}` || ""}
                className="mx-2 side-name"
              >
                {tweet?.username === user?.username
                  ? "You "
                  : tweet.username}{" "}
                retweeted !
              </Link>
            </strong>

            <TweetHasParentOrNot tweet={tweet.myparent} />
          </div>
        ) : (
          <TweetHasParentOrNot tweet={tweet} />
        )}
      </div>
      {tweet.parent ? (
        <>
          <TweetOperation
            username = {tweet.username}
            liked={tweet.iliked}
            likeTweetD={likeTweetD}
            like_count={tweet.myparent.like_count}
            tweet={tweet}
            bookmark={tweet.myparent.i_bookmarked}
            uuid={tweet.myparent.uuid}
            oriId={tweet.uuid}
            retweet={tweet?.username === user?.username ? true : false}
          />
        </>
      ) : (
        <>
          <TweetOperation
          username = {tweet.username}
            liked={tweet.iliked}
            likeTweetD={likeTweetD}
            like_count={tweet.like_count}
            tweet={tweet}
            bookmark={tweet.i_bookmarked}
            id={tweet.id}
            comment_count={tweet.comment_count}
          />
        </>
      )}
    </div>
  );
};

export default TweetPostCard;

const TweetHasParentOrNot = ({ tweet }) => {
  const [profilePicture, setProfilePicture] = useState(false);

  const getUserInfo = async (username) => {
    console.log("asee");
    
    try {
      console.log("kssksk");
      const res = await axiosInstance.get(`http://localhost:8000/user/${username}/`);
      setProfilePicture(res.data.profile_pic)
      console.log(profilePicture+ "alllll")
     
  
  
    } catch (err) {

      // console.log(err);
    }
  };
  useEffect(() => {
    console.log("laksdja")
    getUserInfo(tweet?.username);
    console.log("laksdjadone")
  }, [tweet?.username]);
  const url = "http://localhost:8000/";
  return (
    <>
      <span className="d-flex">
        <span className="add-tweet-image ">
          <Link to={`/${tweet?.username}`}>

          {profilePicture ? ( // Check if profilePicture has a value
        <img 
        className="rounded-circle author-image "
              width="60px"
              height="60px"
        src={profilePicture} alt="Profile" />
      ) : (
        <img className="rounded-circle author-image "
        width="60px"
        height="60px"
          src="https://dp.profilepics.in/profile-pictures-for-facebook-whatsapp/profile-pics/profile-pics-744.jpg"
          alt="Default Profile"
        />
      )}
          </Link>
        </span>

        <Link to={`${tweet?.username}/tweet/${tweet?.uuid}`}>
          <div className="tweet-content">
            <span id="hover" className="d-flex">
              {/* {tweet?.username} */}
              <span className="side-name">
                @ {tweet?.username} |{" "}
                {Moment(tweet?.created).fromNow(true)}
                <span className="mx-2">
                  {tweet?.is_private ? <FaLock /> : <BiGlobe />}
                  {tweet?.isEdited && <span className="mx-2">- Edited</span>}
                </span>
              </span>
            </span>

            <p className="mt-2">
  <div className="divider">
    {tweet?.title}
  </div>
  <div className="divider">
    {tweet?.body}
  </div>
</p>
            {tweet?.image && (
              <img alt="img" src={tweet?.image} className="image img" />
            )}
          </div>
        </Link>
      </span>
    </>
  );
};
