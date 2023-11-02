from tweets.models import Tweet


# class MainRouter:
#     route_app_labels = {
#         "auth",
#         "contenttypes",
#         "admin",
#         "sessions",
#         "users",
#         "chat",
#         "media",
#         "avatars",
#         "notifications",
#         # "community",
#     }

#     def db_for_read(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             return "male_user_db"
#         return None

#     def db_for_write(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             return "male_user_db"
#         return None

#     def allow_relation(self, obj1, obj2, **hints):
#         if (
#             obj1._meta.app_label in self.route_app_labels
#             or obj2._meta.app_label in self.route_app_labels
#         ):
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         return db == "male_user_db"


# class Default:
#     route_app_labels = {
#         "auth",
#         "contenttypes",
#         "admin",
#         "sessions",
#         "users",
#         "chat",
#         "media",
#         "avatars",
#         "notifications",
#         # "community",
#     }

#     def db_for_read(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             return "main_db"
#         return None

#     def db_for_write(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             print("gender default: ")
#             return "main_db"
#         return None

#     def allow_relation(self, obj1, obj2, **hints):
#         if (
#             obj1._meta.app_label in self.route_app_labels
#             or obj2._meta.app_label in self.route_app_labels
#         ):
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if app_label in self.route_app_labels:
#             return db == "main_db"
#         return None


class TweetRouter:
    route_app_labels = {
        "tweets",
        "contenttypes",
        "admin",
        "sessions",
        # "users",
        "chat",
        "media",
        "avatars",
        "notifications",
        "community",
    }

    def db_for_read(self, model, **hints):
        return "male_user_db"
        # if model._meta.app_label == "tweets":
        #     # print("ssas")
        #     return "male_user_db"

        # return None

    def db_for_write(self, model, **hints):
        print("ssas2")
        if model._meta.app_label == "tweets":
            print("ssas3")
            # Access the current instance of Tweet and check the username
            tweet_instance = hints.get("instance")
            # print(tweet_instance)
            # print("hints")
            # print(hints)

            if tweet_instance and hasattr(tweet_instance, "gender"):
                # print("ssas4")
                if tweet_instance.gender == "male":
                    # print('ssas5')
                    # print("genderss: ")
                    return "male_user_db"  # Write to male_user_db
                else:
                    # print('ssas6')
                    # print("gender: ")
                    return "female_user_db"
        elif model._meta.app_label == "chat":
            # message_instance = hints.get("instance")
            # if message_instance:
            #     print("message_instance "+message_instance.user1.username)
            return "male_user_db"
        elif model._meta.app_label == "community":
            post_instance = hints.get("instance")
            if post_instance and hasattr(post_instance, "gender"):
                # print("ssas4")
                if post_instance.gender == "male":
                    # print('ssas5')
                    # print("genderss: ")
                    return "male_user_db"  # Write to male_user_db
                else:
                    # print('ssas6')
                    # print("gender: ")
                    return "female_user_db"
        else:
            return 'male_user_db'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if both objects belong to the "tweets" app
        if obj1._meta.app_label == "tweets" and obj2._meta.app_label == "tweets":
            return True
        else:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # return db == "female_user_db"
        # Allow migrations only for the "tweets" app's models in the specified database
        return db in ["female_user_db", "male_user_db"]
        # return None


# class Aqua:
#     route_app_labels = {"aqua"}

#     def db_for_read(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             return "aqua_db"
#         return None

#     def db_for_write(self, model, **hints):
#         if model._meta.app_label in self.route_app_labels:
#             return "aqua_db"
#         return None

#     def allow_relation(self, obj1, obj2, **hints):
#         if (
#             obj1._meta.app_label in self.route_app_labels
#             or obj2._meta.app_label in self.route_app_labels
#         ):
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if app_label in self.route_app_labels:
#             return db == "aqua_db"
#         return None
