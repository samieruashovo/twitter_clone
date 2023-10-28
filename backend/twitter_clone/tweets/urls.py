from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r"", views.TweetViewSet, basename="tweetslist")
# router.register(r"femaletweet", views.FemaleTweetViewSet, basename="femaletweetslist")
router.register(r"explore/global", views.ExploreTweetViewSet)
# router.register(r"commentsx/", views.SinglePostCommentViewSetc, basename="commentslist")

# router.register(r"comments/l", views.ExploreLocalTweetViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("post/retweet/", views.ReTweetView, name="retweet-view"),
    path("comments/list/<str:pk>", views.ComentView.as_view()),
    path("tweet-detail/<str:uuid>", views.TweetDetailsView.as_view()),
    path(
        "comment_detail/<int:pk>/",
        views.CommentDetail.as_view(),
        name="comment-create-list",
    ),
    path("comments/reply/<int:pk>/", views.ComentReplyView, name="comment-reply"),
    path("love/like-unlike/", views.like_unlike_tweet, name="like-unlike"),
    path(
        "love/like-unlike-comment/",
        views.like_unlike_comment,
        name="like-unlike-comment",
    ),
    path("love/bookmark/", views.bookmark_tweet, name="bookmark"),
    path("love/bookmarkList/", views.bookmarkList, name="bookmark-list"),
    path("search/custom/", views.SearchList.as_view()),
    path("specific/<username>/", views.UserTweetList, name="user-tweet"),
]
