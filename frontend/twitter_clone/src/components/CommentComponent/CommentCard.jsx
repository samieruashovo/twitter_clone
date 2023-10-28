import React, { useState } from "react";
import { Link } from "react-router-dom";
import { TweetOperation } from "../TweetOperation";
import { FiMoreHorizontal } from "react-icons/fi";

import { useDispatch } from "react-redux";
import { BiCaretUp, BiCaretDown } from "react-icons/bi";
import {
  editComment,
  likeComment,
} from "../../redux/asyncActions/CommentAsync";
import Moment from "moment";
import ReplyComment from "./ReplyComment";
import { EditPost } from "../EditPost";
import { DropdownContent } from "./DropDownContent";

const CommentCard = ({ tweetId, user, comment }) => {
  const [curIndex, setCurIndex] = useState(null);
  const [showReply, setShowReply] = useState(false);
  const [edit, setEdit] = useState(false);
  const [editCommentInput, setEditComment] = useState(comment.body);
  const dispatch = useDispatch();
  const sendEditComment = (id) => {
    dispatch(editComment(id, editCommentInput));
    setEdit(false);
  };
  const likeTweetD = (id) => {
    dispatch(likeComment(id));
  };
  return (
    <div className="comment-card ">
      <span>
        <FiMoreHorizontal
          data-toggle="dropdown"
          className="dropdownIcon"
          aria-haspopup="true"
          aria-expanded="false"
        />
      </span>

      <div key={comment.id} className="comment-innerDiv">
        <Link to={`/${comment.username}`}>
        </Link>

        <div>
          <div className="comment-info">
            <span style={{ display: "flex", alignItems: "center" }}>
          <span className="mx-2 side-name">
            @ {comment.username} |
            <span className="mx-1">{Moment(comment.created).fromNow(true)}</span>
          </span>
        </span>
          </div>

          <EditPost
            edit={edit}
            editCommentInput={editCommentInput}
            setEditComment={setEditComment}
            comment={comment}
            setEdit={setEdit}
            sendEditComment={sendEditComment}
          />
        </div>
      </div>

      <TweetOperation
        reply={true}
        id={tweetId}
        comid={comment.id}
        liked={comment.iliked}
        likeTweetD={likeTweetD}
        like_count={comment.like_count}
        NoRetweetMark={true} //don't show retwet or bookmark for comment
      />
    </div>
  );
};

export default CommentCard;