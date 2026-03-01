from enum import Enum


class PostStatus(str, Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    PUBLISHED = "published"
    SCHEDULED = "scheduled"
    ARCHIVED = "archived"


class CommentStatus(str, Enum):
    VISIBLE = "visible"
    HIDDEN = "hidden"
    DELETED = "deleted"


class NotificationType(str, Enum):
    COMMENT_REPLY = "comment_reply"
    COMMENT_ON_POST = "comment_on_post"
    POST_PUBLISHED = "post_published"
    POST_APPROVED = "post_approved"
    NEW_FOLLOWER = "new_follower"
    MENTION = "mention"
    SYSTEM = "system"


class ModerationTargetType(str, Enum):
    POST = "post"
    COMMENT = "comment"
    USER = "user"


class ModerationActionType(str, Enum):
    WARN = "warn"
    HIDE = "hide"
    DELETE = "delete"
    BAN = "ban"
    RESTORE = "restore"

