import React from "react";
import { Link } from "react-router-dom";
import { FiMoreHorizontal } from "react-icons/fi";
import DropDown from "./DropDown";
import { TweetOperation } from "../TweetOperation";
import Moment from "moment";
import { likeTweet } from "../../redux/asyncActions/TweetAsync";
import { BiGlobe } from "react-icons/bi";
import { FaLock } from "react-icons/fa";

const TweetPostCard = ({ tweet, dispatch, user }) => {
  const likeTweetD = (uuid) => {
    dispatch(likeTweet(uuid));
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
            liked={tweet.myparent.iliked}
            likeTweetD={likeTweetD}
            like_count={tweet.myparent.like_count}
            tweet={tweet.myparent}
            bookmark={tweet.myparent.i_bookmarked}
            uuid={tweet.myparent.uuid}
            oriId={tweet.uuid}
            retweet={tweet?.username === user?.username ? true : false}
          />
        </>
      ) : (
        <>
          <TweetOperation
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
  const url = "http://localhost:8000/";
  return (
    <>
      <span className="d-flex">
        <span className="add-tweet-image ">
          <Link to={`/${tweet?.username}`}>
            <img
              alt="img"
              // src={tweet?.author.avatar}
              src={
                "https://dp.profilepics.in/profile-pictures-for-facebook-whatsapp/profile-pics/profile-pics-744.jpg"
              }
              className="rounded-circle author-image "
              width="60px"
              height="60px"
            />
          </Link>
        </span>

        <Link to={`${tweet?.username}/tweet/${tweet?.id}`}>
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
              {tweet?.title} {tweet?.body}
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
