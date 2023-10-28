import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
import { useSelector, useDispatch } from "react-redux";
import {
  tweet_detail,
  deleteTweet,
  likeTweet,
} from "../redux/asyncActions/TweetAsync";

import Second from "../components/Second";
import TweetHeader from "../components/TweetComponents/tweetHeader";
import { Link, useNavigate } from "react-router-dom";
import { FiMoreHorizontal } from "react-icons/fi";
import { AiOutlineDelete } from "react-icons/ai";
import { BiUserPlus, BiEditAlt, BiBlock } from "react-icons/bi";
import { removeMesage } from "../redux/slices/tweetSlice";
import AlertMessage from "../components/SmallComponent/alertMessage";
import { TweetOperation } from "../components/TweetOperation";
import { TweetContent } from "../components/TweetComponents/TweetContent";
import CommentCard from "../components/CommentComponent/CommentCard";
import {
  addComment,
  load_more_comment,
  tweet_comments,
} from "../redux/asyncActions/CommentAsync";
import ClipLoader from "react-spinners/ClipLoader";
import AddPicker from "../components/SmallComponent/AddPicker";
import { BiGlobe } from "react-icons/bi";
import { FaLock } from "react-icons/fa";
import Moment from "moment";

import { axiosInstance } from "../index";
import axios from "axios";
const url = "http://localhost:8000/";
const TweetDetail = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [edit, setEdit] = useState(false);
  const dispatch = useDispatch();

  const history = useNavigate();
  const [editTitle, setEditTitle] = useState("");
  const tweet = useSelector((state) => state.tweetReducer.singleTweet);
  console.log(tweet)
  // if(tweet !== undefined){
  //   console.log(tweet.data[0].uuid);
  // }
  console.log("tweetksjdfh")
  const [commentInput, setCommentInput] = useState("");
  const userIn = useSelector((state) => state.userReducer);

  const { uuid } = useParams();
  const { user, isAuthenticated } = userIn;


  const message = useSelector((state) => state.tweetReducer.message);
  const comments = useSelector((state) => state.commentReducer);
  const meta = comments.meta;

  useEffect(() => {
    console.log('running')
   
    dispatch(tweet_detail(uuid));
    dispatch(tweet_comments(uuid));
  }, [dispatch, uuid]);
  const likeTweetD = (uuid) => {
    dispatch(likeTweet(uuid));
  };
  message &&
    setTimeout(() => {
      dispatch(removeMesage());
    }, 3000);

  const editpost = () => {
    setEdit((prev) => !prev);
    setIsOpen(!isOpen);
    setEditTitle(tweet.title);
  };
  const commentAdd = () => {
    dispatch(addComment(uuid, commentInput));
    setCommentInput("");
  };
  // http://127.0.0.1:8000/tweets/comments/18/?page=2

  const loadMoreComment = () => {
    console.log(meta?.page, meta?.next);
    if (meta.next !== null) {
      dispatch(load_more_comment(uuid, meta.page + 1));
    }
  };

  // const loadTweet= () => async () => {
  //   try {
  //     if (localStorage.getItem("access")) {
  //       const res = await axiosInstance.get(`${url}tweets/tweet-detail/${uuid}`);
  //       console.log(res.data)
  //       console.log("kkkjjjjhhh")
  //     }
  //     await axios.get(`${url}tweets/tweet-detail/${uuid}`);
  //   } catch (err) {
  //     console.log(err+"asdf");
  //   }
  // }
  if (!tweet.data || tweet.data.length === 0) {
    return (
      <div>
        Loading... 
      </div>
    );
  }

  const title = tweet.data[0].title;

  return (
    <div>
  
      
  {tweet.data[0].username && (
        <Second>
          <TweetHeader headerName="Detail" />
          <div className="tweetCard">
            <div className="actual-tweet">
              {isAuthenticated && (
                <span>
                  <FiMoreHorizontal
                    data-toggle="dropdown"
                    className="dropdownIcon"
                    uuid={`#${tweet.data[0].uuid}dropdown`}
                    aria-haspopup="true"
                    aria-expanded="false"
                  />
{/* 
                  <div className="dropdown-menu dropdown-menu-right dropdownMenu">
                    {user?.email === tweet.data[0].email ? (
                      <>
                        <p onClick={editpost}>
                          <BiEditAlt />
                          <span>Edit Post</span>
                        </p>
                        <p
                          onClick={() => {
                            dispatch(deleteTweet(tweet.data[0].uuid));
                            history("/");
                          }}
                        >
                          <AiOutlineDelete color="#e0245e" />
                          <span style={{ color: "#e0245e" }}>Delete Post</span>
                        </p>
                      </>
                    ) : (
                      <p>
                        <BiBlock color="#e0245e" /> <span>Not your's Boi</span>
                      </p>
                    )}
                  </div> */}
                </span>
              )}
              <span className="add-tweet-image">
                <Link to={`/${tweet.data[0].username}`}>
                  <img
                    alt="img"
                    src={tweet.data[0].profile_pic}
                    className="rounded-circle author-image"
                    width="60px"
                    height="60px"
                  />
                </Link>
              </span>
              <TweetContent
                tweet={tweet.data[0]}
                editTitle={editTitle}
                setEditTitle={setEditTitle}
                edit={edit}
                setEdit={setEdit}
                id={tweet.data[0].uuid}
                dispatch={dispatch}
              />
            </div>
            <TweetOperation
              user={isAuthenticated ? user : ""}
              uuid={parseInt(uuid)}
              liked={tweet.iliked}
              likeTweetD={likeTweetD}
              like_count={tweet.like_count}
              tweet={tweet}
              comment_count={tweet.comment_count}
              bookmark={tweet.i_bookmarked}
            />
          </div>
          <section className="comment-list">
            {isAuthenticated && (
              <div className="commentDiv">
                <img
                  src={
                    (user && user.profile_pic) ||
                    "https://qph.fs.quoracdn.net/main-qimg-92e5c1d46505b34638aafd281449dabc"
                  }
                  alt="comment-author"
                  className="authorImage"
                />
                <textarea
                  value={commentInput}
                  onChange={(e) => setCommentInput(e.target.value)}
                  className="commentInput"
                  placeholder="Tweet your Reply"
                ></textarea>

                <button
                  disabled={!commentInput}
                  onClick={commentAdd}
                  className="link-tweet"
                >
                  {comments.uploading ? (
                    <ClipLoader color="white" loading={true} size={18} />
                  ) : (
                    "Reply"
                  )}
                </button>
              </div>
            )}
            {comments && comments.isLoading ? (
              <span className="d-flex justify-content-center mt-4">
                <ClipLoader color="#f44" loading={true} size={23} />
              </span>
            ) : (
              comments?.commentList.map((comment) => (
                <CommentCard
                  tweetId={tweet.uuid}
                  user={isAuthenticated ? user : ""}
                  key={comment.id}
                  comment={comment}
                />
              ))
            )}
            {!comments.isLoading && meta?.next && (
              <div className="mt-3 d-flex justify-content-center">
                <button onClick={loadMoreComment} className="link-tweet">
                  Load more
                </button>
              </div>
            )}
          </section>
        </Second>
      )}
    </div>
  );
  }
export default TweetDetail;



