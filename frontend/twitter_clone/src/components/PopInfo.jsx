import React from "react";

import { useDispatch, useSelector } from "react-redux";
import { userFollow } from "../redux/asyncActions/UserAsync";
import { Link } from "react-router-dom";
import { FollowInfo } from "./SmallComponent/FollowInfo";

const PopInfo = ({ tweet }) => {
  const userInfo = useSelector((state) => state.userReducer);
  const user = userInfo.user;
  const state = userInfo.followState;
  const followers = userInfo.followers;
  const dispatch = useDispatch();

  return (
    <>
      {tweet?.username === user?.username ? (
        ""
      ) : (
        <button
          onClick={() => dispatch(userFollow(tweet?.username))}
          className="link-tweet abs-follow"
        >
          {state ? state : tweet?.following ? "Following" : "Follow"}
        </button>
      )}

      <Link to={`/${tweet?.username}`}>
        <img
          alt="img"
              src={
                "https://dp.profilepics.in/profile-pictures-for-facebook-whatsapp/profile-pics/profile-pics-744.jpg"
              }
          // src={
          //   tweet?.profile_pic.includes("http://")
          //     ? tweet?.author.profile_pic
          //     : `http://127.0.0.1:8000${tweet?.profile_pic}`
          // }
          className="rounded-circle author-image "
          width="60px"
          height="60px"
        />
      </Link>
      <strong>{tweet?.username}</strong>
      <span className="side-name">@{tweet?.first_name}</span>
      {/* <p className="side-name">{tweet?.bio}</p> */}
      <div className="d-flex">
        {/* <FollowInfo
          number={followers ? followers : tweet.followers}
          followinfo="followers"
        /> */}
        {/* <FollowInfo number={tweet.author.following} followinfo="following" /> */}
      </div>
    </>
  );
};

export default React.memo(PopInfo);
