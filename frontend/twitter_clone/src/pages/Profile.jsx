import React, { useEffect, useState } from "react";
import {
  getUserInfo,
  userFollow,
  userProfile,
} from "../redux/asyncActions/UserAsync";
import { useDispatch, useSelector } from "react-redux";
import Second from "../components/Second";
import Moment from "moment";
import useUserInfo from "../hooks/useUserInfo";
import { AiOutlineSchedule } from "react-icons/ai";
import { BiSend } from "react-icons/bi";
import { Link, useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import TweetHeader from "../components/TweetComponents/tweetHeader";
import Viewer from "react-viewer";
import ClipLoader from "react-spinners/ClipLoader";
import { tweet_specific_user } from "../redux/asyncActions/TweetAsync";
import TweetPostCard from "../components/TweetComponents/TweetPostCard";
import { removeMesage } from "../redux/slices/tweetSlice";
import AlertMessage from "../components/SmallComponent/alertMessage";
import UserEditModal from "../components/UserRelated/UserEditModal";
import { FollowInfo } from "../components/SmallComponent/FollowInfo";

//new
import MomentUtils from "@date-io/moment";
// Material UI Imports
//// Core
import Button from "@material-ui/core/Button";
import Divider from "@material-ui/core/Divider";
import IconButton from "@material-ui/core/IconButton";
import Dialog from "@material-ui/core/Dialog";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogActions from "@material-ui/core/DialogActions";
import DialogTitle from "@material-ui/core/DialogTitle";
import TextField from "@material-ui/core/TextField";
import { withStyles } from "@material-ui/core/styles";

import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker,
} from "@material-ui/pickers";
//// Icons
import ArrowBackIcon from "@material-ui/icons/ArrowBack";
import LocationOnOutlinedIcon from "@material-ui/icons/LocationOnOutlined";
import LinkIcon from "@material-ui/icons/Link";
import DateRangeIcon from "@material-ui/icons/DateRange";
import CloseIcon from "@material-ui/icons/Close";
import "../styles/components/Profile.css";
// Custom Components

const Profile = () => {
  const { username } = useParams();
  // const username = localStorage.getItem("username");
  const { user: authUser } = useUserInfo();
  console.log("authUserProfilePage" + authUser);
  const userData = getUserInfo(localStorage.getItem("username"));
  const [showUserModal, setShowUserModal] = useState(false);
  const [visible, setVisible] = useState(false);
  const [covervisible, setCoverVisible] = useState(false);
  const dispatch = useDispatch();
  const userIn = useSelector((state) => state.userReducer);
  const isAuthenticated = userIn.isAuthenticated;
  const tweetsInfo = useSelector((state) => state.tweetReducer);
  const tweets = tweetsInfo.tweets;
  const message = tweetsInfo.message;
  const userprofile = userIn.profileUser;
  console.log("UserProfileProfilePage" + userprofile);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const history = useNavigate();

  message &&
    setTimeout(() => {
      dispatch(removeMesage());
    }, 3000);
  useEffect(() => {
    if (isAuthenticated) {
      dispatch(userProfile(username));
      dispatch(tweet_specific_user(username));
    }

    // if(!isAuthenticated){
    //   history.push('/login')
    // }
  }, [dispatch, username, history, isAuthenticated]);
  const handleClickEditModalOpen = () => {
    setEditModalOpen(true);
  };
  const handleEditModalClose = () => {
    setEditModalOpen(false);
    // setEditBirthDate(profileUser.birth_date ? moment(profileUser.birth_date) : null);
  };
  return (
    <div className="profile">
      <div>
        <div className="profile__header">
          <ArrowBackIcon className="profile__backIcon" />
          <div className="profile__header__validUser">
            <h2> Samier Shovo</h2>
            <div className="profile__header__tweetsNum"> 10 Tweets</div>
          </div>
        </div>
        <div className="profile__photos">
          <img
            className="profile__photos__bg"
            src="http://as01.epimg.net/betech/imagenes/2018/02/27/portada/1519723458_873061_1519723787_noticia_normal.jpg"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = "/static/images/bg_grey.png";
            }}
          />
          <img
            className="profile__photos__photo"
            src="https://dp.profilepics.in/profile-pictures-for-facebook-whatsapp/profile-pics/profile-pics-744.jpg"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = "/static/images/bg_lightgrey.png";
            }}
          />
        </div>
        <div className="profile__info">
          {authUser?.email === userprofile?.email ? (
            <div className="follow-or-edit">
              <button
                className="link-tweet"
                type="button"
                data-toggle="modal"
                data-target="#userModal"
                onClick={handleClickEditModalOpen}
              >
                Edit Profile
              </button>
            </div>
          ) : (
            <div className="follow-or-edit">
              <Link to={`/messages/w/${userprofile?.username}`}>
                <i className="largeicon mx-3 ">
                  <BiSend />
                </i>
              </Link>

              {userprofile?.i_follow ? (
                <button
                  onClick={() => dispatch(userFollow(userprofile.username))}
                  className="link-tweet "
                >
                  Unfollow
                </button>
              ) : (
                <button
                  onClick={() => dispatch(userFollow(userprofile.username))}
                  className="link-tweet"
                >
                  Follow
                </button>
              )}
            </div>
          )}

          <h2> Display name</h2>
          <p className="profile__info__username">@username</p>
          <p className="profile__info__bio">Profile Bio</p>
          <p className="profile__info__miscellaneous">
            Location
            {/* {profileUser.location ?
                                    <span>
                                        <LocationOnOutlinedIcon className="profile__info__icons" size="small"/>
                                        <span className="profile__info__location">{profileUser.location}</span>
                                    </span>
                                    : null
                                } */}
            {/* 
{profileUser.website ?
                                    <span>
                                        <LinkIcon className="profile__info__icons" size="small"/>
                                        <a className="profile__info__website" href={profileUser.website}>{new URL(profileUser.website).hostname}</a>
                                    </span>
                                    : null
                                } */}
            <span>
              {/* <DateRangeIcon className="profile__info__icons" size="small"/>
                                    <span>Joined <time dateTime={profileUser.date_joined}>
                                        {moment(profileUser.date_joined).tz(moment.tz.guess()).format('MMM YYYY')}
                                    </time></span> */}
            </span>
          </p>
          <p className="profile__info__follows">
            <span className="profile__info__followingsCount">0 Following</span>
            <span className="profile__info__followersCount">0 Followers</span>
          </p>
        </div>
        {/* {tweets.map((tweet) => (
          <TweetPostCard
            user={authUser}
            dispatch={dispatch}
            tweet={tweet}
            key={tweet.id}
          />
        ))} */}
        {/* <ProfileTweets 
                            currentUser={user} 
                            profileUser={profileUser} 
                            loadUserProfile={loadUserProfile} 
                            tweets_currentPage={tweets_currentPage}
                            tweets_setCurrentPage={tweets_setCurrentPage}
                            media_currentPage={media_currentPage}
                            media_setCurrentPage={media_setCurrentPage}
                            likes_currentPage={likes_currentPage}
                            likes_setCurrentPage={likes_setCurrentPage}
                        /> */}
      </div>

      <Dialog
        className="profile__editDialog"
        open={editModalOpen}
        onClose={handleEditModalClose}
        fullWidth
        maxWidth="sm"
      >
        <form id="form__editProfile">
          <DialogTitle className="profile__editDialog__title">
            <IconButton
              className="profile__editDialog__closeButton"
              onClick={handleEditModalClose}
              fullWidth
              maxWidth="sm"
            >
              <CloseIcon />
            </IconButton>
            <span>Edit profile</span>
            <Button
              type="submit"
              // className="profile__editDialog__saveButton"
              size="medium"
            >
              Save
            </Button>
          </DialogTitle>
          <DialogContent dividers className="profile__editDialog__content">
            <TextField
              id="profile__editForm__bgImage"
              name="header_photo"
              label="Background Image URL"
              variant="outlined"
              // defaultValue={profileUser.header_photo}
              InputLabelProps={
                {
                  // classes: {
                  //   root: classes.cssLabel,
                  //   focused: classes.cssFocused,
                  // },
                }
              }
              InputProps={
                {
                  // classes: {
                  //   root: classes.cssOutlinedInput,
                  //   focused: classes.cssFocused,
                  //   notchedOutline: classes.notchedOutline,
                  // },
                }
              }
            />
            <TextField
              id="profile__editForm__photo"
              name="photo"
              label="Avatar Photo URL"
              variant="outlined"
              // defaultValue={profileUser.photo}
              InputLabelProps={
                {
                  // classes: {
                  //   root: classes.cssLabel,
                  //   focused: classes.cssFocused,
                  // },
                }
              }
              InputProps={
                {
                  // classes: {
                  //   root: classes.cssOutlinedInput,
                  //   focused: classes.cssFocused,
                  //   notchedOutline: classes.notchedOutline,
                  // },
                }
              }
            />
            <TextField
              id="profile__editForm__displayName"
              name="display_name"
              label="Display Name"
              variant="outlined"
              // defaultValue={profileUser.display_name}
              InputLabelProps={
                {
                  // classes: {
                  //   root: classes.cssLabel,
                  //   focused: classes.cssFocused,
                  // },
                }
              }
              InputProps={
                {
                  // classes: {
                  //   root: classes.cssOutlinedInput,
                  //   focused: classes.cssFocused,
                  //   notchedOutline: classes.notchedOutline,
                  // },
                }
              }
              required
            />
            <TextField
              id="profile__editForm__bio"
              name="bio"
              label="Bio"
              variant="outlined"
              // defaultValue={profileUser.bio}
              InputLabelProps={
                {
                  // classes: {
                  //   root: classes.cssLabel,
                  //   focused: classes.cssFocused,
                  // },
                }
              }
              InputProps={
                {
                  // classes: {
                  //   root: classes.cssOutlinedInput,
                  //   focused: classes.cssFocused,
                  //   notchedOutline: classes.notchedOutline,
                  // },
                }
              }
            />
            <TextField
              id="profile__editForm__location"
              name="location"
              label="Location"
              variant="outlined"
              // defaultValue={profileUser.location}
              InputLabelProps={
                {
                  // classes: {
                  //   root: classes.cssLabel,
                  //   focused: classes.cssFocused,
                  // },
                }
              }
              InputProps={
                {
                  // classes: {
                  //   root: classes.cssOutlinedInput,
                  //   focused: classes.cssFocused,
                  //   notchedOutline: classes.notchedOutline,
                  // },
                }
              }
            />
            <TextField
              id="profile__editForm__website"
              name="website"
              label="Website"
              variant="outlined"
              // defaultValue={profileUser.website}
              InputLabelProps={
                {
                  // classes: {
                  //   root: classes.cssLabel,
                  //   focused: classes.cssFocused,
                  // },
                }
              }
              InputProps={
                {
                  // classes: {
                  //   root: classes.cssOutlinedInput,
                  //   focused: classes.cssFocused,
                  //   notchedOutline: classes.notchedOutline,
                  // },
                }
              }
            />
            <MuiPickersUtilsProvider utils={MomentUtils}>
              <KeyboardDatePicker
                disableToolbar
                variant="inline"
                inputVariant="outlined"
                format="YYYY-MM-DD"
                margin="normal"
                id="profile__editForm__birthDate"
                name="birth_date"
                label="Birth date"
                // defaultValue={
                //   profileUser.birth_date ? moment(profileUser.birth_date) : null
                // }
                // value={editBirthDate}
                // onChange={handleEditBirthDateChange}
                KeyboardButtonProps={{
                  "aria-label": "change date",
                }}
                InputLabelProps={
                  {
                    // classes: {
                    //   root: classes.cssLabel,
                    //   focused: classes.cssFocused,
                    // },
                  }
                }
                InputProps={
                  {
                    // classes: {
                    //   root: classes.cssOutlinedInput,
                    //   focused: classes.cssFocused,
                    //   notchedOutline: classes.notchedOutline,
                    // },
                  }
                }
              />
            </MuiPickersUtilsProvider>
          </DialogContent>
        </form>
      </Dialog>
    </div>
  );
};

export default Profile;
